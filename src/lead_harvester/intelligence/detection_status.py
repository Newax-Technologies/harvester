"""
Computes a DetectionStatus (models/profile.py) for the two service_gap.py
products -- website and LMS -- from crawl evidence. See docs/ROADMAP.md
module 20's "Correction" note.

The static crawler (sources/web.py) fetches and pattern-matches HTML; it
cannot see content behind an authentication wall or rendered client-side
by JavaScript. That means a negative crawl result is real evidence of
"we looked and didn't find it," but it is never proof the technology
doesn't exist -- so neither function here can return
DetectionStatus.ABSENT_CONFIRMED. That state is reserved for a stronger
evidence source (e.g. an explicit manual/authorized-import assertion)
that doesn't exist yet in this codebase; it stays in the enum for that
future source, not for the crawler path.
"""

from __future__ import annotations

from lead_harvester.models.profile import DetectionStatus
from lead_harvester.models.signal import Signal, SignalType
from lead_harvester.models.source import RawPageSnapshot

_LMS_KEYWORDS = ("learning management system", "parent portal", "student portal")


def _successful_snapshots(snapshots: list[RawPageSnapshot]) -> list[RawPageSnapshot]:
    return [s for s in snapshots if not s.fetch_error and s.html]


def compute_website_detection_status(
    website: str | None, snapshots: list[RawPageSnapshot]
) -> DetectionStatus:
    """
    `snapshots` should already be scoped to this one institution's own
    crawled pages (see services/lead_profile_service.py::_get_website_snapshots).

    UNKNOWN, not ABSENT_CONFIRMED, when `website` is blank: this system
    has no source that exhaustively searches for and confirms a genuine
    absence of any website -- a blank field far more often means "we
    haven't found their site yet" than "they confirmed have none."
    Treating it as UNKNOWN (a reduced, not full, service_gap_score
    contribution -- see intelligence/service_gap.py) is the correction
    this status model exists to make.
    """
    if not website:
        return DetectionStatus.UNKNOWN
    if not snapshots:
        return DetectionStatus.NOT_CRAWLED
    if _successful_snapshots(snapshots):
        return DetectionStatus.PRESENT
    return DetectionStatus.CRAWL_FAILED


def compute_lms_detection_status(
    website: str | None, snapshots: list[RawPageSnapshot], signals: list[Signal]
) -> DetectionStatus:
    """
    See module docstring for why this can never return ABSENT_CONFIRMED:
    a static crawler finding no LMS/portal keyword in the pages it could
    reach is real but inherently incomplete evidence (an authenticated
    student portal or a JS-rendered dashboard is invisible to it), so the
    strongest this function can assert from that evidence is NOT_DETECTED.
    """
    has_lms_signal = any(
        s.signal_type == SignalType.TECHNOLOGY_PRESENT
        and any(keyword in s.signal_text.lower() for keyword in _LMS_KEYWORDS)
        for s in signals
    )
    if has_lms_signal:
        return DetectionStatus.PRESENT
    if not website or not snapshots:
        # Nothing to crawl at all (no website on file) or a website on
        # file that was never actually fetched -- either way, no attempt
        # was made to look for an LMS specifically.
        return DetectionStatus.NOT_CRAWLED
    if not _successful_snapshots(snapshots):
        return DetectionStatus.CRAWL_FAILED
    return DetectionStatus.NOT_DETECTED
