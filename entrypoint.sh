#!/bin/sh
set -e

git clone "https://x-access-token:${LODGE_BOOKS_TOKEN}@github.com/albertkol/lodge-books.git" /lodge-books

/app/.venv/bin/python -c "
from my_lodge.cli import build
for mode in ('craft', 'craft-dark', 'ra', 'ra-dark'):
    print(f'Generating {mode}...')
    build(mode)
print('All books generated.')
"

exec /app/.venv/bin/gunicorn my_lodge.app:app --bind "0.0.0.0:${PORT:-8000}" --workers 2 --timeout 120
