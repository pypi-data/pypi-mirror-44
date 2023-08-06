import click
import keyring
import logging
import simplejson as json
from datetime import datetime, timedelta
from fints.client import FinTS3PinTanClient
from fints.dialog import FinTSDialogError
from pathlib import Path

logger = logging.getLogger(__name__)


def _fix_amount(obj):
    return {k: (v.__dict__ if k == "amount" else v) for k, v in obj.items()}


def read_fints(blz, kto, username, password, url, begin, end, tan_mechanism):

    try:
        client = FinTS3PinTanClient(blz, username, password, url)
        if tan_mechanism:
            client.set_tan_mechanism(tan_mechanism)
        accounts = client.get_sepa_accounts()
        if kto:
            account = [a for a in accounts if a.accountnumber == kto][0]
        else:
            account = accounts[0]  # use first account if no kto provided

        balance = client.get_balance(account)
        statement = client.get_transactions(account, begin, end)

        return {
            "balance": _fix_amount(balance.__dict__),
            "statement": [_fix_amount(t.data) for t in statement],
        }
    except FinTSDialogError as ex:
        print("error fetching transaction from", url)
        raise ex


@click.command()
@click.option("--blz", required=True)
@click.option("--kto")
@click.option("--username", required=True)
@click.option("--password", default=None)
@click.option("--url", required=True)
@click.option("--tan-mechanism")
@click.option("--days", type=int, default=90)
@click.option(
    "--root", default=".", help="root destination directory to save downloaded files"
)
@click.option("-v", "--verbose", is_flag=True)
def main(blz, kto, username, password, url, tan_mechanism, days, root, verbose):
    logging.basicConfig(level=(logging.DEBUG if verbose else logging.INFO))

    if not password:
        password = keyring.get_password("nobbofin", username)

    if not password:
        logger.error(
            "please set password using 'keyring set nobbofin %s' or pass it using --password",
            username,
        )
        exit(1)

    dl_fints_transactions(blz, kto, username, password, url, tan_mechanism, days, root)


def dl_fints_transactions(blz, kto, username, password, url, tan_mechanism, days, root):
    root = Path(root)
    end = datetime.today()
    begin = end - timedelta(days=days)
    data = read_fints(blz, kto, username, password, url, begin, end, tan_mechanism)
    filename = (
        f"{data['balance']['date']} FinTS {blz} {begin.date()} - {end.date()}.json"
    )
    with open(root / filename, "w", encoding="utf-8") as outfile:
        json.dump(
            data, outfile, use_decimal=True, default=str, indent=4, sort_keys=True
        )


if __name__ == "__main__":
    main()
