PORT ?= 8000

hexlet-setup:
	chmod +x .hexlet/setup.sh
	.hexlet/setup.sh

setup:
	uv sync

install:
	uv sync

dev:
	. .venv/bin/activate && uv run flask --debug --app page_analyzer:app run --host=0.0.0.0

start:
	. .venv/bin/activate && uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

render-start:
	.venv/bin/gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app