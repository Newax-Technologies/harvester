from __future__ import annotations

import asyncio
import dataclasses
from collections import defaultdict, deque
from dataclasses import dataclass
import time
from typing import Any
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx

from ..config import Settings
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
from ..models.source import SourceType
from .base import NormalizedRecord, SourceConnector
from .search import BraveSearchSource
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
            return None
        await limiter.wait(item.url)
        async with semaphore:
            try:
                async with client.stream("GET", item.url) as response:
                    response.raise_for_status()
                    content_type = response.headers.get("content-type", "").lower()
                    if "text/html" not in content_type and "application/xhtml+xml" not in content_type:
                        return None
                    chunks: list[bytes] = []
                    size = 0
                    async for chunk in response.aiter_bytes():
                        size += len(chunk)
                        if size > self.settings.max_response_bytes:
                            return None
                        chunks.append(chunk)
                    encoding = response.encoding or "utf-8"
                    return b"".join(chunks).decode(encoding, errors="replace"), str(response.url)
            except (httpx.HTTPError, UnicodeError):
                return None

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


class WebSourceConnector(SourceConnector):
    """
    Adapter that fits WebCrawler into the shared SourceConnector interface.

    job_config["seeds"] are crawled directly. job_config["queries"] are first
    resolved to URLs via the Brave Search API (an official, ToS-compliant
    search API), and those discovered URLs are crawled the same way.
    """

    source_type = SourceType.WEBSITE

    def __init__(self, settings: Settings, brave_search_api_key: str | None = None):
        self.settings = settings
        self.brave_search_api_key = brave_search_api_key

    async def _discover_seeds_from_queries(self, queries: list[str], count_per_query: int) -> list[str]:
        if not queries or not self.brave_search_api_key:
            return []
        brave = BraveSearchSource(api_key=self.brave_search_api_key)
        discovered: list[str] = []
        for query in queries:
            results = await brave.search(query, count=count_per_query)
            discovered.extend(result.url for result in results)
        return discovered

    async def fetch(self, job_config: dict[str, Any]) -> list[NormalizedRecord]:
        seeds = list(job_config.get("seeds", []))
        queries = job_config.get("queries", [])
        seeds.extend(
            await self._discover_seeds_from_queries(queries, job_config.get("count_per_query", 10))
        )

        if not seeds:
            return []

        crawler = WebCrawler(self.settings)
        leads = await crawler.crawl(seeds)

        return [
            NormalizedRecord(
                source_id=lead.website or lead.source_url,
                raw_payload=dataclasses.asdict(lead),
                normalized_name=lead.organization or lead.name or None,
                normalized_phone=lead.phone or None,
                normalized_domain=lead.website or None,
                location_wkt=None,
            )
            for lead in leads
        ]
