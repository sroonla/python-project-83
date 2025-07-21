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
    # Проверка пустого URL - ожидаем 422 без редиректа
    response = client.post('/urls', data={'url': ''})
    assert response.status_code == 422
    assert 'Некорректный URL' in response.text
    
    # Проверка невалидного протокола
    response = client.post('/urls', data={'url': 'ftp://example.com'})
    assert response.status_code == 422
    assert 'Некорректный URL' in response.text
    
    # Проверка длинного URL
    long_url = 'https://' + 'a' * 300
    response = client.post('/urls', data={'url': long_url})
    assert response.status_code == 422
    assert 'Некорректный URL' in response.text

def test_add_existing_url(client):
    # Первое добавление
    client.post('/urls', data={'url': 'https://example.com'})
    
    # Второе добавление того же URL
    response = client.post('/urls', data={'url': 'https://example.com'}, follow_redirects=True)
    assert response.status_code == 200
    assert 'Страница уже существует' in response.text

def test_show_nonexistent_url(client):
    response = client.get('/urls/999999', follow_redirects=True)
    assert response.status_code == 200
    assert 'Страница не найдена' in response.text

def test_check_nonexistent_url(client):
    response = client.post('/urls/999999/checks', follow_redirects=True)
    assert response.status_code == 200
    assert 'Страница не найдена' in response.text

def test_check_url_timeout(client, monkeypatch):
    # Добавляем URL
    response = client.post('/urls', data={'url': 'https://example.com'})
    url_id = response.location.split('/')[-1]
    
    # Мокаем requests.get для эмуляции таймаута
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout("Test timeout")
    
    monkeypatch.setattr(requests, 'get', mock_get)
    
    # Выполняем проверку
    client.post(f'/urls/{url_id}/checks')
    response = client.get(f'/urls/{url_id}', follow_redirects=True)
    assert response.status_code == 200
    assert 'Таймаут при проверке сайта' in response.text

def test_check_url_ssl_error(client, monkeypatch):
    # Добавляем URL
    response = client.post('/urls', data={'url': 'https://example.com'})
    url_id = response.location.split('/')[-1]
    
    # Мокаем requests.get для эмуляции SSL ошибки
    def mock_get(*args, **kwargs):
        raise requests.exceptions.SSLError("Test SSL error")
    
    monkeypatch.setattr(requests, 'get', mock_get)
    
    # Выполняем проверку
    client.post(f'/urls/{url_id}/checks')
    response = client.get(f'/urls/{url_id}', follow_redirects=True)
    assert response.status_code == 200
    assert 'Ошибка SSL сертификата' in response.text

def test_check_url_without_meta(client, monkeypatch):
    # Добавляем URL
    response = client.post('/urls', data={'url': 'https://example.com'})
    url_id = response.location.split('/')[-1]
    
    # Мокаем ответ сервера
    class MockResponse:
        status_code = 200
        text = "<html><title>Test</title><h1>Header</h1></html>"
        content = text.encode('utf-8')
        history = []  # Добавляем для обработки редиректов
    
    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: MockResponse())
    
    # Выполняем проверку
    client.post(f'/urls/{url_id}/checks')
    
    # Получаем проверки
    checks = get_url_checks(int(url_id))
    assert len(checks) > 0
    assert checks[0]["h1"] == "Header"
    assert checks[0]["title"] == "Test"
    assert checks[0]["description"] is None

def test_add_url_db_error(client, monkeypatch):
    # Мокаем функцию добавления URL
    def mock_add_url(url):
        raise Exception("Database error")
    
    monkeypatch.setattr('page_analyzer.db.add_url', mock_add_url)
    
    # Пытаемся добавить URL
    response = client.post(
        '/urls',
        data={'url': 'https://example.com'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert 'Ошибка при добавлении страницы' in response.text