PORT ?= 8000

install:
	sudo apt-get update
	sudo apt-get install -y libpq-dev python3-dev gcc
	uv sync

dev:
	source .venv/bin/activate && flask --app page_analyzer.app run --host=0.0.0.0 --port=$(PORT) --debug

start:
	source .venv/bin/activate && gunicorn -w 5 -b 0.0.0.0:$(PORT) wsgi:app

render-start:
	.venv/bin/gunicorn -w 5 -b 0.0.0.0:$(PORT) wsgi:app