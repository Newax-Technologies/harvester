from typing import Any

import httpx

YANDEX_SEARCH_API_URL = "https://search-maps.yandex.ru/v1/"


class YandexMapsConnector:
    """
    Yandex Maps Search API (org/places search by free-text query, returning
    a GeoJSON FeatureCollection) -- see
    https://yandex.com/dev/geosearch/doc/en/. Mirrors
    sources/google_places.py's shape (sync httpx.Client, single API key,
    a `search(query)` method) so pipeline.py can drive it the same way.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("YANDEX_MAPS_API_KEY is not set.")

        self.client = httpx.Client(timeout=10.0)

    def search(self, query: str, *, lang: str = "en_US", results: int = 20) -> list[dict[str, Any]]:
        params = {
            "apikey": self.api_key,
            "text": query,
            "lang": lang,
            "type": "biz",
            "results": max(1, min(results, 50)),
        }

        try:
            response = self.client.get(YANDEX_SEARCH_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("features", [])
        except httpx.HTTPError as e:
            print(f"Error fetching Yandex Maps for query '{query}': {e}")
            return []
