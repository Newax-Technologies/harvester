import re
from urllib.parse import urlparse

def normalize_domain(url: str) -> str:
    """
    Strips http/https, www., and subpaths to return just the clean domain.
    """
    if not url:
        return ""
    
    # Ensure URL has a scheme so urlparse works correctly
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
        
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
        return ""


def normalize_phone(phone: str) -> str:
    """
    Strips all non-digit characters. 
    If E.164 formatting is desired, we can add a country code prefix if missing.
    """
    if not phone:
        return ""
    
    # Extract only digits and the plus sign
    cleaned = re.sub(r"[^\d+]", "", phone)
    return cleaned


def normalize_name(name: str) -> str:
    """
    Lowercases and removes extra whitespace/punctuation for fuzzy matching.
    """
    if not name:
        return ""
    
    name = name.lower()
    # Replace common punctuation with space
    name = re.sub(r"[,.\-&_]", " ", name)
    # Collapse multiple spaces
    name = re.sub(r"\s+", " ", name).strip()
    return name


def normalize_address(address: str) -> str:
    """
    Lowercases and normalizes whitespace for basic address comparison.
    """
    if not address:
        return ""
    
    address = address.lower()
    address = re.sub(r"[,.\-]", " ", address)
    address = re.sub(r"\s+", " ", address).strip()
    return address
