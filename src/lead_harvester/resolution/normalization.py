import re


def normalize_phone(phone: str) -> str:
    # Remove all non-numeric characters except +
    cleaned = re.sub(r"[^\d+]", "", phone)
    if cleaned.startswith("00"):
        cleaned = "+" + cleaned[2:]
    # Basic normalization, ideally should use phonenumbers library
    return cleaned


def normalize_url(url: str) -> str:
    url = url.strip().lower()
    url = url.removesuffix("/")
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]
    url = url.removeprefix("www.")
    return url


def normalize_institution_name(name: str) -> str:
    name = name.lower()
    # Remove common punctuation
    name = re.sub(r"[^\w\s]", "", name)
    # Remove common suffixes for normalization comparison
    suffixes = [r"\bacademy\b", r"\bschool\b", r"\bcollege\b", r"\binstitute\b"]
    for suffix in suffixes:
        name = re.sub(suffix, "", name)
    return " ".join(name.split())
