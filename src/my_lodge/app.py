import io
import os
import random
from datetime import datetime
from urllib.parse import quote

import qrcode
import yaml
from flask import Flask, redirect, render_template, request, send_file, session, url_for
from jinja2 import ChoiceLoader, FileSystemLoader, PackageLoader, PrefixLoader

from my_lodge.cli import BOOKS_REPO, ROOT, build

_CHARGE = "Charge to the Initiate, First Degree"
_TOOLS = "Working Tools, First Degree"

QUOTES = [
    {
        "text": (
            "Ancient no doubt it is, having subsisted from time immemorial;"
            " and honourable it must be acknowledged to be, as, by a natural"
            " tendency, it conduces to make those so who are obedient to its precepts."
        ),
        "source": _CHARGE,
    },
    {
        "text": (
            "No institution can boast of a more solid foundation than that on which"
            " Freemasonry rests — the practice of every moral and social virtue."
        ),
        "source": _CHARGE,
    },
    {
        "text": (
            "In every age, monarchs themselves have been promoters of the art,"
            " have not thought it derogatory to their dignity to exchange the"
            " sceptre for the trowel, have patronised our mysteries and joined"
            " in our assemblies."
        ),
        "source": _CHARGE,
    },
    {
        "text": (
            "Consider it as the unerring standard of truth and justice and regulate"
            " your life and actions by the divine precepts it contains."
        ),
        "source": _CHARGE,
    },
    {
        "text": (
            "To your neighbour, by acting with him on the square, by rendering him"
            " every kind office that justice or mercy may require, by relieving his"
            " necessities and soothing his afflictions."
        ),
        "source": _CHARGE,
    },
    {
        "text": (
            "Let prudence direct you, temperance chasten you, fortitude support you,"
            " and justice be the guide of all your actions."
        ),
        "source": _CHARGE,
    },
    {
        "text": (
            "Be especially careful to maintain in their fullest splendour those truly"
            " Masonic ornaments — benevolence and charity."
        ),
        "source": _CHARGE,
    },
    {
        "text": (
            "Secrecy consists of an inviolable adherence to the obligation you have"
            " so solemnly entered into — never improperly to disclose any of those"
            " Masonic secrets that have been, or may at any future time be,"
            " entrusted to your keeping."
        ),
        "source": _CHARGE,
    },
    {
        "text": (
            "Dedicate yourself to such pursuits as may enable you to continue"
            " respectable in life, useful to mankind, and an ornament to the"
            " society of which you have this day become a member."
        ),
        "source": _CHARGE,
    },
    {
        "text": "Endeavour to make a daily advancement in Masonic knowledge.",
        "source": _CHARGE,
    },
    {
        "text": (
            "As we are not operative, but free and accepted, or speculative, masons,"
            " we apply these tools to morals."
        ),
        "source": _TOOLS,
    },
    {
        "text": (
            "The 24-inch gauge represents the 24 hours of the day: part to be spent"
            " in prayer to Almighty God, part in labour and refreshment, and part in"
            " serving a friend or brother in time of need, when we can do so without"
            " detriment to ourselves or connections."
        ),
        "source": _TOOLS,
    },
    {
        "text": (
            "The common gavel denotes the force of conscience, which should keep down"
            " all vain and unbecoming thoughts, so that our words and actions may"
            " ascend unpolluted to the throne of grace."
        ),
        "source": _TOOLS,
    },
    {
        "text": (
            "The chisel points out the advantages of education, by which means we are"
            " rendered fit members for well-organised society."
        ),
        "source": _TOOLS,
    },
    {
        "text": (
            "Should you at any time meet a friend or brother in distressed"
            " circumstances, you will remember the peculiar moment when, poor and"
            " penniless, you were admitted into Freemasonry and cheerfully embrace"
            " the opportunity of practising towards him that virtue you now profess"
            " to admire."
        ),
        "source": _CHARGE,
    },
]

app = Flask(
    __name__,
    static_folder=str(ROOT / "static"),
    template_folder=str(ROOT / "templates"),
)
app.jinja_loader = ChoiceLoader(
    [
        FileSystemLoader(str(ROOT / "templates")),
        PrefixLoader({"govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja")}),
    ]
)
app.secret_key = os.environ["SECRET_KEY"]
app.permanent_session_lifetime = 3600


@app.context_processor
def inject_globals():
    return {"current_year": datetime.now().year}


def _books():
    with open(BOOKS_REPO / "books.yaml") as f:
        return yaml.safe_load(f)["books"]


@app.route("/robots.txt")
def robots():
    return "User-agent: *\nDisallow: /\n", 200, {"Content-Type": "text/plain"}


@app.before_request
def require_login():
    if request.endpoint in ("login", "robots", "static"):
        return
    if not session.get("authenticated"):
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form_error = None
    if request.method == "POST":
        if request.form.get("password") in os.environ["APP_PASSWORD"].split(","):
            session.permanent = True
            session["authenticated"] = True
            return redirect(url_for("index"))
        form_error = "Incorrect password."
    return render_template("login.jinja2", form_error=form_error)


def _calendar_urls():
    cid = os.environ["CALENDAR_ID"]
    ical_https = f"https://calendar.google.com/calendar/ical/{cid}%40group.calendar.google.com/public/basic.ics"
    return {
        "calendar_google_url": (
            f"https://calendar.google.com/calendar/r?cid={cid}@group.calendar.google.com"
        ),
        "calendar_outlook_url": (
            f"https://outlook.live.com/calendar/0/addfromweb?url={quote(ical_https)}"
        ),
        "calendar_webcal_url": (
            f"webcal://calendar.google.com/calendar/ical/{cid}%40group.calendar.google.com/public/basic.ics"
        ),
        "calendar_ical_https": ical_https,
    }


@app.route("/")
def index():
    return render_template(
        "index.jinja2",
        books=_books(),
        quote=random.choice(QUOTES),
        **_calendar_urls(),
    )


def _make_qr(data):
    buf = io.BytesIO()
    qrcode.make(data).save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/calendar/qr-apple.png")
def calendar_qr_apple():
    return _make_qr(_calendar_urls()["calendar_webcal_url"])


@app.route("/calendar/qr-web.png")
def calendar_qr_web():
    return _make_qr(_calendar_urls()["calendar_ical_https"])


@app.route("/download", methods=["POST"])
def download():
    mode = request.form.get("mode")
    book = next((b for b in _books() if b["mode"] == mode), None)
    if not book:
        return "Not found", 404
    output_path = ROOT / "output" / f"{book['mode']}.pdf"
    return send_file(
        str(output_path), as_attachment=True, download_name=f"{book['name']}.pdf"
    )


def _generate_pdfs_at_startup() -> None:
    if not BOOKS_REPO.exists():
        return
    output_dir = ROOT / "output"
    output_dir.mkdir(exist_ok=True)
    for mode in ("craft", "craft-dark", "ra", "ra-dark"):
        if not (output_dir / f"{mode}.pdf").exists():
            print(f"Generating {mode}...")
            build(mode)
    print("All books ready.")


_generate_pdfs_at_startup()


def main():
    app.run(debug=True, port=7607)
