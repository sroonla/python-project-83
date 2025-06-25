import pytest
from page_analyzer.db import get_connection, normalize_url, is_valid_url

def test_db_connection():
    conn = get_connection()
    assert conn is not None
    conn.close()

def test_normalize_url():
    assert normalize_url("https://example.com/path") == "https://example.com"
    assert normalize_url("http://example.com:80") == "http://example.com:80"

def test_is_valid_url():
    assert is_valid_url("https://example.com") is True
    assert is_valid_url("not-a-url") is False