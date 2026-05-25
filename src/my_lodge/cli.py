from pathlib import Path

from bookcraft import generate as _generate

ROOT = Path(__file__).resolve().parent.parent.parent
BOOKS_REPO = ROOT.parent / "lodge-books"

MODES = {
    "craft": ("craft.yaml", "c-keywords.yaml", "craft"),
    "craft-dark": ("craft-dark.yaml", "c-keywords.yaml", "craft-dark"),
    "craft-2026-05": ("craft-2026-05.yaml", "c-keywords.yaml", "craft"),
    "ra": ("ra.yaml", "ra-keywords.yaml", "ra"),
    "ra-dark": ("ra-dark.yaml", "ra-keywords.yaml", "ra-dark"),
}


def generate_book(config: str, keywords: str, mode: str, output_name: str) -> Path:
    output_path = ROOT / "output" / f"{output_name}.pdf"
    output_path.parent.mkdir(exist_ok=True)
    _generate(
        books_path=str(BOOKS_REPO) + "/",
        settings_path=str(BOOKS_REPO / config),
        fonts_path=str(BOOKS_REPO / "config" / "fonts.yaml"),
        keywords_path=str(BOOKS_REPO / keywords),
        output_path=str(output_path),
        mode=mode,
    )
    return output_path


def build(mode: str) -> None:
    settings, keywords, bookcraft_mode = MODES[mode]
    generate_book(
        config=f"config/{settings}",
        keywords=f"config/{keywords}",
        mode=bookcraft_mode,
        output_name=mode,
    )


def craft():
    build("craft")


def craft_2026_05():
    build("craft-2026-05")


def craft_dark():
    build("craft-dark")


def ra():
    build("ra")


def ra_dark():
    build("ra-dark")
