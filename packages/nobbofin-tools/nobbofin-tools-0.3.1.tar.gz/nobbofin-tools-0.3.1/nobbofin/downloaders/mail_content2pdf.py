from collections import namedtuple

import click
import email
import imaplib
import keyring
import logging
import re
import ssl
from dateutil import parser
from pathlib import Path

from nobbofin.converters import msg2pdf

logger = logging.getLogger(__name__)


R = namedtuple("R", ["c1", "c2", "destination"])

cfg = {
    "INBOX.Unwichtig": [
        R("FROM", '"onlineshop@hochbahn.de"', "Expenses/Reise/Nahverkehr")
    ]
}


@click.command()
@click.option("--host")
@click.option("--user")
@click.option("--password", default=None)
@click.option(
    "--root", default=".", help="root destination directory to save downloaded files"
)
@click.option(
    "--move-to", default=None, help="target folder to move processed messages to"
)
@click.option("-v", "--verbose", is_flag=True)
@click.option("-d", "--dump", is_flag=True)
def main(host, user, password, root, move_to, verbose, dump):
    logging.basicConfig(level=(logging.DEBUG if verbose else logging.INFO))

    if not password:
        password = keyring.get_password("nobbofin", user)

    if not password:
        logger.error(
            "please set password using 'keyring set nobbofin %s' or pass it using --password",
            user,
        )
        exit(1)

    dl_mail_content_as_pdf(host, user, password, root, move_to, dump)


def dl_mail_content_as_pdf(host, user, password, root, move_to, dump=False):
    root = Path(root)
    context = ssl.create_default_context()
    with imaplib.IMAP4_SSL(host=host, ssl_context=context) as M:
        M.login(user, password)
        logger.debug("IMAP: logged in successfully")

        logger.debug("list of folders:")
        logger.debug(M.list()[1])

        for mailbox, rules in cfg.items():
            M.select(mailbox=mailbox, readonly=False)

            for rule in rules:
                process_rule(M, root, rule, move_to, dump)

        M.logout()
        logger.debug("IMAP: logged out")


def move_messages(M: imaplib.IMAP4, msg_uids, target):
    for msg_uid in msg_uids:
        typ, data = M.uid("COPY", msg_uid, target)
        assert typ == "OK"
        logger.debug("msg %s moved", msg_uid)

        typ, data = M.uid("STORE", msg_uid, "+FLAGS", "(\Deleted)")
        assert typ == "OK"
        logger.debug("msg %s marked for deletion", msg_uid)

    M.expunge()
    logger.debug("mailbox expunged")


def process_rule(M: imaplib.IMAP4, root: Path, rule: R, imap_target: str, dump: bool):
    logger.debug("searching for %s = %s", rule.c1, rule.c2)
    typ, msgnums = M.search(None, rule.c1, rule.c2)
    assert typ == "OK"
    logger.debug("list of message-nums:")
    logger.debug(msgnums)
    msg_uids = []
    for num in msgnums[0].split():
        logger.debug("fetching message num %s", num)
        typ, data = M.fetch(num, "(RFC822 UID)")

        # sample for data[0][0]:
        # b'12 (UID 1677 RFC822 {31481}'
        logger.debug("data[0][0]: %s", data[0][0])
        msg_uid = re.findall("UID (\d+) ", data[0][0].decode("ascii"))[0]
        logger.debug("message UID: %s", msg_uid)
        msg_uids.append(msg_uid)

        if dump:
            with open(msg_uid + ".msg", "wb") as f:
                f.write(data[0][1])
            logger.info("dumped message to %s.msg", msg_uid)

        logger.debug("message %s fetched, parsing...", num)
        msg = email.message_from_bytes(data[0][1])
        process_message(msg, root, rule)

    if imap_target:
        move_messages(M, msg_uids, imap_target)


def process_message(msg, root, rule):
    dt = parser.parse(msg["date"])
    logger.debug("msg date: %s", dt)

    for filename, pdf in msg2pdf.convert(msg):
        dest_folder = root / rule.destination
        dest_folder.mkdir(parents=True, exist_ok=True)

        dest_path = dest_folder / filename

        if not dest_path.is_file():
            with dest_path.open("wb") as f:
                f.write(pdf)
                f.close()
            logger.info("saved %s", dest_path)
        else:
            logger.debug("skipping %s - file exists", dest_path)


if __name__ == "__main__":
    main()
