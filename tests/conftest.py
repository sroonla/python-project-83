import os
import pytest
from page_analyzer.app import app as flask_app
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "DATABASE_URL": os.getenv('TEST_DATABASE_URL', 'postgresql://test_user:test_pass@localhost/test_db')
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()