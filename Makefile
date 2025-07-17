PORT ?= 8000

install:
    pip install --upgrade pip
    pip install -r requirements.txt

test:
    pytest

coverage:
    coverage run --source=page_analyzer -m pytest
    coverage report

start:
    gunicorn -w 5 -b 0.0.0.0:$(PORT) wsgi:app

dev:
    flask --app page_analyzer.app run --host=0.0.0.0 --port=$(PORT) --debug