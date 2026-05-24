# my-lodge

A password-protected web app for St. Bartholomew Lodges. Members can download ritual books as PDFs and subscribe to the lodge calendar.

Built with Flask and the [GOV.UK Design System](https://design-system.service.gov.uk/), powered by [bookcraft](https://pypi.org/project/bookcraft/).

## Requirements

- [uv](https://docs.astral.sh/uv/)
- [lodge-books](https://github.com/albertkolozsvari/lodge-books) cloned as a sibling directory (`../lodge-books`)

## Setup

```bash
uv sync
cp .env.example .env
# fill in SECRET_KEY and APP_PASSWORD in .env
```

## Running locally

```bash
make serve
```

## Generating books

PDFs are written to `output/`. Requires `lodge-books` cloned as a sibling directory.

```bash
uv run craft        # Calver Craft Ritual, light theme
uv run craft-dark   # Calver Craft Ritual, dark theme
uv run ra           # Domatic Royal Arch Ritual, light theme
uv run ra-dark      # Domatic Royal Arch Ritual, dark theme
```

## Linting

```bash
uv run ruff check .
uv run ruff format --check .
uv run djlint templates/ --lint --extension jinja2
uv run ty check
```

## Structure

```
src/my_lodge/   # Flask app and CLI entry points
templates/      # Jinja2 templates (*.jinja2)
static/         # GOV.UK Frontend assets and logo
output/         # generated PDFs (gitignored)
```
