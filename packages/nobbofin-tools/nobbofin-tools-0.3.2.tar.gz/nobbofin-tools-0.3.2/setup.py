from setuptools import setup

setup(
    name="nobbofin-tools",
    version="0.3.2",
    author="Enno Lohmeier",
    author_email="elo-pypi@nerdworks.de",
    packages=[
        "nobbofin",
        "nobbofin.converters",
        "nobbofin.importers",
        "nobbofin.downloaders",
    ],
    install_requires=[
        "beancount >= 2.1",
        "simplejson >= 3.1",
        "click",
        "fints",
        "keyring",
        "requests",
        "beautifulsoup4",
        "weasyprint",
    ],
    scripts=[
        "nobbofin/downloaders/mail_attachments.py",
        "nobbofin/downloaders/mail_content2pdf.py",
        "nobbofin/downloaders/coba_docs.py",
        "nobbofin/downloaders/dkb_docs.py",
        "nobbofin/downloaders/dkbvisa_transactions.py",
        "nobbofin/downloaders/fints_transactions.py",
    ],
)
