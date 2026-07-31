import os
import httpx
from typing import Any

from .base import NormalizedRecord, SourceConnector
from .geographic_tiling import build_queries_for_tile, generate_tiles
from ..models.source import SourceType
from ..resolution.normalize import normalize_domain, normalize_name, normalize_phone

GOOGLE_PLACES_API_URL = "https://places.googleapis.com/v1/places:searchText"

class GooglePlacesConnector:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("GOOGLE_PLACES_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_PLACES_API_KEY is not set.")
        
        self.client = httpx.Client(
            headers={
                "X-Goog-Api-Key": self.api_key,
                "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.location,places.types,places.primaryType,places.businessStatus,places.nationalPhoneNumber,places.internationalPhoneNumber,places.websiteUri,places.rating,places.userRatingCount,places.regularOpeningHours,places.googleMapsUri"
            }
        )

    def search(self, query: str) -> list[dict[str, Any]]:
        payload = {
            "textQuery": query
        }
        
        try:
            response = self.client.post(GOOGLE_PLACES_API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("places", [])
        except httpx.HTTPError as e:
            print(f"Error fetching Google Places for query '{query}': {e}")
            return []


def _to_normalized_record(place: dict[str, Any]) -> NormalizedRecord | None:
    source_id = place.get("id")
    if not source_id:
        return None

    name = place.get("displayName", {}).get("text", "")
    phone = place.get("nationalPhoneNumber", "")
    website = place.get("websiteUri", "")

    loc = place.get("location", {})
    lat, lng = loc.get("latitude"), loc.get("longitude")
    location_wkt = f"SRID=4326;POINT({lng} {lat})" if lat is not None and lng is not None else None

    return NormalizedRecord(
        source_id=source_id,
        raw_payload=place,
        normalized_name=normalize_name(name),
        normalized_phone=normalize_phone(phone),
        normalized_domain=normalize_domain(website),
        location_wkt=location_wkt,
    )


class GooglePlacesSourceConnector(SourceConnector):
    """Adapter that fits GooglePlacesConnector into the shared SourceConnector interface."""

    source_type = SourceType.GOOGLE_PLACES

    def __init__(self, api_key: str | None = None):
        self.client = GooglePlacesConnector(api_key=api_key)

    async def fetch(self, job_config: dict[str, Any]) -> list[NormalizedRecord]:
        tiles = generate_tiles(job_config)
        categories = job_config.get("categories", ["FORMAL_EDUCATION"])

        records: list[NormalizedRecord] = []
        for tile in tiles:
            for query in build_queries_for_tile(tile, categories):
                for place in self.client.search(query):
                    record = _to_normalized_record(place)
                    if record is not None:
                        records.append(record)
        return records
