from urllib.parse import urlparse
import validators

def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def is_valid_url(url):
    if not url:
        return False
    
    if len(url) > 255:
        return False
    
    if "localhost" in url or "127.0.0.1" in url:
        return True
    
    parsed = urlparse(url)
    if parsed.scheme not in ['http', 'https']:
        return False
    
    return validators.url(url)