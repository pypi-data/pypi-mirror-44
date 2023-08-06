import email


import html
import quopri
import re
from dateutil import parser


# Source: https://github.com/django/django/blob/master/django/utils/text.py
# but with allowed spaces
from weasyprint import HTML, CSS


def get_valid_filename(s):
    s = str(s).strip()
    return re.sub(r"(?u)[^-\w. ]", "", s)


def extract_text(part):
    if part.get("Content-Transfer-Encoding") == "quoted-printable":
        return quopri.decodestring(part.get_payload()).decode(
            part.get_content_charset()
        )
    raise NotImplementedError()


def convert(msg: email.message.Message):
    dt = parser.parse(msg["Date"])
    pt_num = 0
    for part in msg.walk():

        filename = get_valid_filename(f"{dt:%Y-%m-%d} - {msg['Subject']}")
        if pt_num > 0:
            filename += f" - {pt_num}"
        filename += ".pdf"
        pt_num += 1

        if part.get_content_maintype() == "text":
            txt = f"""
                <table>
                <tr>
                    <th>Von:</th>
                    <td>{html.escape(msg['From'])}</td>
                </tr>
                <tr>
                    <th>Betreff:</th>
                    <td>{html.escape(msg['Subject'])}</td>
                </tr>
                <tr>
                    <th>Datum:</th>
                    <td>{dt}</td>
                </tr>
                <tr>
                    <th>An:</th>
                    <td>{html.escape(msg['To'])}</td>
                </tr>
                </table>

                    <hr>
                    <pre>{extract_text(part)}</pre>
                """
            yield filename, HTML(string=txt).write_pdf(
                stylesheets=[
                    CSS(
                        string="""
                        @page {
                            size: A4;
                            @bottom-right{
                                content: "Seite " counter(page) " von " counter(pages);
                                font-size: 10pt;
                            }
                        }
                        body {
                            font-size: 10pt;
                        }
                        pre {
                            white-space: pre-wrap;
                            word-wrap: break-word;
                        }
                    """
                    )
                ]
            )
