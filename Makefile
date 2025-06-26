PORT ?= 8000

hexlet-setup:
	docker build -t hexlet-app .

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

setup:
    if [ -n "$$HEXLET_CI" ]; then \
        echo "Installing system dependencies for Hexlet CI"; \
        apt-get update && apt-get install -y libpq-dev; \
    fi
    uv sync