from lead_harvester.intelligence.website_quality import compute_website_quality_tier
from lead_harvester.models.profile import WebsiteQualityTier
from lead_harvester.models.source import RawPageSnapshot

_VIEWPORT_HTML = '<html><head><meta name="viewport" content="width=device-width"></head></html>'
_FULL_HTML = (
    '<html><head><meta name="viewport" content="width=device-width"></head>'
    "<body><form action='/contact'></form></body></html>"
)


def _snapshot(**overrides) -> RawPageSnapshot:
    defaults = {
        "url": "https://example.edu",
        "final_url": "https://example.edu",
        "html": "",
        "fetch_error": "",
    }
    defaults.update(overrides)
    return RawPageSnapshot(**defaults)


def test_no_website_is_none():
    assert compute_website_quality_tier(None, []) == WebsiteQualityTier.NONE
    assert compute_website_quality_tier("", []) == WebsiteQualityTier.NONE


def test_https_only_with_no_pages_is_poor():
    assert compute_website_quality_tier("https://example.edu", []) == WebsiteQualityTier.POOR


def test_partial_checklist_with_a_broken_page_is_adequate():
    # https(2) + viewport(2) -- no form, no depth bonus (only 2 pages), no
    # broken-link bonus (1 of 2 pages is an HTTP-error page, >=10%). Score 5.
    snapshots = [_snapshot(html=_VIEWPORT_HTML), _snapshot(fetch_error="http_error: 500")]
    tier = compute_website_quality_tier("https://example.edu", snapshots)
    assert tier == WebsiteQualityTier.ADEQUATE


def test_full_page_checklist_with_a_broken_page_is_good():
    # https(2) + viewport(2) + form(2) + depth(1, only 2 pages) -- no
    # broken-link bonus (1 of 2 pages is an HTTP-error page). Score 7.
    snapshots = [_snapshot(html=_FULL_HTML), _snapshot(fetch_error="http_error: 500")]
    tier = compute_website_quality_tier("https://example.edu", snapshots)
    assert tier == WebsiteQualityTier.GOOD


def test_full_checklist_with_deep_crawl_is_exceptional():
    # https(2) + viewport(2) + form(2) + depth(2, 6+ pages) + no broken
    # pages(2). Score 10.
    snapshots = [_snapshot(html=_FULL_HTML) for _ in range(6)]
    tier = compute_website_quality_tier("https://example.edu", snapshots)
    assert tier == WebsiteQualityTier.EXCEPTIONAL


def test_non_http_error_fetch_failures_are_not_counted_as_broken():
    # robots_disallowed rows are exclusions, not evidence of a broken site
    # -- they must not deny the low-broken-link-rate bonus.
    snapshots = [_snapshot(html=_FULL_HTML) for _ in range(6)]
    snapshots += [_snapshot(fetch_error="robots_disallowed") for _ in range(10)]
    tier = compute_website_quality_tier("https://example.edu", snapshots)
    assert tier == WebsiteQualityTier.EXCEPTIONAL
