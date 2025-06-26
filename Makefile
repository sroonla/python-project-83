PORT ?= 8000

hexlet-setup:
	docker build -t hexlet-app .

install:
	# Установка системных зависимостей
	sudo apt-get update
	sudo apt-get install -y libpq-dev python3-dev gcc
	# Установка Python-зависимостей
	uv sync

setup: install

dev:
	. .venv/bin/activate && uv run flask --debug --app page_analyzer:app run --host=0.0.0.0

start:
	. .venv/bin/activate && uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

render-start:
	.venv/bin/gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app