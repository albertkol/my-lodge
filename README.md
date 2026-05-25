# my-lodge

A password-protected web app for St. Bartholomew Lodges. Members can download ritual books as PDFs and subscribe to the lodge calendar.

Built with Flask and the [GOV.UK Design System](https://design-system.service.gov.uk/), powered by [bookcraft](https://pypi.org/project/bookcraft/).

## Requirements

- [uv](https://docs.astral.sh/uv/)
- [lodge-books](https://github.com/albertkol/lodge-books) cloned as a sibling directory (`../lodge-books`)

## Setup

```bash
uv sync
cp .env.example .env
# fill in SECRET_KEY, APP_PASSWORD, CALENDAR_ID, and LODGE_BOOKS_TOKEN in .env
```

## Running locally

```bash
make serve
```

## Generating books

PDFs are written to `output/`. Requires `lodge-books` cloned as a sibling directory.

```bash
make craft          # Calver Craft Ritual, light theme
make craft-dark     # Calver Craft Ritual, dark theme
make craft-2026-05  # Calver Craft Ritual, GH Edition 2026-05
make ra             # Domatic Royal Arch Ritual, light theme
make ra-dark        # Domatic Royal Arch Ritual, dark theme
```

On the server, PDFs are generated automatically in the background at startup.

## Linting

```bash
uv run ruff check .
uv run ruff format --check .
uv run djlint templates/ --lint --extension jinja2
uv run ty check
```

## Deployment

Deployed on [Render](https://render.com/) via Docker. Pushes to `main` trigger CI; if lint passes, the deploy hook is called automatically.

## Structure

```
src/my_lodge/   # Flask app and CLI entry points
templates/      # Jinja2 templates (*.jinja2)
static/         # GOV.UK Frontend assets and logo
output/         # generated PDFs (gitignored)
```
