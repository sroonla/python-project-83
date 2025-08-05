import os
import pytest
from page_analyzer.app import app as flask_app
from page_analyzer.db import init_db, add_url

@pytest.fixture
def app():
    app = flask_app
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = "test_secret_key"

    with app.app_context():
        init_db()

    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_url(app):
    with app.app_context():
        url_id = add_url("https://example.com")
        return url_id