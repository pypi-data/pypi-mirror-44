import click
import keyring
import logging
from os import path
import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from pathlib import Path

logger = logging.getLogger(__name__)


def _build_dkb_filename(text, dt):
    # reimplement the dkb service side logic to omit the GET request to get a content-disposition hdr

    # z.B. "Kreditkartenabrechnung 1234********1234 per 21.09.2018"
    # oder "Kontoauszug Nr. 009_2018 zu Konto 1011234567"

    m = re.findall(r"Kontoauszug Nr. (\d{3})_(\d{4}) zu Konto (\d+)", text)
    if len(m) == 1:
        m = m[0]
        return f"Kontoauszug_{m[2]}_Nr_{m[1]}_{m[0]}_per_{dt:%Y_%m_%d}.pdf"

    m = re.findall(
        r"Kreditkartenabrechnung (\d{4}\*+\d{4}) per (\d{2}\.\d{2}\.\d{4})", text
    )
    if len(m) == 1:
        m = m[0]
        dt = datetime.strptime(m[1], "%d.%m.%Y")
        return f"Kreditkartenabrechnung_{m[0]}_per_{dt:%Y_%m_%d}.pdf".replace("*", "x")

    raise NotImplementedError("could not parse", text)


def _parse_docs(soup):
    for tr in (
        soup.find("div", {"class": "mbo-FolderViewFilter"})
        .find("table")
        .find("tbody")
        .find_all("tr")
    ):
        link = (
            "https://www.dkb.de"
            + [
                l for l in tr.find_all("a") if "getMailboxAttachment" in l.attrs["href"]
            ][0].attrs["href"]
        )
        date = datetime.strptime(
            tr.find("td", {"class": "abaxx-aspect-created"}).text, "%d.%m.%Y"
        ).date()
        filename_orig = tr.find("a", {"class": "evt-getMailboxAttachment"}).text
        filename = _build_dkb_filename(filename_orig, date)
        yield {"date": date, "filename": filename, "link": link}


class DKBDocDownloader:
    def __init__(self):
        self._session = requests.session()
        self._logged_in = False

    def login(self, username, password):
        r = self._session.get("https://www.dkb.de/-")
        soup = BeautifulSoup(r.content, "lxml")
        data = {
            i.attrs["name"]: i.attrs["value"] if "value" in i.attrs else ""
            for i in soup.find("form", {"id": "login"}).find_all("input")
        }
        data.update({"j_username": username, "j_password": password})
        res = self._session.post("https://www.dkb.de/banking", data=data)

        # check login success
        assert (
            res.url
            == "https://www.dkb.de/DkbTransactionBanking/content/banking/financialstatus/FinancialComposite/FinancialStatus.xhtml?$event=init"
        ), "login failed"

        self._logged_in = True

    def list_giro(self):
        return self._list(
            "https://www.dkb.de/banking/postfach/ordner?$event=gotoFolder&folderNameOrId=%24kontoauszuege"
        )

    def list_visa(self):
        return self._list(
            "https://www.dkb.de/banking/postfach/ordner?$event=gotoFolder&folderNameOrId=%24kontoauszuege"
        )

    def _list(self, url):
        assert self._logged_in, "not logged in"
        r = self._session.get(url)
        assert r.ok
        soup = BeautifulSoup(r.content, "lxml")
        return list(_parse_docs(soup))

    def download(self, doc):
        assert self._logged_in, "not logged in"
        rf = self._session.get(doc["link"])
        assert rf.ok, "download failed"
        return rf.content


@click.command()
@click.option("--username", required=True)
@click.option("--password", default=None)
@click.option("--days", type=int, default=90)
@click.option(
    "--root", default=".", help="root destination directory to save downloaded files"
)
@click.option("-v", "--verbose", is_flag=True)
def fetch_dkb_documents(username, password, days, root, verbose):
    logging.basicConfig(level=(logging.DEBUG if verbose else logging.INFO))

    if not password:
        password = keyring.get_password("nobbofin", username)

    if not password:
        logger.error(
            "please set password using 'keyring set nobbofin %s' or pass it using --password",
            username,
        )
        exit(1)

    root = Path(root)

    end = datetime.today()
    begin = (end - timedelta(days=days)).date()

    dl = DKBDocDownloader()
    dl.login(username, password)
    docs = dl.list_visa() + dl.list_giro()

    for d in docs:
        if d["date"] < begin:
            continue
        bc_filename = d["date"].strftime("%Y-%m-%d") + "_" + d["filename"]
        bc_path = root / bc_filename
        if path.exists(bc_path):
            # skipping file
            continue

        content = dl.download(d)

        with open(bc_path, "wb") as f:
            f.write(content)

        logger.info("downloaded %s", d["filename"])


if __name__ == "__main__":
    fetch_dkb_documents()
