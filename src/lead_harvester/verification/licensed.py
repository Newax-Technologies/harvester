from __future__ import annotations

from typing import Any

import httpx

from lead_harvester.models.verification import VerificationStatus
from .base import EmailVerificationProvider, VerificationOutcome

_STATUS_MAP = {
    "valid": VerificationStatus.VALID,
    "deliverable": VerificationStatus.VALID,
    "invalid": VerificationStatus.INVALID,
    "undeliverable": VerificationStatus.INVALID,
    "risky": VerificationStatus.RISKY,
    "catch-all": VerificationStatus.RISKY,
    "unknown": VerificationStatus.UNKNOWN,
}


class LicensedEmailVerificationProvider(EmailVerificationProvider):
    """
    Generic adapter for a licensed email-verification API (e.g. ZeroBounce,
    NeverBounce, Kickbox). Exact response field names differ per provider --
    this expects a normalized JSON shape:

        {"status": "valid"|"invalid"|"risky"|"unknown",
         "is_disposable": bool, "is_role_account": bool, "mx_found": bool}

    If your provider's response looks different, adapt `_parse_response`
    rather than the calling code.
    """

    name = "licensed_provider"

    def __init__(self, api_url: str, api_key: str, timeout_seconds: float = 10.0):
        if not api_url or not api_key:
            raise ValueError("Licensed email verification requires both an API URL and an API key.")
        self.api_url = api_url
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    async def verify(self, email: str) -> VerificationOutcome:
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.get(
                self.api_url,
                params={"email": email},
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            response.raise_for_status()
            payload = response.json()

        return self._parse_response(payload)

    def _parse_response(self, payload: dict[str, Any]) -> VerificationOutcome:
        status = _STATUS_MAP.get(str(payload.get("status", "")).lower(), VerificationStatus.UNKNOWN)
        return VerificationOutcome(
            provider=self.name,
            status=status,
            is_disposable=bool(payload.get("is_disposable", False)),
            is_role_account=bool(payload.get("is_role_account", False)),
            mx_found=payload.get("mx_found"),
            raw_response=payload,
        )
