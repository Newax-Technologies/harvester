"""
Computes service_gap_score -- see docs/ROADMAP.md module 20.

The best lead is the one with the *most* service gaps NEWAX can sell
into, not the fewest -- the opposite of what a generic "looks legitimate"
qualification check would optimize for. Decided formula:
`opportunity_score = missing_product_count * size_multiplier` -- a small
single-branch institution missing every product still scores lower than a
multi-branch institution missing the same things.

Correction: the original v1 policy ("absence means unavailable, full
stop") treated "no website on file" and "no LMS signal detected" as
equally strong, maximum-confidence evidence of a missing product --
indistinguishable from an institution the crawler genuinely confirmed
lacks one. A static crawler cannot establish absence of a technology,
especially one behind authentication or rendered client-side by
JavaScript (see intelligence/detection_status.py) -- so `missing_product_count`
is now driven by a per-product DetectionStatus
(models/profile.py) via _DETECTION_GAP_WEIGHT: only DetectionStatus.ABSENT_CONFIRMED
contributes a full missing-product score; NOT_DETECTED/UNKNOWN contribute
a reduced amount (real but incomplete evidence, or none at all); a pure
data gap (NOT_CRAWLED/CRAWL_FAILED -- no attempt made, or the attempt
produced nothing usable) contributes nothing, since there is no basis
whatsoever to call it a gap.

IoT hardware/software integration is a known v1 limitation, stated up
front rather than discovered later: rarely announced on a public website,
so it's treated as unknown/neutral (no product slot, no gap contribution)
rather than assumed-absent -- unlike website/LMS above, since there's no
realistic way to even attempt detecting it from a public site.
"""

from __future__ import annotations

from dataclasses import dataclass

from lead_harvester.intelligence.detection_status import (
    compute_lms_detection_status,
    compute_website_detection_status,
)
from lead_harvester.models.profile import DetectionStatus, SizeTier, WebsiteQualityTier
from lead_harvester.models.signal import Signal
from lead_harvester.models.source import RawPageSnapshot

# WebsiteQualityTier -> gap contribution for the website product slot,
# used only once DetectionStatus confirms the website is actually
# PRESENT (see compute_service_gap_score) -- NONE counts as fully
# missing (a present-but-unscoreable site shouldn't happen once PRESENT
# is established, since PRESENT requires at least one successful
# snapshot, but the mapping is kept total rather than partial);
# POOR/ADEQUATE are a partial gap -- still a real upsell/redesign
# opportunity; GOOD/EXCEPTIONAL count as no gap.
_WEBSITE_GAP_WEIGHT: dict[WebsiteQualityTier, float] = {
    WebsiteQualityTier.NONE: 1.0,
    WebsiteQualityTier.POOR: 0.5,
    WebsiteQualityTier.ADEQUATE: 0.5,
    WebsiteQualityTier.GOOD: 0.0,
    WebsiteQualityTier.EXCEPTIONAL: 0.0,
}

# [Certain] Only ABSENT_CONFIRMED contributes a full (1.0) missing-product
# score. NOT_DETECTED/UNKNOWN reduce confidence -- a real but incomplete
# signal, not proof -- rather than scoring as a full opportunity.
# NOT_CRAWLED/CRAWL_FAILED are pure data gaps (no evidence was even
# gathered) and contribute nothing: there is no basis to call an
# institution we never looked at "missing" anything.
_DETECTION_GAP_WEIGHT: dict[DetectionStatus, float] = {
    DetectionStatus.PRESENT: 0.0,
    DetectionStatus.ABSENT_CONFIRMED: 1.0,
    DetectionStatus.NOT_DETECTED: 0.3,
    DetectionStatus.UNKNOWN: 0.15,
    DetectionStatus.NOT_CRAWLED: 0.0,
    DetectionStatus.CRAWL_FAILED: 0.0,
}

_SIZE_MULTIPLIER: dict[SizeTier, float] = {
    SizeTier.UNKNOWN: 1.0,
    SizeTier.SMALL: 1.0,
    SizeTier.MEDIUM: 1.5,
    SizeTier.LARGE: 2.0,
}


@dataclass(frozen=True)
class ServiceGapResult:
    score: float
    website_status: DetectionStatus
    lms_status: DetectionStatus


def compute_service_gap_score(
    website: str | None,
    website_snapshots: list[RawPageSnapshot],
    website_quality_tier: WebsiteQualityTier,
    signals: list[Signal],
    size_tier: SizeTier,
) -> ServiceGapResult:
    """
    missing_product_count sums the website gap and the LMS gap. The
    website gap uses _WEBSITE_GAP_WEIGHT's quality-based 0/0.5/1 (the
    original, unchanged distinction between "no site," "a weak site,"
    and "a strong site") only when website DetectionStatus is PRESENT;
    otherwise (no confirmed site to grade the quality of) it falls back
    to _DETECTION_GAP_WEIGHT, same as the LMS gap always does. The sum is
    then scaled by size_multiplier so a larger institution's gaps
    outrank an identical small one's. Returns both per-product statuses
    alongside the score so services/lead_profile_service.py can persist
    them for evidence/transparency without recomputing.
    """
    website_status = compute_website_detection_status(website, website_snapshots)
    lms_status = compute_lms_detection_status(website, website_snapshots, signals)

    if website_status == DetectionStatus.PRESENT:
        website_gap = _WEBSITE_GAP_WEIGHT[website_quality_tier]
    else:
        website_gap = _DETECTION_GAP_WEIGHT[website_status]

    lms_gap = _DETECTION_GAP_WEIGHT[lms_status]

    missing_product_count = website_gap + lms_gap
    score = missing_product_count * _SIZE_MULTIPLIER[size_tier]
    return ServiceGapResult(score=score, website_status=website_status, lms_status=lms_status)
