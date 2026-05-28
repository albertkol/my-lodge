#!/bin/sh
set -e

exec /app/.venv/bin/gunicorn my_lodge.app:app --bind "0.0.0.0:${PORT:-8000}" --workers 1 --timeout 600 --preload
