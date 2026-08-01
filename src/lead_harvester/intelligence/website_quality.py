"""
Computes a WebsiteQualityTier for an institution from its crawled
RawPageSnapshot rows -- see docs/ROADMAP.md module 20's website quality
engine.

Rule-based, built on the existing static crawler (sources/web.py's
httpx+BeautifulSoup fetch already captures everything this checklist
needs) -- no headless-browser/JS-rendering pass in v1, decided with the
user. Purely structural/technical signals, no design/copywriting/visual-
quality judgment (that would need an LLM-based path not chosen for v1) --
a site that is technically solid but ugly, or vice versa, isn't
distinguished.
"""

from __future__ import annotations

import re

from lead_harvester.models.profile import WebsiteQualityTier
from lead_harvester.models.source import RawPageSnapshot

_VIEWPORT_META_RE = re.compile(r'<meta[^>]+name=["\']viewport["\']', re.IGNORECASE)
_FORM_TAG_RE = re.compile(r"<form\b", re.IGNORECASE)

# Weighted checklist points. Chosen so no single check dominates the tier
# on its own, and the max attainable (10) maps cleanly onto the five tiers
# below.
_POINTS_HTTPS = 2
_POINTS_MOBILE_VIEWPORT = 2
_POINTS_CONTACT_FORM = 2
_POINTS_PAGE_DEPTH_ADEQUATE = 1  # 2-5 pages crawled
_POINTS_PAGE_DEPTH_COMPREHENSIVE = 2  # 6+ pages crawled
_POINTS_LOW_BROKEN_LINK_RATE = 2  # < 10% of this site's pages were HTTP errors


def compute_website_quality_tier(
    website: str | None, snapshots: list[RawPageSnapshot]
) -> WebsiteQualityTier:
    """
    `snapshots` should already be scoped to the one institution's own
    crawled pages (see services/lead_profile_service.py's caller for how
    that scoping query works). NONE is forced whenever `website` is absent
    -- no scoring needed for an institution with no site at all.
    """
    if not website:
        return WebsiteQualityTier.NONE

    score = 0
    if website.strip().lower().startswith("https://"):
        score += _POINTS_HTTPS

    successful = [s for s in snapshots if not s.fetch_error and s.html]
    if any(_VIEWPORT_META_RE.search(s.html) for s in successful):
        score += _POINTS_MOBILE_VIEWPORT
    if any(_FORM_TAG_RE.search(s.html) for s in successful):
        score += _POINTS_CONTACT_FORM

    page_count = len(snapshots)
    if page_count >= 6:
        score += _POINTS_PAGE_DEPTH_COMPREHENSIVE
    elif page_count >= 2:
        score += _POINTS_PAGE_DEPTH_ADEQUATE

    # Only HTTP-error fetches count as "broken" -- robots-disallowed,
    # oversized, and decode-error rows are exclusions, not evidence of a
    # broken site (module 3's RawPageSnapshot.fetch_error already
    # distinguishes these via its machine-readable reason string).
    if page_count:
        broken = sum(1 for s in snapshots if s.fetch_error.startswith("http_error"))
        if (broken / page_count) < 0.1:
            score += _POINTS_LOW_BROKEN_LINK_RATE

    if score >= 8:
        return WebsiteQualityTier.EXCEPTIONAL
    if score >= 6:
        return WebsiteQualityTier.GOOD
    if score >= 3:
        return WebsiteQualityTier.ADEQUATE
    return WebsiteQualityTier.POOR
