import re
from urllib.parse import urlparse

import phonenumbers


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
        domain = domain.removeprefix("www.")
        return domain
    except Exception as e:
        print(f"normalize_domain failed for {url!r}: {e}")
        return ""


def normalize_phone(phone: str, default_region: str | None = None) -> str:
    """
    Normalizes to E.164 (e.g. "+923001234567") via the phonenumbers library,
    so the SAME physical number normalizes identically whether it was
    entered/reported in national format ("0300 1234567") or international
    format ("+92 300 1234567") -- a real, live mismatch: manual leads
    commonly use the "+"-prefixed form while Google Places' own
    nationalPhoneNumber field never includes one, so exact-match phone
    blocking silently missed a manual lead and its matching scraped record
    for the same institution.

    default_region is an ISO-2 country hint (e.g. "PK") used only when the
    input has no explicit "+" country code of its own -- without a region
    hint AND no "+", a bare national-format number is genuinely ambiguous
    and this falls back to the old strip-to-digits behavior rather than
    guessing a country.
    """
    if not phone:
        return ""

    try:
        parsed = phonenumbers.parse(phone, default_region)
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        pass

    # Not parseable as a real number (invalid, or ambiguous without a
    # region hint) -- fall back to a best-effort digits/plus-only string
    # rather than dropping the value entirely.
    return re.sub(r"[^\d+]", "", phone)


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


def normalize_city(city: str) -> str:
    """
    Lowercases and normalizes whitespace/punctuation for city-name
    comparison -- same shape as normalize_name, kept separate so a future
    city-specific rule (e.g. alias resolution) doesn't have to piggyback
    on person/institution name normalization.
    """
    if not city:
        return ""

    city = city.lower()
    city = re.sub(r"[,.\-&_]", " ", city)
    city = re.sub(r"\s+", " ", city).strip()
    return city


# Common country names/aliases -> ISO 3166-1 alpha-2, keyed by
# normalize_name(name). Not an exhaustive ISO-3166 list -- known v1
# limitation, covers the countries this system's actual usage has hit
# (South Asia/Middle East/major English-speaking markets) rather than all
# ~195. An unrecognized name returns None so a caller can fall back to a
# configured default instead of silently guessing.
_COUNTRY_ALIASES: dict[str, str] = {
    "pakistan": "PK",
    "india": "IN",
    "bangladesh": "BD",
    "sri lanka": "LK",
    "nepal": "NP",
    "afghanistan": "AF",
    "united arab emirates": "AE",
    "uae": "AE",
    "saudi arabia": "SA",
    "qatar": "QA",
    "kuwait": "KW",
    "bahrain": "BH",
    "oman": "OM",
    "united states": "US",
    "united states of america": "US",
    "usa": "US",
    "united kingdom": "GB",
    "uk": "GB",
    "great britain": "GB",
    "canada": "CA",
    "australia": "AU",
    "new zealand": "NZ",
    "china": "CN",
    "japan": "JP",
    "south korea": "KR",
    "singapore": "SG",
    "malaysia": "MY",
    "indonesia": "ID",
    "thailand": "TH",
    "vietnam": "VN",
    "philippines": "PH",
    "germany": "DE",
    "france": "FR",
    "italy": "IT",
    "spain": "ES",
    "netherlands": "NL",
    "belgium": "BE",
    "switzerland": "CH",
    "sweden": "SE",
    "norway": "NO",
    "denmark": "DK",
    "ireland": "IE",
    "turkey": "TR",
    "egypt": "EG",
    "south africa": "ZA",
    "nigeria": "NG",
    "kenya": "KE",
    "brazil": "BR",
    "mexico": "MX",
    "argentina": "AR",
    "russia": "RU",
}


def country_to_iso2(country: str) -> str | None:
    """
    Maps a free-text country name (or an already-valid ISO-3166-1
    alpha-2 code) to its ISO-2 code. Returns None for anything
    unrecognized rather than guessing -- see _COUNTRY_ALIASES' own
    docstring for this table's known coverage limitation.
    """
    if not country:
        return None

    stripped = country.strip()
    if len(stripped) == 2 and stripped.isalpha():
        return stripped.upper()

    return _COUNTRY_ALIASES.get(normalize_name(stripped))
