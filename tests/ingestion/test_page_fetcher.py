import asyncio

import httpx
import pytest

from lead_harvester.ingestion.page_fetcher import RobotsCache, fetch_page
from lead_harvester.ingestion.rate_limiter import DomainRateLimiter


async def _fetch(handler, url: str, *, max_response_bytes: int = 1_000_000):
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        robots = RobotsCache(client, "TestBot/1.0")
        limiter = DomainRateLimiter(0.0)
        semaphore = asyncio.Semaphore(2)
        return await fetch_page(
            client, robots, limiter, semaphore, url, max_response_bytes=max_response_bytes
        )


@pytest.mark.asyncio
async def test_fetch_page_returns_body_and_final_url():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /\n")
        return httpx.Response(
            200,
            headers={"content-type": "text/html; charset=utf-8"},
            text="<html><body>Hello</body></html>",
        )

    result = await _fetch(handler, "https://example.com/page")

    assert result is not None
    body, final_url = result
    assert "Hello" in body
    assert final_url == "https://example.com/page"


@pytest.mark.asyncio
async def test_fetch_page_respects_robots_disallow():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nDisallow: /private\n")
        return httpx.Response(200, headers={"content-type": "text/html"}, text="<html></html>")

    result = await _fetch(handler, "https://example.com/private/page")

    assert result is None


@pytest.mark.asyncio
async def test_fetch_page_rejects_non_html_content_type():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /\n")
        return httpx.Response(
            200, headers={"content-type": "application/pdf"}, content=b"%PDF-1.4"
        )

    result = await _fetch(handler, "https://example.com/file.pdf")

    assert result is None


@pytest.mark.asyncio
async def test_fetch_page_enforces_max_response_bytes():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /\n")
        return httpx.Response(200, headers={"content-type": "text/html"}, text="x" * 2000)

    result = await _fetch(handler, "https://example.com/big", max_response_bytes=100)

    assert result is None


@pytest.mark.asyncio
async def test_fetch_page_returns_none_on_http_error_status():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /\n")
        return httpx.Response(500, headers={"content-type": "text/html"}, text="boom")

    result = await _fetch(handler, "https://example.com/broken")

    assert result is None


@pytest.mark.asyncio
async def test_robots_cache_reuses_parsed_result_for_same_root():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nAllow: /\n")
        return httpx.Response(200, headers={"content-type": "text/html"}, text="<html></html>")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        robots = RobotsCache(client, "TestBot/1.0")
        assert await robots.allowed("https://example.com/a")
        assert await robots.allowed("https://example.com/b")

    assert calls.count("/robots.txt") == 1
