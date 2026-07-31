"""
The single source of truth for CanonicalInstitution.confidence_score's
formula: an "API/UI-facing percentage" (0-100), NOT a 0-1 fraction --
canonical/merger.py's own comments already establish this convention
(confidence_score=len(raw_records) * 10.0 at creation,
min(confidence_score + 10.0, 100.0) on each new independent source).

Extracted here (rather than left as two separate inline literals in
merger.py) so a THIRD copy never has to guess the formula or its scale
again -- exactly the divergence docs/CODE_REVIEW_LESSONS.md pattern 2
warns about. This already happened once: api/routes/manual_leads.py set
confidence_score=0.7 (a 0-1 fraction) and profiles/scoring.py thresholded
it at >0.8/>0.5 (also 0-1 assumptions) -- both silently wrong against the
real 0-100 scale, both fixed alongside this extraction.
"""

from __future__ import annotations

POINTS_PER_SOURCE = 10.0
MAX_CONFIDENCE = 100.0


def confidence_for_source_count(source_count: int) -> float:
    """confidence_score for an institution built/corroborated by `source_count` distinct sources."""
    return min(source_count * POINTS_PER_SOURCE, MAX_CONFIDENCE)


def bump_confidence(current: float) -> float:
    """confidence_score after one additional independent source attaches."""
    return min(current + POINTS_PER_SOURCE, MAX_CONFIDENCE)
