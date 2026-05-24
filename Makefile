serve:
	set -a && . ./.env && set +a && uv run serve

install-fe:
	npm install && npm run install-fe

craft:
	uv run --no-sources craft

craft-dark:
	uv run --no-sources craft-dark

ra:
	uv run --no-sources ra

ra-dark:
	uv run --no-sources ra-dark

local-craft:
	uv run craft

local-craft-dark:
	uv run craft-dark

local-ra:
	uv run ra

local-ra-dark:
	uv run ra-dark
