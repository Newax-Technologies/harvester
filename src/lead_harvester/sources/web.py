from __future__ import annotations

import asyncio
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx

from ..config import Settings
from ..enrichment.technology_detector import detect_technology_signals
from ..extractors import (
    best_evidence,
    candidate_internal_links,
    extract_emails,
    extract_links,
    extract_page_identity,
    extract_phones,
    extract_social_profiles,
    visible_text,
)


@dataclass
class Lead:
    source: str
    source_url: str
    name: str
    organization: str
    title: str
    email: str
    phone: str
    website: str
    location: str
    social_profiles: list[str]
    evidence: str
    raw: dict[str, Any]


@dataclass(slots=True)
class CrawlItem:
    url: str
    depth: int


@dataclass(slots=True)
class PageSnapshot:
    """
    One page-fetch attempt, success or failure -- see
    docs/ROADMAP.md module 3's raw_snapshot sub-concern. Persisted by
    pipeline.py::_run_web_crawler into models/source.py's
    RawPageSnapshot once this crawl's SourceRun exists (this dataclass
    itself has no DB dependency, matching the rest of this module).
    """

    url: str
    final_url: str
    status_code: int | None
    content_type: str
    html: str | None
    fetch_error: str


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


class WebCrawler:
    def __init__(self, settings: Settings):
        self.settings = settings
        # Populated by _fetch as a side effect of crawl() -- one entry per
        # page fetch attempted (success or failure), read by
        # pipeline.py::_run_web_crawler after crawl() returns. Not part of
        # crawl()'s return value itself so its signature (and every
        # existing test/caller that mocks WebCrawler.crawl wholesale)
        # stays unchanged.
        self.snapshots: list[PageSnapshot] = []

    async def crawl(self, seeds: list[str]) -> list[Lead]:
        headers = {
            "User-Agent": self.settings.user_agent,
            "Accept": "text/html,application/xhtml+xml",
        }
        timeout = httpx.Timeout(self.settings.request_timeout_seconds)
        limits = httpx.Limits(
            max_connections=max(2, self.settings.concurrency * 2),
            max_keepalive_connections=max(1, self.settings.concurrency),
        )
        async with httpx.AsyncClient(
            headers=headers,
            timeout=timeout,
            limits=limits,
            follow_redirects=True,
        ) as client:
            robots = RobotsCache(client, self.settings.user_agent)
            limiter = DomainRateLimiter(self.settings.delay_seconds)
            semaphore = asyncio.Semaphore(self.settings.concurrency)
            queue = deque(CrawlItem(url=self._normalize_seed(seed), depth=0) for seed in seeds)
            seen: set[str] = set()
            pages_by_domain: dict[str, int] = defaultdict(int)
            leads_by_domain: dict[str, Lead] = {}

            while queue:
                batch: list[CrawlItem] = []
                while queue and len(batch) < self.settings.concurrency:
                    item = queue.popleft()
                    if item.url in seen:
                        continue
                    domain = self._domain(item.url)
                    if pages_by_domain[domain] >= self.settings.max_pages_per_domain:
                        continue
                    seen.add(item.url)
                    pages_by_domain[domain] += 1
                    batch.append(item)

                results = await asyncio.gather(
                    *(self._fetch(client, robots, limiter, semaphore, item) for item in batch),
                    return_exceptions=True,
                )
                for item, result in zip(batch, results, strict=True):
                    if isinstance(result, Exception) or result is None:
                        continue
                    html, final_url = result
                    domain = self._domain(final_url)
                    page_lead, links = self._extract_lead(html, final_url)
                    if page_lead:
                        existing = leads_by_domain.get(domain)
                        leads_by_domain[domain] = self._merge(existing, page_lead)

                    if item.depth < self.settings.max_depth:
                        for link in candidate_internal_links(links, final_url):
                            if link not in seen:
                                queue.append(CrawlItem(link, item.depth + 1))

            return list(leads_by_domain.values())

    async def _fetch(
        self,
        client: httpx.AsyncClient,
        robots: RobotsCache,
        limiter: DomainRateLimiter,
        semaphore: asyncio.Semaphore,
        item: CrawlItem,
    ) -> tuple[str, str] | None:
        if not await robots.allowed(item.url):
            self._record_snapshot(item.url, "", None, "", None, "robots_disallowed")
            return None
        await limiter.wait(item.url)
        async with semaphore:
            try:
                async with client.stream("GET", item.url) as response:
                    response.raise_for_status()
                    final_url = str(response.url)
                    content_type = response.headers.get("content-type", "").lower()
                    if (
                        "text/html" not in content_type
                        and "application/xhtml+xml" not in content_type
                    ):
                        self._record_snapshot(
                            item.url,
                            final_url,
                            response.status_code,
                            content_type,
                            None,
                            "non_html_content_type",
                        )
                        return None
                    chunks: list[bytes] = []
                    size = 0
                    async for chunk in response.aiter_bytes():
                        size += len(chunk)
                        if size > self.settings.max_response_bytes:
                            self._record_snapshot(
                                item.url,
                                final_url,
                                response.status_code,
                                content_type,
                                None,
                                "response_too_large",
                            )
                            return None
                        chunks.append(chunk)
                    encoding = response.encoding or "utf-8"
                    html = b"".join(chunks).decode(encoding, errors="replace")
                    self._record_snapshot(
                        item.url, final_url, response.status_code, content_type, html, ""
                    )
                    return html, final_url
            except httpx.HTTPStatusError as e:
                self._record_snapshot(
                    item.url,
                    str(e.response.url),
                    e.response.status_code,
                    "",
                    None,
                    f"http_error: {e.response.status_code}",
                )
                return None
            except (httpx.HTTPError, UnicodeError) as e:
                self._record_snapshot(item.url, "", None, "", None, f"{type(e).__name__}: {e}")
                return None

    def _record_snapshot(
        self,
        url: str,
        final_url: str,
        status_code: int | None,
        content_type: str,
        html: str | None,
        fetch_error: str,
    ) -> None:
        self.snapshots.append(
            PageSnapshot(
                url=url,
                final_url=final_url,
                status_code=status_code,
                content_type=content_type,
                html=html,
                fetch_error=fetch_error,
            )
        )

    def _extract_lead(self, html: str, url: str) -> tuple[Lead | None, list[str]]:
        text = visible_text(html)
        identity = extract_page_identity(html, url)
        emails = extract_emails(text, html)
        phones = extract_phones(text)
        links = extract_links(html, url)
        social_profiles = extract_social_profiles(links)
        matched_needles = [*self.settings.keywords, *self.settings.intent_terms]

        if not any([emails, phones, social_profiles, identity["organization"]]):
            return None, links

        lead = Lead(
            source="website",
            source_url=url,
            name=identity["name"],
            organization=identity["organization"],
            title=identity["title"],
            email=emails[0] if emails else "",
            phone=phones[0] if phones else "",
            website=f"{urlparse(url).scheme}://{urlparse(url).netloc}",
            location=identity["location"],
            social_profiles=social_profiles,
            evidence=best_evidence(text, matched_needles),
            raw={
                "description": identity["description"],
                "all_emails": emails,
                "all_phones": phones,
                "pages": [url],
                # Rule-based pain-point/buying-signal detection (see
                # enrichment/technology_detector.py) -- carried through
                # raw_payload so pipeline.py can materialize it into real
                # Signal rows once this page's record resolves to an
                # institution (institution_id doesn't exist yet here).
                "detected_signals": detect_technology_signals(text),
            },
        )
        return lead, links

    @staticmethod
    def _merge(existing: Lead | None, incoming: Lead) -> Lead:
        if existing is None:
            return incoming
        existing.name = existing.name or incoming.name
        existing.organization = existing.organization or incoming.organization
        existing.title = existing.title or incoming.title
        existing.email = existing.email or incoming.email
        existing.phone = existing.phone or incoming.phone
        existing.location = existing.location or incoming.location
        existing.evidence = existing.evidence or incoming.evidence
        existing.social_profiles = sorted(set(existing.social_profiles + incoming.social_profiles))
        existing.raw["all_emails"] = sorted(
            set(existing.raw.get("all_emails", []) + incoming.raw.get("all_emails", []))
        )
        existing.raw["all_phones"] = sorted(
            set(existing.raw.get("all_phones", []) + incoming.raw.get("all_phones", []))
        )
        existing.raw["pages"] = sorted(
            set(existing.raw.get("pages", []) + incoming.raw.get("pages", []))
        )
        # Dicts aren't hashable, so dedupe by (signal_type, text) instead of
        # the set()-based approach the other raw[] lists above use.
        merged_signals = {
            (s["signal_type"], s["text"]): s
            for s in [
                *existing.raw.get("detected_signals", []),
                *incoming.raw.get("detected_signals", []),
            ]
        }
        existing.raw["detected_signals"] = list(merged_signals.values())
        return existing

    @staticmethod
    def _normalize_seed(seed: str) -> str:
        seed = seed.strip()
        if not seed.startswith(("http://", "https://")):
            seed = f"https://{seed}"
        return seed

    @staticmethod
    def _domain(url: str) -> str:
        return urlparse(url).netloc.lower().removeprefix("www.")
