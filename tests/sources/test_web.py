import asyncio

import httpx
import pytest

from lead_harvester.config import Settings
from lead_harvester.sources.web import CrawlItem, DomainRateLimiter, Lead, RobotsCache, WebCrawler


def test_extract_lead_populates_detected_signals():
    html = """
    <html><body>
    <h1>Beacon House School</h1>
    <p>Email us at admissions@beaconhouse.example.edu or call +923001234567.</p>
    <p>We're now hiring teachers for the new term.</p>
    </body></html>
    """
    crawler = WebCrawler(Settings(google_places_api_key="dummy-test-key"))
    lead, _links = crawler._extract_lead(html, "https://beaconhouse.example.edu")

    assert lead is not None
    assert lead.raw["detected_signals"] == [
        {
            "signal_type": "buying_signal",
            "text": "Actively hiring -- may indicate growth/budget.",
        }
    ]


def test_extract_lead_with_no_signals_gets_empty_list():
    html = """
    <html><body>
    <h1>Beacon House School</h1>
    <p>Email us at admissions@beaconhouse.example.edu or call +923001234567.</p>
    </body></html>
    """
    crawler = WebCrawler(Settings(google_places_api_key="dummy-test-key"))
    lead, _links = crawler._extract_lead(html, "https://beaconhouse.example.edu")

    assert lead is not None
    assert lead.raw["detected_signals"] == []


def _lead(**raw_overrides) -> Lead:
    raw = {
        "description": "",
        "all_emails": [],
        "all_phones": [],
        "pages": ["https://example.edu"],
        "detected_signals": [],
    }
    raw.update(raw_overrides)
    return Lead(
        source="website",
        source_url="https://example.edu",
        name="",
        organization="Example School",
        title="",
        email="",
        phone="",
        website="https://example.edu",
        location="",
        social_profiles=[],
        evidence="",
        raw=raw,
    )


def test_merge_combines_and_dedupes_detected_signals_from_both_pages():
    existing = _lead(
        detected_signals=[
            {
                "signal_type": "buying_signal",
                "text": "Actively hiring -- may indicate growth/budget.",
            }
        ]
    )
    incoming = _lead(
        detected_signals=[
            # Duplicate of an existing signal -- must not appear twice.
            {
                "signal_type": "buying_signal",
                "text": "Actively hiring -- may indicate growth/budget.",
            },
            {
                "signal_type": "pain_point",
                "text": "Uses WhatsApp for communication with no online booking/portal.",
            },
        ]
    )

    merged = WebCrawler._merge(existing, incoming)

    assert len(merged.raw["detected_signals"]) == 2
    assert {
        "signal_type": "pain_point",
        "text": "Uses WhatsApp for communication with no online booking/portal.",
    } in merged.raw["detected_signals"]


def test_merge_with_no_existing_lead_returns_incoming_unchanged():
    incoming = _lead(
        detected_signals=[
            {
                "signal_type": "buying_signal",
                "text": "Actively hiring -- may indicate growth/budget.",
            }
        ]
    )

    merged = WebCrawler._merge(None, incoming)

    assert merged is incoming


def _fetch_ctx(handler):
    """
    A real httpx.AsyncClient backed by a MockTransport, plus the
    RobotsCache/DomainRateLimiter/Semaphore _fetch needs -- everything is
    allowed by robots (no robots.txt handling needed in `handler`; the
    RobotsCache is pre-seeded with an always-allow parser so it never
    issues its own request).
    """
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    robots = RobotsCache(client, "LeadBot/1.0")

    class _AllowAllParser:
        def can_fetch(self, *_args, **_kwargs):
            return True

    robots.cache["https://example.edu"] = _AllowAllParser()
    limiter = DomainRateLimiter(0.0)
    semaphore = asyncio.Semaphore(5)
    return client, robots, limiter, semaphore


@pytest.mark.asyncio
async def test_fetch_records_a_snapshot_on_success():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"}, text="<html>hi</html>")

    crawler = WebCrawler(Settings())
    client, robots, limiter, semaphore = _fetch_ctx(handler)
    item = CrawlItem(url="https://example.edu/", depth=0)

    result = await crawler._fetch(client, robots, limiter, semaphore, item)

    assert result == ("<html>hi</html>", "https://example.edu/")
    assert len(crawler.snapshots) == 1
    snapshot = crawler.snapshots[0]
    assert snapshot.url == "https://example.edu/"
    assert snapshot.status_code == 200
    assert snapshot.html == "<html>hi</html>"
    assert snapshot.fetch_error == ""


@pytest.mark.asyncio
async def test_fetch_records_a_snapshot_for_robots_disallowed():
    crawler = WebCrawler(Settings())
    client, robots, limiter, semaphore = _fetch_ctx(lambda r: httpx.Response(200))

    class _DisallowParser:
        def can_fetch(self, *_args, **_kwargs):
            return False

    robots.cache["https://example.edu"] = _DisallowParser()
    item = CrawlItem(url="https://example.edu/private", depth=0)

    result = await crawler._fetch(client, robots, limiter, semaphore, item)

    assert result is None
    assert crawler.snapshots[0].fetch_error == "robots_disallowed"
    assert crawler.snapshots[0].html is None


@pytest.mark.asyncio
async def test_fetch_records_a_snapshot_for_non_html_content_type():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "application/pdf"}, content=b"%PDF")

    crawler = WebCrawler(Settings())
    client, robots, limiter, semaphore = _fetch_ctx(handler)
    item = CrawlItem(url="https://example.edu/brochure.pdf", depth=0)

    result = await crawler._fetch(client, robots, limiter, semaphore, item)

    assert result is None
    assert crawler.snapshots[0].fetch_error == "non_html_content_type"
    assert crawler.snapshots[0].status_code == 200


@pytest.mark.asyncio
async def test_fetch_records_a_snapshot_for_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, headers={"content-type": "text/html"})

    crawler = WebCrawler(Settings())
    client, robots, limiter, semaphore = _fetch_ctx(handler)
    item = CrawlItem(url="https://example.edu/missing", depth=0)

    result = await crawler._fetch(client, robots, limiter, semaphore, item)

    assert result is None
    assert crawler.snapshots[0].status_code == 404
    assert "404" in crawler.snapshots[0].fetch_error


@pytest.mark.asyncio
async def test_fetch_records_a_snapshot_for_response_too_large():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"}, text="x" * 1000)

    settings = Settings()
    settings.max_response_bytes = 10
    crawler = WebCrawler(settings)
    client, robots, limiter, semaphore = _fetch_ctx(handler)
    item = CrawlItem(url="https://example.edu/huge", depth=0)

    result = await crawler._fetch(client, robots, limiter, semaphore, item)

    assert result is None
    assert crawler.snapshots[0].fetch_error == "response_too_large"
