import os
import pytest
import psycopg2
from pathlib import Path
from page_analyzer.app import app as flask_app
from page_analyzer.db import init_db, add_url

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_PATH = BASE_DIR / 'database.sql'

print(f"SQL_PATH: {SQL_PATH}")
print(f"File exists: {SQL_PATH.exists()}")


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


@pytest.fixture(scope='session', autouse=True)
def setup_test_database():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        pytest.skip("DATABASE_URL not set")
    
    with open(SQL_PATH, 'r') as f:
        sql = f.read()
    
    conn = psycopg2.connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    finally:
        conn.close()