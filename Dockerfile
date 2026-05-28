FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY src/ src/
COPY static/ static/
COPY templates/ templates/

RUN uv sync --frozen --no-dev
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

# Pre-generate PDFs at build time so they are available immediately on startup.
# LODGE_BOOKS_TOKEN is automatically injected by Render from the existing env var.
# The entrypoint still clones lodge-books at runtime so books.yaml is available for the index page.
ARG LODGE_BOOKS_TOKEN
RUN git clone "https://x-access-token:${LODGE_BOOKS_TOKEN}@github.com/albertkol/lodge-books.git" /lodge-books && \
    mkdir -p /app/output && \
    /app/.venv/bin/python -c "from my_lodge.cli import build; [build(m) for m in ('craft', 'craft-dark', 'craft-2026-05', 'ra', 'ra-dark')]" && \
    rm -rf /lodge-books

ENTRYPOINT ["./entrypoint.sh"]
