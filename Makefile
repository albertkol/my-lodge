serve:
	set -a && . ./.env && set +a && uv run serve

install-fe:
	npm install && npm run install-fe

craft:
	uv run craft

craft-dark:
	uv run craft-dark

craft-2026-05:
	uv run craft-2026-05

ra:
	uv run ra

ra-dark:
	uv run ra-dark
