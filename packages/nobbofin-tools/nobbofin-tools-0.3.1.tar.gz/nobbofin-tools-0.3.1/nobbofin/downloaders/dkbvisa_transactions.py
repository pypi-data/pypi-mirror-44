import click
import keyring
import logging
from bs4 import BeautifulSoup
from datetime import datetime
import requests
from pathlib import Path

logger = logging.getLogger(__name__)


def read_dkbvisa(username, password):
    session = requests.session()
    r = session.get("https://www.dkb.de/-")
    r_soup = BeautifulSoup(r.content, "lxml")
    data = {
        i.attrs["name"]: i.attrs["value"] if "value" in i.attrs else ""
        for i in r_soup.find("form", {"id": "login"}).find_all("input")
    }
    data["j_username"] = username
    data["j_password"] = password
    res = session.post("https://www.dkb.de/banking", data=data)

    # check login success
    assert (
        res.url
        == "https://www.dkb.de/DkbTransactionBanking/content/banking/financialstatus/FinancialComposite/FinancialStatus.xhtml?$event=init"
    )

    # query last 90 days
    res2 = session.post(
        "https://www.dkb.de/banking/finanzstatus/kreditkartenumsaetze",
        data={
            "slAllAccounts": "1",
            "slTransactionStatus": "0",
            "filterType": "PERIOD",
            "slSearchPeriod": "3",
            "postingDate": "",
            "toPostingDate": "",
            "$event": "search",
        },
    )
    res2_soup = BeautifulSoup(res2.content, "lxml")
    balance_date = datetime.strptime(
        res2_soup.find("div", {"class": "accountBalance"})
        .find("span")
        .text.strip()[10:],
        "%d.%m.%Y",
    ).date()

    # read CSV content
    res3 = session.get(
        "https://www.dkb.de/banking/finanzstatus/kreditkartenumsaetze?$event=csvExport"
    )
    csv_data = res3.text
    return balance_date, csv_data


@click.command()
@click.option("--username", required=True)
@click.option("--password", default=None)
@click.option(
    "--root", default=".", help="root destination directory to save downloaded files"
)
@click.option("-v", "--verbose", is_flag=True)
def main(username, password, root, verbose):
    logging.basicConfig(level=(logging.DEBUG if verbose else logging.INFO))

    if not password:
        password = keyring.get_password("nobbofin", username)

    if not password:
        logger.error(
            "please set password using 'keyring set nobbofin %s' or pass it using --password",
            username,
        )
        exit(1)

    dl_dkbvisa_transactions(username, password, root)


def dl_dkbvisa_transactions(username, password, root):
    root = Path(root)
    balance_date, csv_data = read_dkbvisa(username, password)
    filename = f"{balance_date} DKBVISA {username}.csv"
    with open(root / filename, "w", encoding="utf-8") as outfile:
        outfile.write(csv_data)


if __name__ == "__main__":
    main()
