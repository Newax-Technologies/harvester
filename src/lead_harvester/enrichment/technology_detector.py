"""
Rule-based pain-point/buying-signal detection over a crawled website's
visible text -- see docs/ROADMAP.md module 6 ("Enrichment").

Revives the intent of the deleted intelligence/pain_detection.py (which
only ever operated on the dead Phase-1 entities/ dataclasses nothing
constructed -- see docs/CODE_REVIEW_LESSONS.md pattern 2), wired for real
this time: sources/web.py's crawler already extracts `text` per page but
had nowhere durable to put pattern-detected signals; this module is that
detection step, and pipeline.py materializes its output into real
models/signal.py Signal rows once a crawled page resolves to an
institution.

Known v1 limitation: text-pattern matching only (no HTML/DOM inspection,
so it can't detect e.g. a specific CMS/booking-widget by its markup) --
matches this codebase's other rule-based v1 scopes rather than a full
technology-fingerprinting service.
"""

from __future__ import annotations

# (trigger, suppressing_terms, message): flagged when `trigger` is present
# and NONE of `suppressing_terms` are -- the suppressing terms indicate the
# institution already has a real solution, so the pain point doesn't apply.
_SUPPRESSIBLE_PAIN_POINT_RULES: list[tuple[str, tuple[str, ...], str]] = [
    (
        "whatsapp",
        ("book now", "schedule", "portal", "parent portal"),
        "Uses WhatsApp for communication with no online booking/portal.",
    ),
]

# (trigger, required_context_terms, message): flagged when `trigger` is
# present AND at least one required-context term is also present -- the
# context terms narrow the trigger to the specific pain point (e.g. a
# Google Form used specifically for admissions, not just any form).
_CONTEXTUAL_PAIN_POINT_RULES: list[tuple[str, tuple[str, ...], str]] = [
    (
        "google form",
        ("admission", "enroll", "enrolment", "enrollment"),
        "Uses Google Forms for admissions instead of a dedicated system.",
    ),
]

_BUYING_SIGNAL_RULES: list[tuple[str, str]] = [
    ("now hiring", "Actively hiring -- may indicate growth/budget."),
    ("we're hiring", "Actively hiring -- may indicate growth/budget."),
    ("join our team", "Actively hiring -- may indicate growth/budget."),
    ("new campus", "Recently opened or announced a new campus/location."),
    ("grand opening", "Recently opened or announced a new campus/location."),
]

# docs/ROADMAP.md module 20: known LMS/portal names and phrases. A positive
# detection ("has an LMS") -- a fact, not a pain point or buying signal --
# so it's emitted as SignalType.TECHNOLOGY_PRESENT rather than either of the
# rule lists above. Per the module's decided absence-means-unavailable
# policy, the caller (service_gap.py) treats "no match" as "no LMS", not
# "unknown".
_LMS_SIGNAL_RULES: list[tuple[str, str]] = [
    ("moodle", "Uses Moodle as its learning management system."),
    ("google classroom", "Uses Google Classroom as its learning management system."),
    ("canvas lms", "Uses Canvas as its learning management system."),
    ("blackboard", "Uses Blackboard as its learning management system."),
    ("schoology", "Uses Schoology as its learning management system."),
    ("powerschool", "Uses PowerSchool as its learning management system."),
    ("parent portal", "Has a parent portal."),
    ("student portal", "Has a student portal."),
]


def detect_technology_signals(text: str) -> list[dict[str, str]]:
    """
    Returns a list of {"signal_type": "pain_point"|"buying_signal",
    "text": "..."} dicts detected from `text` (already-extracted visible
    page text, e.g. sources/web.py's `visible_text(html)`). Case-
    insensitive substring matching -- deliberately simple, matching this
    codebase's other v1 rule-based detection (see module docstring).
    """
    if not text:
        return []

    lowered = text.lower()
    seen: set[tuple[str, str]] = set()
    signals: list[dict[str, str]] = []

    def _add(signal_type: str, message: str) -> None:
        key = (signal_type, message)
        if key not in seen:
            seen.add(key)
            signals.append({"signal_type": signal_type, "text": message})

    for trigger, suppressing_terms, message in _SUPPRESSIBLE_PAIN_POINT_RULES:
        if trigger in lowered and not any(term in lowered for term in suppressing_terms):
            _add("pain_point", message)

    for trigger, required_context_terms, message in _CONTEXTUAL_PAIN_POINT_RULES:
        if trigger in lowered and any(term in lowered for term in required_context_terms):
            _add("pain_point", message)

    for trigger, message in _BUYING_SIGNAL_RULES:
        if trigger in lowered:
            _add("buying_signal", message)

    for trigger, message in _LMS_SIGNAL_RULES:
        if trigger in lowered:
            _add("technology_present", message)

    return signals
