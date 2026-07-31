"""
Computes a 0-100 "operational maturity" score for an institution -- see
docs/ROADMAP.md module 7's operational_maturity sub-concern.

Distinct from profiles/scoring.py's lead score (which measures how good a
SALES opportunity this institution is): this measures how digitally/
operationally mature the institution's own operations look, purely from
detected Signal evidence (models/signal.py, populated by both
enrichment/technology_detector.py's rule-based website detection and
intelligence/researcher.py's AI-driven LinkedIn analysis) plus whether it
has a website at all. A pain-point-heavy institution (e.g. WhatsApp-only
booking, Google-Forms admissions) scores LOW maturity -- that's exactly the
signal a sales/product conversation about upgrading them would use.

Known v1 limitation: every detected PAIN_POINT signal is weighted equally
regardless of severity (the Signal model has no per-signal severity field
-- see models/signal.py's own known-v1-limitation note); this is a coarse
proxy, not a calibrated maturity index.
"""

from __future__ import annotations

from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.signal import Signal, SignalType

_BASELINE_SCORE = 50
_HAS_WEBSITE_BONUS = 20
_PAIN_POINT_PENALTY = 15
_BUYING_SIGNAL_BONUS = 5
_MAX_SCORE = 100
_MIN_SCORE = 0


def compute_operational_maturity(institution: CanonicalInstitution, signals: list[Signal]) -> int:
    score = _BASELINE_SCORE

    if institution.website:
        score += _HAS_WEBSITE_BONUS

    pain_point_count = sum(1 for s in signals if s.signal_type == SignalType.PAIN_POINT)
    buying_signal_count = sum(1 for s in signals if s.signal_type == SignalType.BUYING_SIGNAL)

    score -= pain_point_count * _PAIN_POINT_PENALTY
    # Buying signals (e.g. "now hiring", "new campus") indicate growth, not
    # digital maturity directly, but growth-stage institutions tend to be
    # actively investing in their own operations -- a small positive
    # nudge, capped low relative to the pain-point penalty so a growing but
    # genuinely under-tooled institution still scores low overall.
    score += min(buying_signal_count, 2) * _BUYING_SIGNAL_BONUS

    return max(_MIN_SCORE, min(_MAX_SCORE, score))
