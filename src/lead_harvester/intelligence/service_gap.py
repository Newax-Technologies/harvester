"""
Computes service_gap_score -- see docs/ROADMAP.md module 20.

The best lead is the one with the *most* service gaps NEWAX can sell
into, not the fewest -- the opposite of what a generic "looks legitimate"
qualification check would optimize for. Decided formula:
`opportunity_score = missing_product_count * size_multiplier` -- a small
single-branch institution missing every product still scores lower than a
multi-branch institution missing the same things.

Decided detection policy: absence means unavailable, full stop -- no
website found means no website, no LMS signal detected means no LMS, for
both. This is a deliberate accepted tradeoff (documented in ROADMAP): an
institution the crawler never actually reached looks identical to one
confirmed to lack a website/LMS.

IoT hardware/software integration is a known v1 limitation, stated up
front rather than discovered later: rarely announced on a public website,
so it's treated as unknown/neutral (no product slot, no gap contribution)
rather than assumed-absent -- unlike website/LMS above, since there's no
realistic way to even attempt detecting it from a public site.
"""

from __future__ import annotations

from lead_harvester.models.profile import SizeTier, WebsiteQualityTier
from lead_harvester.models.signal import Signal, SignalType

# WebsiteQualityTier -> gap contribution for the website product slot.
# NONE counts as fully missing; POOR/ADEQUATE are a partial gap -- still a
# real upsell/redesign opportunity; GOOD/EXCEPTIONAL count as no gap.
_WEBSITE_GAP_WEIGHT: dict[WebsiteQualityTier, float] = {
    WebsiteQualityTier.NONE: 1.0,
    WebsiteQualityTier.POOR: 0.5,
    WebsiteQualityTier.ADEQUATE: 0.5,
    WebsiteQualityTier.GOOD: 0.0,
    WebsiteQualityTier.EXCEPTIONAL: 0.0,
}

_SIZE_MULTIPLIER: dict[SizeTier, float] = {
    SizeTier.UNKNOWN: 1.0,
    SizeTier.SMALL: 1.0,
    SizeTier.MEDIUM: 1.5,
    SizeTier.LARGE: 2.0,
}

_LMS_KEYWORDS = ("learning management system", "parent portal", "student portal")


def _has_lms_signal(signals: list[Signal]) -> bool:
    return any(
        s.signal_type == SignalType.TECHNOLOGY_PRESENT
        and any(keyword in s.signal_text.lower() for keyword in _LMS_KEYWORDS)
        for s in signals
    )


def compute_service_gap_score(
    website_quality_tier: WebsiteQualityTier,
    signals: list[Signal],
    size_tier: SizeTier,
) -> float:
    """
    missing_product_count sums the website gap (0/0.5/1, from
    website_quality_tier) and the LMS gap (0 or 1, from whether any
    TECHNOLOGY_PRESENT signal mentions an LMS/portal) -- see module
    docstring for why absence means unavailable rather than unknown for
    these two. IoT is deliberately excluded (no product slot at all in
    v1). The sum is then scaled by size_multiplier so a larger
    institution's gaps outrank an identical small one's.
    """
    missing_product_count = _WEBSITE_GAP_WEIGHT[website_quality_tier]
    if not _has_lms_signal(signals):
        missing_product_count += 1.0

    return missing_product_count * _SIZE_MULTIPLIER[size_tier]
