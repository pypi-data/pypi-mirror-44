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

logger = logging.getLogger(__name__)


R = namedtuple("R", ["c1", "c2", "destination"])

cfg = {
    "INBOX.Unwichtig": [
        R("FROM", '"buchungsbestaetigung@bahn.de"', "Expenses/Reise/Bahn"),
        R("FROM", '"service@drive-now.com"', "Expenses/Reise/Carsharing"),
        R("FROM", '"kundenservice@car2go.com"', "Expenses/Reise/Carsharing"),
        R("FROM", '"noreply@car2go.com"', "Expenses/Reise/Carsharing"),
        R("FROM", '"billing@hetzner.com"', "Expenses/Nerdworks/Hosting"),
        R("FROM", '"service-shop@deutschepost.de"', "Expenses/Nerdworks/Porto"),
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
def fetch_mail_attachments(host, user, password, root, move_to, verbose):
    logging.basicConfig(level=(logging.DEBUG if verbose else logging.INFO))

    if not password:
        password = keyring.get_password("nobbofin", user)

    if not password:
        logger.error(
            "please set password using 'keyring set nobbofin %s' or pass it using --password",
            user,
        )
        exit(1)

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
                process_rule(M, root, rule, move_to)

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


def process_rule(M: imaplib.IMAP4, root: Path, rule: R, imap_target: str):
    logger.debug("searching for %s = %s", rule.c1, rule.c2)
    typ, msgnums = M.search(None, rule.c1, rule.c2)
    assert typ == "OK"
    logger.debug("list of message-nums:")
    logger.debug(msgnums)
    msg_uids = []
    for num in msgnums[0].split():
        logger.debug("fetching message num %s", num)
        typ, data = M.fetch(num, "(RFC822 UID)")
        logger.debug("message %s fetched, parsing...", num)
        msg = email.message_from_bytes(data[0][1])
        process_message(msg, root, rule)

        # sample for data[0][0]:
        # b'12 (UID 1677 RFC822 {31481}'
        logger.debug("data[0][0]: %s", data[0][0])
        msg_uid = re.findall("UID (\d+) ", data[0][0].decode("ascii"))[0]
        logger.debug("message UID: %s", msg_uid)
        msg_uids.append(msg_uid)

    if imap_target:
        move_messages(M, msg_uids, imap_target)


def process_message(msg, root, rule):
    dt = parser.parse(msg["date"])
    logger.debug("msg date: %s", dt)
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            logger.debug("skipping multipart")
            continue
        if part.get("Content-Disposition") is None:
            logger.debug("skipping missing content-disposition")
            continue
        if part.get_filename() is None:
            logger.debug("skipping missing filename")
            continue

        logger.debug("found %s", part.get_filename())
        dest_folder = root / rule.destination
        dest_folder.mkdir(parents=True, exist_ok=True)

        filename = f"{dt:%Y-%m-%d} {part.get_filename()}"
        dest_path = dest_folder / filename

        if not dest_path.is_file():
            with dest_path.open("wb") as f:
                f.write(part.get_payload(decode=True))
                f.close()
            logger.info("saved %s", dest_path)
        else:
            logger.debug("skipping %s - file exists", dest_path)


if __name__ == "__main__":
    fetch_mail_attachments()
