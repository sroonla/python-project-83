import requests
from bs4 import BeautifulSoup

def parse_page(url):
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/125.0.0.0 Safari/537.36'
        ),
        'Accept': (
            'text/html,application/xhtml+xml,application/xml;'
            'q=0.9,image/webp,*/*;q=0.8'
        ),
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    response = requests.get(
        url,
        headers=headers,
        timeout=10,
        allow_redirects=True
    )
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    h1_tag = soup.find('h1')
    h1 = h1_tag.text.strip() if h1_tag else None
    
    title_tag = soup.find('title')
    title = title_tag.text.strip() if title_tag else None
    
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    description = (
        meta_desc['content'].strip()
        if meta_desc and meta_desc.get('content')
        else None
    )
    
    if description and len(description) > 255:
        description = description[:252] + '...'
    
    return {
        'status_code': response.status_code,
        'h1': h1,
        'title': title,
        'description': description
    }