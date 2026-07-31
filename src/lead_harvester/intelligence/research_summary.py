"""
Composes a human-readable summary from detected Signal evidence -- see
docs/ROADMAP.md module 7's research_summary sub-concern.

services/lead_profile_service.py::refresh_lead_profile already prefers an
AI-generated summary (intelligence/researcher.py's LinkedIn-only "summary"
ResearchFinding) when one exists. This module is the fallback for every
institution that has no AI summary but DOES have real Signal evidence
(e.g. a website-crawled institution enriched by
enrichment/technology_detector.py, or a Google/Yandex/Apple Maps place
with no LinkedIn profile ever researched) -- previously that fallback was
a static "No AI research summary yet." with no mention of real detected
evidence sitting right there in the Signal table.
"""

from __future__ import annotations

from lead_harvester.models.signal import Signal, SignalType


def summarize_signals(signals: list[Signal]) -> str:
    """
    Returns "" when there's nothing to summarize (caller falls back to a
    generic institution description) -- never a hardcoded placeholder
    string, so a caller can tell "no signals" apart from "summarized".
    """
    pain_points = [s.signal_text for s in signals if s.signal_type == SignalType.PAIN_POINT]
    buying_signals = [s.signal_text for s in signals if s.signal_type == SignalType.BUYING_SIGNAL]

    if not pain_points and not buying_signals:
        return ""

    parts: list[str] = []
    if pain_points:
        noun = "pain point" if len(pain_points) == 1 else "pain points"
        parts.append(f"{len(pain_points)} {noun} detected: {'; '.join(pain_points)}.")
    if buying_signals:
        noun = "buying signal" if len(buying_signals) == 1 else "buying signals"
        parts.append(f"{len(buying_signals)} {noun}: {'; '.join(buying_signals)}.")

    return " ".join(parts)
