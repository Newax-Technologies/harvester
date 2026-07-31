"""
Web crawl orchestration -- docs/ROADMAP.md module 3 (Collection and
Crawling). Moved out of sources/web.py; see rate_limiter.py's docstring
for why. This module owns the crawl loop (queue, per-domain page caps,
depth limit, lead extraction/merging); robots/rate-limiting/fetching now
live in page_fetcher.py and rate_limiter.py instead of being inlined here.
"""

from __future__ import annotations

import asyncio
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

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
from .page_fetcher import RobotsCache, fetch_page
from .rate_limiter import DomainRateLimiter


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
                    *(
                        fetch_page(
                            client,
                            robots,
                            limiter,
                            semaphore,
                            item.url,
                            max_response_bytes=self.settings.max_response_bytes,
                        )
                        for item in batch
                    ),
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
