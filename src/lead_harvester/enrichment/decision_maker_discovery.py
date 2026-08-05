"""
Rule-based decision-maker name+role detection from a crawled page's
visible text -- see docs/ROADMAP.md module 6 ("Enrichment").

extractors.py::extract_page_identity already pulls a person's name (and,
as of this module, jobTitle) from JSON-LD `Person` structured data when a
page happens to carry it, but most small-business sites don't mark up
their leadership with JSON-LD at all -- the "Principal: Jane Doe" /
"Founded by John Smith, CEO" text sitting in plain page copy was
previously never looked at. This is that missing text-pattern fallback,
used by sources/web.py only when JSON-LD found no Person. Whichever name/
role either source finds gets threaded onto the phone/email ContactPoint
canonical/merger.py's WEBSITE branch also creates from the same page --
the same way a decision-maker's row already carries person_name/role for
AUTHORIZED_IMPORT contacts.

Known v1 limitation: text-pattern matching only (regex over one role
keyword adjacent to a capitalized name-shaped token run), matching this
codebase's other rule-based v1 detectors -- no NER/name-validation model,
so an unusual sentence shape can miss a real decision-maker.
"""

from __future__ import annotations

import re

_ROLE_KEYWORDS = (
    "Managing Director",
    "Head of School",
    "Principal",
    "Director",
    "Founder",
    "Owner",
    "Proprietor",
    "President",
    "Chairman",
    "Chairwoman",
    "CEO",
    "CFO",
    "COO",
    "Administrator",
    "Dean",
)

_ROLE_ALTERNATION = "|".join(re.escape(keyword) for keyword in _ROLE_KEYWORDS)
_NAME_TOKEN = r"[A-Z][a-zA-Z.'\-]+(?:\s+[A-Z][a-zA-Z.'\-]+){0,3}"

_ROLE_THEN_NAME = re.compile(rf"\b(?i:{_ROLE_ALTERNATION})\s*[:\-,]\s*({_NAME_TOKEN})\b")
_NAME_THEN_ROLE = re.compile(rf"\b({_NAME_TOKEN}),?\s+(?i:{_ROLE_ALTERNATION})\b")
# Separate keyword-only match to recover which role text was actually
# matched (the (?i:...) group above isn't capturing, by design, so the
# name group's index stays stable regardless of which alternative matched).
_ROLE_ONLY = re.compile(rf"(?i:{_ROLE_ALTERNATION})")


def discover_decision_maker(text: str) -> dict[str, str] | None:
    """
    Returns {"name": ..., "role": ...} for the first "<Role>: <Name>" or
    "<Name>, <Role>" pattern found in `text`, or None if neither matches.
    "<Role>: <Name>" is checked first since it's the less ambiguous
    ordering -- a role keyword can't be mistaken for the start of a name.
    """
    if not text:
        return None

    match = _ROLE_THEN_NAME.search(text)
    if match:
        role_match = _ROLE_ONLY.search(match.group(0))
        return {"name": match.group(1).strip(), "role": role_match.group(0) if role_match else ""}

    match = _NAME_THEN_ROLE.search(text)
    if match:
        role_match = _ROLE_ONLY.search(match.group(0))
        return {"name": match.group(1).strip(), "role": role_match.group(0) if role_match else ""}

    return None
