# Stage 1: clone lodge-books using a token passed as a build secret
FROM alpine/git AS books
RUN --mount=type=secret,id=lodge_books_token \
    git clone \
        "https://$(cat /run/secrets/lodge_books_token)@github.com/albertkolozsvari/lodge-books.git" \
        /lodge-books


# Stage 2: production image
FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY --from=books /lodge-books /lodge-books

# Install dependencies before copying source for better layer caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-sources --no-install-project

COPY src/ src/
COPY static/ static/
COPY templates/ templates/

RUN uv sync --frozen --no-dev --no-sources

CMD ["sh", "-c", "/app/.venv/bin/gunicorn my_lodge.app:app --bind 0.0.0.0:${PORT:-8000} --workers 2"]
