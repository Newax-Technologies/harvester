"""
Per-domain rate limiting for the web crawler -- docs/ROADMAP.md module 3
(Collection and Crawling). Moved out of sources/web.py, which previously
held the crawl loop, robots/rate-limiting, and HTTP fetching all in one
file with no separation between "decide when it's safe to hit this domain
again" and the rest of the crawl.
"""

from __future__ import annotations

import asyncio
import time
from collections import defaultdict
from urllib.parse import urlparse


class DomainRateLimiter:
    def __init__(self, delay_seconds: float):
        self.delay_seconds = max(0.0, delay_seconds)
        self.last_request: dict[str, float] = defaultdict(float)
        self.locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

    async def wait(self, url: str) -> None:
        domain = urlparse(url).netloc.lower()
        async with self.locks[domain]:
            elapsed = time.monotonic() - self.last_request[domain]
            delay = self.delay_seconds - elapsed
            if delay > 0:
                await asyncio.sleep(delay)
            self.last_request[domain] = time.monotonic()
