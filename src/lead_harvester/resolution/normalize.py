import re
from urllib.parse import urlparse

import phonenumbers

from ..extractors import SOCIAL_HOSTS

# Twitter's rebrand means the SAME account can be scraped/typed as either
# host -- folded to one canonical host so a re-scrape after the rebrand (or
# a manual entry using the old domain) still matches a contact already on
# file instead of creating a second one.
_SOCIAL_HOST_ALIASES = {"twitter.com": "x.com"}
# One canonical platform key per recognized host (ContactPoint.contact_type),
# derived from the same SOCIAL_HOSTS set extract_social_profiles already uses
# to recognize a link as a social profile in the first place -- one source of
# truth for "which hosts count", rather than a second list that can drift.
_SOCIAL_PLATFORM_BY_HOST = {
    _SOCIAL_HOST_ALIASES.get(host, host): _SOCIAL_HOST_ALIASES.get(host, host).removesuffix(".com")
    for host in SOCIAL_HOSTS
}


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


def normalize_website(url: str) -> str:
    """
    Cleans up a website URL for storage/display: strips surrounding
    whitespace, adds a scheme if missing, and lowercases the host. Unlike
    normalize_domain (a bare host used purely for blocking/matching), this
    deliberately keeps "www." and the full path/query/fragment -- it's a
    value a human or downstream consumer expects to actually resolve, not
    a matching key. canonical/merger.py's display_fields() makes the same
    call for already-source-shaped raw_payload values (and is NOT routed
    through this function -- see its own tests) since a connector's raw
    website value is already reasonably well-formed; this is for messier
    boundaries like a manually typed form field.
    """
    if not url:
        return ""

    candidate = url.strip()
    if not candidate:
        return ""
    if not candidate.startswith(("http://", "https://")):
        candidate = f"https://{candidate}"

    try:
        parsed = urlparse(candidate)
    except Exception as e:
        print(f"normalize_website failed for {url!r}: {e}")
        return url.strip()

    if not parsed.netloc:
        return url.strip()

    query = f"?{parsed.query}" if parsed.query else ""
    fragment = f"#{parsed.fragment}" if parsed.fragment else ""
    return f"{parsed.scheme}://{parsed.netloc.lower()}{parsed.path}{query}{fragment}"


def normalize_social_handle(url: str) -> str:
    """
    Normalizes a social profile URL to a stable matching/storage key:
    lowercased scheme+host+path, "www." stripped, twitter.com folded into
    its current x.com host, and any query string/fragment (tracking
    params, "?utm_source=...") dropped since they don't change which
    account the link points to. Whole-string lowercasing (not just the
    host) is deliberate: most platforms' handles are themselves
    case-insensitive, and collapsing case is what lets a re-scrape or a
    manually retyped link match a contact already on file.
    """
    if not url:
        return ""

    candidate = url.strip()
    if not candidate:
        return ""
    if not candidate.startswith(("http://", "https://")):
        candidate = f"https://{candidate}"

    try:
        parsed = urlparse(candidate)
    except Exception as e:
        print(f"normalize_social_handle failed for {url!r}: {e}")
        return url.strip().lower()

    if not parsed.netloc:
        return url.strip().lower()

    host = parsed.netloc.lower().removeprefix("www.")
    host = _SOCIAL_HOST_ALIASES.get(host, host)
    path = parsed.path.rstrip("/")
    return f"https://{host}{path}".lower()


def social_platform_for_host(url: str) -> str | None:
    """
    Maps a social profile URL to a short platform key ("linkedin",
    "instagram", "x", ...) suitable for ContactPoint.contact_type, or None
    if the host isn't one of extractors.SOCIAL_HOSTS' recognized platforms.
    """
    if not url:
        return None

    candidate = url.strip()
    if not candidate.startswith(("http://", "https://")):
        candidate = f"https://{candidate}"

    try:
        host = urlparse(candidate).netloc.lower().removeprefix("www.")
    except Exception:
        return None

    host = _SOCIAL_HOST_ALIASES.get(host, host)
    return _SOCIAL_PLATFORM_BY_HOST.get(host)
