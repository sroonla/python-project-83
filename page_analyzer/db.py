import os
import psycopg2
from dotenv import load_dotenv
from urllib.parse import urlparse
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def is_valid_url(url):
    if not url:
        return False
    if len(url) > 255:
        return False
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        return False
    if not parsed.netloc:
        return False
    return True


def add_url(url):
    normalized_url = normalize_url(url)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s)
                ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name
                RETURNING id
            """, (normalized_url, datetime.now()))
            result = cur.fetchone()
            conn.commit()
            return result[0] if result else None


def get_url_by_id(url_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
            row = cur.fetchone()
            if row:
                return {"id": row[0], "name": row[1], "created_at": row[2]}
            return None


def get_url_by_name(url):
    normalized_url = normalize_url(url)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM urls WHERE name = %s", (normalized_url,))
            row = cur.fetchone()
            if row:
                return {"id": row[0], "name": row[1], "created_at": row[2]}
            return None


def add_url_check(url_id, status_code, h1=None, title=None, description=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO url_checks (
                    url_id, 
                    status_code, 
                    h1, 
                    title, 
                    description,
                    created_at
                ) VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (url_id, status_code, h1, title, description, datetime.now()))
            result = cur.fetchone()
            conn.commit()
            return result[0] if result else None


def get_url_checks(url_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    id, 
                    status_code, 
                    created_at, 
                    h1,
                    title, 
                    description
                FROM url_checks 
                WHERE url_id = %s 
                ORDER BY created_at DESC
            """, (url_id,))
            return [
                {
                    "id": row[0],
                    "status_code": row[1],
                    "created_at": row[2],
                    "h1": row[3],
                    "title": row[4],
                    "description": row[5]
                }
                for row in cur.fetchall()
            ]


def get_all_urls():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    u.id, 
                    u.name, 
                    MAX(uc.created_at) AS last_check,
                    (SELECT status_code 
                     FROM url_checks 
                     WHERE url_id = u.id 
                     ORDER BY created_at DESC 
                     LIMIT 1) AS last_status
                FROM urls u
                LEFT JOIN url_checks uc ON u.id = uc.url_id
                GROUP BY u.id, u.name
                ORDER BY u.id DESC
            """)
            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "last_check": row[2],
                    "last_status": row[3]
                }
                for row in cur.fetchall()
            ]
        
        
def init_db():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS url_checks (
                    id SERIAL PRIMARY KEY,
                    url_id INTEGER NOT NULL REFERENCES urls(id),
                    status_code INTEGER,
                    h1 VARCHAR(255),
                    title VARCHAR(255),
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
    except psycopg2.errors.DuplicateTable:
        conn.rollback()
        print("Tables already exist, skipping creation")
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("Tables already exist, skipping creation")
    finally:
        conn.close()