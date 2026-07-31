from __future__ import annotations

import csv
from collections.abc import Iterable
from pathlib import Path

from ..extractors import best_evidence, extract_emails, extract_phones
from ..models import Lead

ALIASES = {
    "source": ("source", "platform", "network"),
    "source_url": ("source_url", "profile_url", "url", "permalink"),
    "name": ("name", "display_name", "full_name", "username"),
    "organization": ("organization", "company", "business", "employer"),
    "title": ("title", "job_title", "headline", "role"),
    "email": ("email", "email_address"),
    "phone": ("phone", "phone_number", "mobile"),
    "website": ("website", "external_url", "domain"),
    "location": ("location", "city", "region"),
    "text": ("text", "bio", "description", "content", "post_text", "caption"),
}


def _value(row: dict[str, str], field: str) -> str:
    lower_row = {key.lower().strip(): (value or "").strip() for key, value in row.items()}
    for alias in ALIASES[field]:
        if lower_row.get(alias):
            return lower_row[alias]
    return ""


def load_social_csv(path: str, keywords: Iterable[str], intent_terms: Iterable[str]) -> list[Lead]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(path)

    leads: list[Lead] = []
    needles = [*keywords, *intent_terms]
    with file_path.open("r", newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            text = _value(row, "text")
            email = _value(row, "email") or next(iter(extract_emails(text)), "")
            phone = _value(row, "phone") or next(iter(extract_phones(text)), "")
            source_url = _value(row, "source_url")
            website = _value(row, "website")
            social_profiles = [source_url] if source_url else []
            leads.append(
                Lead(
                    source=_value(row, "source") or "social_csv",
                    source_url=source_url or website or f"social-csv:{len(leads) + 1}",
                    name=_value(row, "name"),
                    organization=_value(row, "organization"),
                    title=_value(row, "title"),
                    email=email,
                    phone=phone,
                    website=website,
                    location=_value(row, "location"),
                    social_profiles=social_profiles,
                    evidence=best_evidence(text, needles),
                    raw={key: value for key, value in row.items() if value},
                )
            )
    return leads
