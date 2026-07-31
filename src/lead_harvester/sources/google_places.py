import os
from typing import Any

import httpx

GOOGLE_PLACES_API_URL = "https://places.googleapis.com/v1/places:searchText"


class GooglePlacesConnector:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("GOOGLE_PLACES_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_PLACES_API_KEY is not set.")

        self.client = httpx.Client(
            headers={
                "X-Goog-Api-Key": self.api_key,
                "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.location,places.types,places.primaryType,places.businessStatus,places.nationalPhoneNumber,places.internationalPhoneNumber,places.websiteUri,places.rating,places.userRatingCount,places.regularOpeningHours,places.googleMapsUri",
            }
        )

    def search(self, query: str) -> list[dict[str, Any]]:
        payload = {"textQuery": query}

        try:
            response = self.client.post(GOOGLE_PLACES_API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("places", [])
        except httpx.HTTPError as e:
            print(f"Error fetching Google Places for query '{query}': {e}")
            return []
