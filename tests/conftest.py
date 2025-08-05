import os
import pytest
from page_analyzer.app import app as flask_app
from page_analyzer.db import init_db, get_connection, add_url

@pytest.fixture
def app():
    app = flask_app
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = "test_secret_key"
    app.config['DATABASE_URL'] = os.getenv("TEST_DATABASE_URL", os.getenv("DATABASE_URL"))
    return app

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    init_db()

@pytest.fixture
def client(app):
    with app.app_context():
        init_db()
    return app.test_client()

@pytest.fixture
def test_url(app):
    with app.app_context():
        url_id = add_url("https://example.com")
        return url_id