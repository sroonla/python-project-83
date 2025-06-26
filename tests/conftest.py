import os
import pytest
from page_analyzer.db import get_connection

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Создает тестовую БД и применяет миграции"""
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        pytest.skip("DATABASE_URL not set, skipping database setup")
        return

    try:
        conn = get_connection(db_url)
        cur = conn.cursor()
        
        with open('database.sql', 'r') as f:
            sql_script = f.read()
            
            commands = sql_script.split(';')
            for command in commands:
                if command.strip():
                    cur.execute(command)
        
        conn.commit()
    except Exception as e:
        pytest.fail(f"Database setup failed: {str(e)}")
    finally:
        if conn:
            conn.close()