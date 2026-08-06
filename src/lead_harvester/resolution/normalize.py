import re
from urllib.parse import urlparse

import phonenumbers


def normalize_domain(url: str) -> str:
    """
    Strips http/https, www., and subpaths to return just the clean domain.

    Correction: bounded to 255 chars -- every column this value is ever
    written to (RawSourceRecord/RawPageSnapshot.normalized_domain,
    CanonicalInstitution.domain) is String(255). A malformed or
    adversarial URL's netloc (e.g. embedded userinfo, an
    unreasonably long host) can otherwise exceed that, turning a single
    bad seed URL into a flush-time "value too long" error that aborts an
    entire crawler run instead of just leaving that one page's domain
    unmatched.
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
        return domain[:255]
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


def normalize_website(url: str) -> str:
    """
    Canonicalizes a website URL for storage/display: adds a scheme only when
    missing (preserving an explicit http:// rather than forcing https://,
    since some institutions genuinely only serve http), lowercases the host,
    strips a leading "www.", and drops a bare trailing "/" -- so
    "WWW.Example.EDU/" and "https://example.edu" store identically instead
    of comparing as different values downstream (dedup, display, sync).
    Falls back to the original (unparseable) string rather than discarding
    it -- unlike normalize_domain, which is only ever used as a blocking key
    where an empty fallback is safe, this value is shown to users directly.
    """
    if not url:
        return ""

    original = url.strip()
    if not original:
        return ""

    has_scheme = original.startswith(("http://", "https://"))
    scheme_url = original if has_scheme else f"https://{original}"

    try:
        parsed = urlparse(scheme_url)
        host = parsed.netloc.lower().removeprefix("www.")
        if not host:
            return original
        path = parsed.path.rstrip("/")
        return parsed._replace(netloc=host, path=path).geturl()
    except Exception:
        return original


# Hosts extractors.SOCIAL_HOSTS also recognizes, mapped to the contact_type
# value stored on a ContactPoint for that platform -- kept in sync with that
# set by hand (same documented tradeoff resolution/blocking.py's
# _predicted_decision comment already accepts for its own duplicated logic).
_SOCIAL_PLATFORMS: dict[str, str] = {
    "linkedin.com": "linkedin",
    "instagram.com": "instagram",
    "facebook.com": "facebook",
    "x.com": "twitter",
    "twitter.com": "twitter",
    "youtube.com": "youtube",
    "tiktok.com": "tiktok",
    "reddit.com": "reddit",
}


def normalize_social_profile(url: str) -> tuple[str, str] | None:
    """
    Maps a social profile URL (as found by extractors.extract_social_profiles)
    to (contact_type, canonical_url), e.g.
    "https://www.facebook.com/SomePage/?ref=x" -> ("facebook",
    "https://facebook.com/SomePage"). Returns None for an unrecognized host,
    or for a bare platform homepage (no path beyond "/") -- that carries no
    institution-identifying handle, so it isn't worth a ContactPoint.
    """
    if not url:
        return None

    try:
        parsed = urlparse(url if "://" in url else f"https://{url}")
    except Exception:
        return None

    host = parsed.netloc.lower().removeprefix("www.")
    platform = next(
        (
            name
            for domain, name in _SOCIAL_PLATFORMS.items()
            if host == domain or host.endswith(f".{domain}")
        ),
        None,
    )
    if platform is None:
        return None

    path = parsed.path.rstrip("/")
    if not path:
        return None

    canonical = parsed._replace(netloc=host, path=path, query="", fragment="").geturl()
    return platform, canonical


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
