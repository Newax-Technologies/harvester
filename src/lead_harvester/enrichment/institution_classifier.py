"""
Rule-based institution_type classification from a crawled page's
organization name + meta description -- see docs/ROADMAP.md module 6
("Enrichment").

canonical/merger.py's WEBSITE branch of display_fields has never supplied
an institution_type at all (always "") -- unlike GOOGLE_PLACES/YANDEX/
MANUAL/AUTHORIZED_IMPORT -- which means a web-crawled-only institution can
never auto-classify into a Sector (services/sector_service.py, module 16),
since that match is keyed on institution_type. This is the missing
classification step: same keyword-substring style intelligence/taxonomy.py
already uses for education sub-categories, but covering the concrete
institution_type values docs/ROADMAP.md's module 16 seed list actually
uses across every seeded sector, not just education.

Rules are ordered so a more specific type (e.g. "dental_clinic") is
checked before the generic type it would otherwise also match ("clinic").
"""

from __future__ import annotations

_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("dental_clinic", ("dental clinic", "dentist", "dental care")),
    (
        "diagnostic_lab",
        (
            "diagnostic lab",
            "diagnostic center",
            "diagnostic centre",
            "medical laboratory",
            "pathology lab",
        ),
    ),
    ("pharmacy", ("pharmacy", "chemist")),
    ("hospital", ("hospital",)),
    ("clinic", ("clinic", "medical center", "medical centre")),
    ("university", ("university",)),
    ("college", ("college",)),
    ("academy", ("academy",)),
    ("school", ("school",)),
    ("law_firm", ("law firm", "attorneys", "advocates & legal", "advocates and legal")),
    ("legal_services", ("legal services", "legal consultancy")),
    (
        "accounting_firm",
        ("accounting firm", "chartered accountants", "chartered accountant", "cpa firm"),
    ),
    ("financial_advisory", ("financial advisory", "financial advisors", "financial advisers")),
    ("insurance_agency", ("insurance agency", "insurance company", "insurance brokers")),
    ("bank", ("bank",)),
    ("freight_forwarder", ("freight forwarder", "freight forwarding")),
    ("courier_service", ("courier service", "courier company")),
    ("logistics_company", ("logistics",)),
    ("transport_company", ("transport company", "transportation company")),
    ("property_developer", ("property developer", "real estate developer")),
    ("real_estate_agency", ("real estate agency", "real estate agents", "realtor")),
    ("supermarket", ("supermarket", "grocery store")),
    ("boutique", ("boutique",)),
    ("showroom", ("showroom",)),
    ("retail_store", ("retail store",)),
    ("event_venue", ("event venue", "banquet hall", "wedding venue")),
    ("hotel", ("hotel",)),
    ("restaurant", ("restaurant",)),
]


def classify_institution_type(name: str, description: str = "") -> str:
    """
    Returns the first institution_type whose keyword(s) substring-match
    `name`/`description` (case-insensitive), checked in the order above
    (more specific types first). Returns "" -- not a guess -- when nothing
    matches, matching every other source_type's own display_fields branch
    when its raw payload genuinely doesn't declare a type.
    """
    haystack = f"{name} {description}".lower()
    if not haystack.strip():
        return ""
    for institution_type, keywords in _RULES:
        if any(keyword in haystack for keyword in keywords):
            return institution_type
    return ""
