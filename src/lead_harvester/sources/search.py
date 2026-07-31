from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass(slots=True)
class SearchResult:
    title: str
    url: str
    description: str = ""


class BraveSearchSource:
    endpoint = "https://api.search.brave.com/res/v1/web/search"

    def __init__(self, api_key: str, timeout_seconds: float = 12.0):
        if not api_key:
            raise ValueError("BRAVE_SEARCH_API_KEY is required for query discovery")
        self.api_key = api_key
        # An instance attribute (mirrors sources/google_places.py's
        # self.client) rather than a per-call `async with
        # httpx.AsyncClient(...)` block -- tests can swap this for a
        # MockTransport-backed client the same way they do for the other
        # connectors, instead of needing to patch httpx itself.
        self.client = httpx.AsyncClient(timeout=timeout_seconds)

    async def search(
        self,
        query: str,
        count: int = 20,
        country: str = "PK",
        search_lang: str = "en",
    ) -> list[SearchResult]:
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key,
        }
        params = {
            "q": query,
            "count": max(1, min(count, 20)),
            "country": country,
            "search_lang": search_lang,
            "safesearch": "strict",
            "extra_snippets": "true",
        }
        response = await self.client.get(self.endpoint, headers=headers, params=params)
        response.raise_for_status()
        payload = response.json()
        return [
            SearchResult(
                title=str(item.get("title", "")),
                url=str(item.get("url", "")),
                description=str(item.get("description", "")),
            )
            for item in payload.get("web", {}).get("results", [])
            if item.get("url")
        ]
