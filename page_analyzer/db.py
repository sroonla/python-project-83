import os
import psycopg2
from dotenv import load_dotenv
from urllib.parse import urlparse
import validators

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def is_valid_url(url):
    return validators.url(url) and len(url) <= 255

def add_url(url):
    normalized_url = normalize_url(url)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO urls (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
                RETURNING id
            """, (normalized_url,))
            new_id = cur.fetchone()
            conn.commit()
            return new_id[0] if new_id else None

def get_url_by_id(url_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
            return cur.fetchone()

def get_url_by_name(url):
    normalized_url = normalize_url(url)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM urls WHERE name = %s", (normalized_url,))
            return cur.fetchone()

def get_all_urls():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT urls.id, urls.name, 
                       MAX(url_checks.created_at) AS last_check
                FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                GROUP BY urls.id, urls.name
                ORDER BY urls.id DESC
            """)
            return cur.fetchall()

def add_url_check(url_id, status_code):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO url_checks (url_id, status_code)
                VALUES (%s, %s)
            """, (url_id, status_code))
            conn.commit()

def get_url_checks(url_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, status_code, created_at 
                FROM url_checks 
                WHERE url_id = %s 
                ORDER BY created_at DESC
            """, (url_id,))
            return cur.fetchall()

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
            return cur.fetchall()