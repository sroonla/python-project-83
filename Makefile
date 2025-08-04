PORT ?= 8000

install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run --host=0.0.0.0 --port=$(PORT)

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	uv run ruff check page_analyzer tests

fix-lint:
	uv run ruff check --fix page_analyzer tests

test:
	PYTHONPATH=$(PWD) uv run pytest -vv

test-coverage:
	uv run pytest --cov=page_analyzer --cov-report xml

check: test lint

.PHONY: install dev start build render-start lint fix-lint test test-coverage check