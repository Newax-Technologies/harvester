from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d{1,3}[\s.\-()]*)?(?:\d[\s.\-()]*){7,14}\d(?!\d)")
SOCIAL_HOSTS = {
    "linkedin.com",
    "instagram.com",
    "facebook.com",
    "x.com",
    "twitter.com",
    "youtube.com",
    "tiktok.com",
    "reddit.com",
}
CONTACT_HINTS = ("contact", "about", "team", "company", "services", "clinic", "staff")


def normalize_space(value: str) -> str:
    return " ".join(value.split())


def visible_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for node in soup(["script", "style", "noscript", "svg", "template"]):
        node.decompose()
    return normalize_space(soup.get_text(" ", strip=True))


def _clean_email(email: str) -> str:
    return email.strip(".,;:()[]{}<>\"'").lower()


def extract_emails(text: str, html: str = "") -> list[str]:
    values = {_clean_email(item) for item in EMAIL_RE.findall(f"{text} {html}")}
    blocked_suffixes = (".png", ".jpg", ".jpeg", ".webp", ".svg")
    return sorted(value for value in values if not value.endswith(blocked_suffixes))


def _normalize_phone(phone: str) -> str:
    phone = normalize_space(phone).strip(".,;:")
    digits = re.sub(r"\D", "", phone)
    if len(digits) < 8 or len(digits) > 15:
        return ""
    if phone.startswith("+"):
        return "+" + digits
    return digits


def extract_phones(text: str) -> list[str]:
    phones = {_normalize_phone(item) for item in PHONE_RE.findall(text)}
    return sorted(phone for phone in phones if phone)


def extract_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href", "").strip()
        if not href or href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        absolute = urljoin(base_url, href)
        parsed = urlparse(absolute)
        if parsed.scheme not in {"http", "https"}:
            continue
        links.add(parsed._replace(fragment="").geturl())
    return sorted(links)


def extract_social_profiles(links: list[str]) -> list[str]:
    profiles: set[str] = set()
    for link in links:
        host = urlparse(link).netloc.lower().removeprefix("www.")
        if any(host == domain or host.endswith(f".{domain}") for domain in SOCIAL_HOSTS):
            profiles.add(link.rstrip("/"))
    return sorted(profiles)


def candidate_internal_links(links: list[str], base_url: str) -> list[str]:
    base_host = urlparse(base_url).netloc.lower().removeprefix("www.")
    ranked: list[tuple[int, str]] = []
    for link in links:
        parsed = urlparse(link)
        host = parsed.netloc.lower().removeprefix("www.")
        if host != base_host:
            continue
        lowered = parsed.path.lower()
        priority = 0 if any(hint in lowered for hint in CONTACT_HINTS) else 1
        ranked.append((priority, link))
    return [link for _, link in sorted(ranked, key=lambda item: (item[0], item[1]))]


def _meta_content(soup: BeautifulSoup, *selectors: tuple[str, str]) -> str:
    for attr, value in selectors:
        tag = soup.find("meta", attrs={attr: value})
        if tag and tag.get("content"):
            return normalize_space(str(tag["content"]))
    return ""


def _json_ld_objects(soup: BeautifulSoup) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            value = json.loads(script.string or "")
        except (TypeError, json.JSONDecodeError):
            continue
        if isinstance(value, dict):
            graph = value.get("@graph")
            if isinstance(graph, list):
                objects.extend(item for item in graph if isinstance(item, dict))
            objects.append(value)
        elif isinstance(value, list):
            objects.extend(item for item in value if isinstance(item, dict))
    return objects


def extract_page_identity(html: str, url: str) -> dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    title = normalize_space(soup.title.get_text(" ", strip=True)) if soup.title else ""
    site_name = _meta_content(soup, ("property", "og:site_name"), ("name", "application-name"))
    description = _meta_content(
        soup,
        ("name", "description"),
        ("property", "og:description"),
    )
    organization = site_name
    name = ""
    role = ""
    location = ""
    address_locality = ""
    address_country = ""

    for item in _json_ld_objects(soup):
        item_type = item.get("@type", "")
        types = {item_type} if isinstance(item_type, str) else set(item_type or [])
        if not organization and types.intersection(
            {
                "Organization",
                "LocalBusiness",
                "Corporation",
                "MedicalBusiness",
                "ProfessionalService",
            }
        ):
            organization = normalize_space(str(item.get("name", "")))
        if not name and "Person" in types:
            name = normalize_space(str(item.get("name", "")))
            role = normalize_space(str(item.get("jobTitle", "")))
        if not location:
            address = item.get("address")
            if isinstance(address, dict):
                address_locality = normalize_space(str(address.get("addressLocality", "")))
                address_country = normalize_space(str(address.get("addressCountry", "")))
                parts = [
                    address_locality,
                    normalize_space(str(address.get("addressRegion", ""))),
                    address_country,
                ]
                location = ", ".join(part for part in parts if part)

    if not organization:
        organization = title.split("|")[0].split("-")[0].strip()
    if not organization:
        organization = urlparse(url).netloc.removeprefix("www.")

    return {
        "name": name,
        "role": role,
        "organization": organization,
        "title": title,
        "description": description,
        "location": location,
        "address_locality": address_locality,
        "address_country": address_country,
    }


def best_evidence(text: str, needles: list[str], max_length: int = 320) -> str:
    if not text:
        return ""
    lowered = text.lower()
    positions = [
        lowered.find(needle.lower()) for needle in needles if needle and needle.lower() in lowered
    ]
    center = min((position for position in positions if position >= 0), default=0)
    start = max(0, center - max_length // 3)
    excerpt = text[start : start + max_length]
    return normalize_space(excerpt)
