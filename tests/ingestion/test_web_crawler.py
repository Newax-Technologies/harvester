from contextlib import contextmanager
from unittest.mock import patch

import httpx
import pytest

from lead_harvester.config import Settings
from lead_harvester.ingestion.web_crawler import WebCrawler


def _settings(**overrides) -> Settings:
    defaults = dict(
        user_agent="TestBot/1.0",
        request_timeout_seconds=5.0,
        concurrency=2,
        delay_seconds=0.0,
        max_pages_per_domain=10,
        max_depth=2,
        max_response_bytes=1_000_000,
        keywords=[],
        intent_terms=[],
    )
    defaults.update(overrides)
    return Settings(**defaults)


@contextmanager
def _mock_transport(handler):
    """
    WebCrawler.crawl constructs its own httpx.AsyncClient internally with no
    way to inject a transport from the outside -- patch AsyncClient.__init__
    for the duration of the test so every client it builds (there's only
    ever the one, reused for both robots.txt and page fetches) uses our
    MockTransport instead of hitting the network.
    """
    original_init = httpx.AsyncClient.__init__

    def patched_init(self, *args, **kwargs):
        kwargs["transport"] = httpx.MockTransport(handler)
        original_init(self, *args, **kwargs)

    with patch.object(httpx.AsyncClient, "__init__", patched_init):
        yield


def _robots_allow_all(request: httpx.Request) -> httpx.Response | None:
    if request.url.path == "/robots.txt":
        return httpx.Response(200, text="User-agent: *\nAllow: /\n")
    return None


@pytest.mark.asyncio
async def test_crawl_follows_internal_links_and_extracts_a_lead():
    def handler(request: httpx.Request) -> httpx.Response:
        robots = _robots_allow_all(request)
        if robots is not None:
            return robots
        if request.url.host == "example.com" and request.url.path == "/":
            return httpx.Response(
                200,
                headers={"content-type": "text/html"},
                text=(
                    '<html><body><a href="https://example.com/contact">Contact</a>'
                    '<a href="https://external.com/">External</a></body></html>'
                ),
            )
        if request.url.host == "example.com" and request.url.path == "/contact":
            return httpx.Response(
                200,
                headers={"content-type": "text/html"},
                text="<html><body>Reach us at info@example.com</body></html>",
            )
        return httpx.Response(404)

    with _mock_transport(handler):
        crawler = WebCrawler(_settings())
        leads = await crawler.crawl(["https://example.com/"])

    assert len(leads) == 1
    assert leads[0].email == "info@example.com"
    assert leads[0].website == "https://example.com"


@pytest.mark.asyncio
async def test_crawl_does_not_follow_external_links():
    visited_hosts = set()

    def handler(request: httpx.Request) -> httpx.Response:
        robots = _robots_allow_all(request)
        if robots is not None:
            return robots
        visited_hosts.add(request.url.host)
        if request.url.host == "example.com" and request.url.path == "/":
            return httpx.Response(
                200,
                headers={"content-type": "text/html"},
                text='<html><body><a href="https://external.com/">External</a></body></html>',
            )
        return httpx.Response(200, headers={"content-type": "text/html"}, text="<html></html>")

    with _mock_transport(handler):
        crawler = WebCrawler(_settings())
        await crawler.crawl(["https://example.com/"])

    assert "external.com" not in visited_hosts


@pytest.mark.asyncio
async def test_crawl_respects_max_depth():
    # A chain: seed(depth 0) -> /page1(depth 1) -> /page2(depth 2, not
    # fetched when max_depth=1 -- only links found at depth < max_depth are
    # queued for a further fetch).
    fetched_paths = []

    def handler(request: httpx.Request) -> httpx.Response:
        robots = _robots_allow_all(request)
        if robots is not None:
            return robots
        fetched_paths.append(request.url.path)
        if request.url.path == "/":
            return httpx.Response(
                200,
                headers={"content-type": "text/html"},
                text='<html><body><a href="https://example.com/page1">Next</a></body></html>',
            )
        if request.url.path == "/page1":
            return httpx.Response(
                200,
                headers={"content-type": "text/html"},
                text='<html><body><a href="https://example.com/page2">Next</a></body></html>',
            )
        return httpx.Response(200, headers={"content-type": "text/html"}, text="<html></html>")

    with _mock_transport(handler):
        crawler = WebCrawler(_settings(max_depth=1))
        await crawler.crawl(["https://example.com/"])

    assert "/" in fetched_paths
    assert "/page1" in fetched_paths
    assert "/page2" not in fetched_paths


@pytest.mark.asyncio
async def test_crawl_merges_leads_from_multiple_pages_on_the_same_domain():
    def handler(request: httpx.Request) -> httpx.Response:
        robots = _robots_allow_all(request)
        if robots is not None:
            return robots
        if request.url.path == "/":
            return httpx.Response(
                200,
                headers={"content-type": "text/html"},
                text=(
                    '<html><body>'
                    '<a href="https://example.com/email">Email page</a>'
                    '<a href="https://example.com/phone">Phone page</a>'
                    "</body></html>"
                ),
            )
        if request.url.path == "/email":
            return httpx.Response(
                200,
                headers={"content-type": "text/html"},
                text="<html><body>info@example.com</body></html>",
            )
        if request.url.path == "/phone":
            return httpx.Response(
                200,
                headers={"content-type": "text/html"},
                text="<html><body>Call +92 300 1234567</body></html>",
            )
        return httpx.Response(200, headers={"content-type": "text/html"}, text="<html></html>")

    with _mock_transport(handler):
        crawler = WebCrawler(_settings())
        leads = await crawler.crawl(["https://example.com/"])

    # Both pages describe the same domain -- merged into one Lead rather
    # than reported as two separate, incomplete records.
    assert len(leads) == 1
    assert leads[0].email == "info@example.com"
    assert leads[0].phone
