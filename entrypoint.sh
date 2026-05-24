#!/bin/sh
set -e

git clone "https://x-access-token:${LODGE_BOOKS_TOKEN}@github.com/albertkol/lodge-books.git" /lodge-books

exec /app/.venv/bin/gunicorn my_lodge.app:app --bind "0.0.0.0:${PORT:-8000}" --workers 2 --timeout 300
