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
    
    if not validators.url(url):
        return False
    
    return True