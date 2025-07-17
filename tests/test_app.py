import pytest
import requests
from page_analyzer.db import get_url_checks, get_url_by_id

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Анализатор страниц' in response.text

def test_add_url(client):
    response = client.post('/urls', data={'url': 'https://example.com'})
    assert response.status_code == 302
    assert '/urls/' in response.location

def test_check_url(client):
    response = client.post('/urls', data={'url': 'https://example.com'})
    url_id = response.location.split('/')[-1]
    
    response = client.post(f'/urls/{url_id}/checks')
    assert response.status_code == 302
    assert response.location.endswith(f'/urls/{url_id}')

def test_add_invalid_url(client):
    response = client.post('/urls', data={'url': ''}, follow_redirects=True)
    assert response.status_code == 200
    assert 'Некорректный URL' in response.text
    
    response = client.post('/urls', data={'url': 'ftp://example.com'}, follow_redirects=True)
    assert 'Некорректный URL' in response.text
    
    long_url = 'https://' + 'a' * 300
    response = client.post('/urls', data={'url': long_url}, follow_redirects=True)
    assert 'Некорректный URL' in response.text

def test_add_existing_url(client):
    client.post('/urls', data={'url': 'https://example.com'})
    
    response = client.post('/urls', data={'url': 'https://example.com'}, follow_redirects=True)
    assert 'Страница уже существует' in response.text

def test_show_nonexistent_url(client):
    response = client.get('/urls/999999', follow_redirects=True)
    assert 'Страница не найдена' in response.text

def test_check_nonexistent_url(client):
    response = client.post('/urls/999999/checks', follow_redirects=True)
    assert 'Страница не найдена' in response.text

def test_check_url_timeout(client, monkeypatch):
    response = client.post('/urls', data={'url': 'https://example.com'})
    url_id = response.location.split('/')[-1]
    
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout("Test timeout")
    
    monkeypatch.setattr(requests, 'get', mock_get)
    
    client.post(f'/urls/{url_id}/checks')
    response = client.get(f'/urls/{url_id}', follow_redirects=True)
    assert 'Таймаут при проверке сайта' in response.text

def test_check_url_ssl_error(client, monkeypatch):
    response = client.post('/urls', data={'url': 'https://example.com'})
    url_id = response.location.split('/')[-1]
    
    def mock_get(*args, **kwargs):
        raise requests.exceptions.SSLError("Test SSL error")
    
    monkeypatch.setattr(requests, 'get', mock_get)
    
    client.post(f'/urls/{url_id}/checks')
    response = client.get(f'/urls/{url_id}', follow_redirects=True)
    assert 'Ошибка SSL сертификата' in response.text

def test_check_url_without_meta(client, monkeypatch):
    response = client.post('/urls', data={'url': 'https://example.com'})
    url_id = response.location.split('/')[-1]
    
    class MockResponse:
        status_code = 200
        text = "<html><title>Test</title><h1>Header</h1></html>"
        content = text.encode('utf-8')
    
    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: MockResponse())
    
    client.post(f'/urls/{url_id}/checks')
    
    checks = get_url_checks(int(url_id))
    assert len(checks) > 0
    assert checks[0]["h1"] == "Header"
    assert checks[0]["title"] == "Test"
    assert checks[0]["description"] is None

def test_add_url_db_error(client, monkeypatch):
    def mock_add_url(url):
        raise Exception("Database error")
    
    monkeypatch.setattr('page_analyzer.db.add_url', mock_add_url)
    
    response = client.post('/urls', data={'url': 'https://example.com'}, follow_redirects=True)
    assert 'Ошибка при добавлении страницы' in response.text