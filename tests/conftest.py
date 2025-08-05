import os
import pytest
from page_analyzer.app import app as flask_app
from page_analyzer.db import get_connection
from page_analyzer.db import add_url

@pytest.fixture
def app():
    app = flask_app
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = "test_secret_key"
    return app

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        pytest.skip("DATABASE_URL not set, skipping database setup")
        return

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    possible_paths = [
        os.path.join(project_root, 'database.sql'),
        '/project/database.sql',
        '/app/database.sql'
    ]
    
    db_sql_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_sql_path = path
            break
    
    if not db_sql_path:
        pytest.fail(f"database.sql not found. Checked paths: {possible_paths}")
        return

    print(f"Using database.sql at: {db_sql_path}")
    
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        with open(db_sql_path, 'r') as f:
            sql_script = f.read()
            
            commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]
            print(f"Found {len(commands)} SQL commands to execute")
            
            for i, command in enumerate(commands, 1):
                print(f"Executing command #{i}: {command[:50]}...")
                cur.execute(command)
        
        conn.commit()
        print("Database schema initialized successfully")
    except Exception as e:
        pytest.fail(f"Database setup failed: {str(e)}")
    finally:
        if conn:
            conn.close()

@pytest.fixture
def client(app):
    return app.test_client()

def test_url(app):
    with app.app_context():
        url_id = add_url("https://example.com")
        return url_id