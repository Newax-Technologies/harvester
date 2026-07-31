import time
from typing import Any

import httpx
import jwt

APPLE_MAPS_TOKEN_URL = "https://maps-api.apple.com/v1/token"
APPLE_MAPS_SEARCH_URL = "https://maps-api.apple.com/v1/search"

# Apple issues access tokens with a short TTL (typically 30 minutes) --
# refresh a bit early rather than racing a request against expiry.
_ACCESS_TOKEN_REFRESH_MARGIN_SECONDS = 60


class AppleMapsConnector:
    """
    Apple MapKit Server API (https://developer.apple.com/documentation/
    applemapsserverapi). Unlike Google Places/Yandex, there is no single
    long-lived API key: a developer JWT is signed locally (ES256, using the
    private key downloaded once from App Store Connect) and exchanged for a
    short-lived access token, which is what actually authorizes /v1/search
    calls. This connector signs the developer JWT itself (no network call)
    and caches the exchanged access token until it's close to expiring.

    Known v1 limitation: Apple's /v1/search response carries name/address/
    coordinate only -- no phone number or website field like Google
    Places/Yandex return. process_apple_place (pipeline.py) reflects that;
    those fields are simply absent for Apple-sourced records.
    """

    def __init__(self, team_id: str, key_id: str, private_key: str):
        if not team_id or not key_id or not private_key:
            raise ValueError(
                "APPLE_MAPS_TEAM_ID, APPLE_MAPS_KEY_ID, and APPLE_MAPS_PRIVATE_KEY are all "
                "required."
            )
        self.team_id = team_id
        self.key_id = key_id
        self.private_key = private_key
        self.client = httpx.Client(timeout=10.0)
        self._access_token: str | None = None
        self._access_token_expires_at: float = 0.0

    def _developer_token(self) -> str:
        now = int(time.time())
        return jwt.encode(
            {"iss": self.team_id, "iat": now, "exp": now + 3600},
            self.private_key,
            algorithm="ES256",
            headers={"kid": self.key_id, "typ": "JWT"},
        )

    def _get_access_token(self) -> str:
        if self._access_token and time.monotonic() < self._access_token_expires_at:
            return self._access_token

        response = self.client.get(
            APPLE_MAPS_TOKEN_URL,
            headers={"Authorization": f"Bearer {self._developer_token()}"},
        )
        response.raise_for_status()
        data = response.json()
        self._access_token = data["accessToken"]
        expires_in = data.get("expiresInSeconds", 1800)
        self._access_token_expires_at = (
            time.monotonic() + expires_in - _ACCESS_TOKEN_REFRESH_MARGIN_SECONDS
        )
        return self._access_token

    def search(self, query: str, *, lang: str = "en-US") -> list[dict[str, Any]]:
        try:
            access_token = self._get_access_token()
            response = self.client.get(
                APPLE_MAPS_SEARCH_URL,
                params={"q": query, "lang": lang},
                headers={"Authorization": f"Bearer {access_token}"},
            )
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except httpx.HTTPError as e:
            print(f"Error fetching Apple Maps for query '{query}': {e}")
            return []
