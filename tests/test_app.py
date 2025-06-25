def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Анализатор страниц' in response.data.decode('utf-8')

def test_add_url(client):
    response = client.post('/urls', data={'url': 'https://example.com'})
    assert response.status_code == 302
    assert '/urls/' in response.location

def test_check_url(client):
    client.post('/urls', data={'url': 'https://example.com'})
    
    response = client.post('/urls/1/checks')
    assert response.status_code == 302
    assert response.location.endswith('/urls/1')