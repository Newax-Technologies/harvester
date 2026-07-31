"""
robots.txt-aware, size-bounded page fetching -- docs/ROADMAP.md module 3
(Collection and Crawling). Moved out of sources/web.py alongside
rate_limiter.py; see that module's docstring for why.
"""

from __future__ import annotations

import asyncio
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx

from .rate_limiter import DomainRateLimiter


class RobotsCache:
    def __init__(self, client: httpx.AsyncClient, user_agent: str):
        self.client = client
        self.user_agent = user_agent
        self.cache: dict[str, RobotFileParser] = {}
        self.lock = asyncio.Lock()

    async def allowed(self, url: str) -> bool:
        parsed = urlparse(url)
        root = f"{parsed.scheme}://{parsed.netloc}"
        async with self.lock:
            parser = self.cache.get(root)
            if parser is None:
                parser = RobotFileParser()
                robots_url = f"{root}/robots.txt"
                parser.set_url(robots_url)
                try:
                    response = await self.client.get(robots_url)
                    if response.status_code < 400:
                        parser.parse(response.text.splitlines())
                    else:
                        parser.parse([])
                except httpx.HTTPError:
                    parser.parse([])
                self.cache[root] = parser
        return parser.can_fetch(self.user_agent, url)


async def fetch_page(
    client: httpx.AsyncClient,
    robots: RobotsCache,
    limiter: DomainRateLimiter,
    semaphore: asyncio.Semaphore,
    url: str,
    *,
    max_response_bytes: int,
) -> tuple[str, str] | None:
    """
    Fetches one URL, honoring robots.txt and the domain rate limit, bounded
    to max_response_bytes and text/html-ish content types. Returns
    (decoded_body, final_url_after_redirects), or None if the URL is
    disallowed, not HTML, over the size cap, or the request itself failed.
    """
    if not await robots.allowed(url):
        return None
    await limiter.wait(url)
    async with semaphore:
        try:
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                content_type = response.headers.get("content-type", "").lower()
                if (
                    "text/html" not in content_type
                    and "application/xhtml+xml" not in content_type
                ):
                    return None
                chunks: list[bytes] = []
                size = 0
                async for chunk in response.aiter_bytes():
                    size += len(chunk)
                    if size > max_response_bytes:
                        return None
                    chunks.append(chunk)
                encoding = response.encoding or "utf-8"
                return b"".join(chunks).decode(encoding, errors="replace"), str(response.url)
        except (httpx.HTTPError, UnicodeError):
            return None
