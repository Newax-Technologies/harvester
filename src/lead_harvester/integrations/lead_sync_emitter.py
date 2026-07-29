"""
Lead sync webhook emitter (harvester -> core-newax)
====================================================
Fires a signed HTTP webhook whenever an institution is created/updated so
core-newax can mirror it into its CoreOrganization/CoreAddress/
CoreContactMethod tables via CoreExternalReference.

v1 delivery is fire-and-forget: a failed delivery is logged and swallowed,
never raised, since a webhook outage must never break the harvester write
path it's attached to. There is no retry/outbox yet -- a lost delivery is
lost, not queued. That durability gap is tracked as follow-up work, not
silently accepted as "fine".
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
import uuid
from datetime import UTC, datetime
from typing import Any

import httpx

from lead_harvester.config import Settings
from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint

SCHEMA_VERSION = 1
TIMESTAMP_HEADER = "X-Lead-Harvester-Timestamp"
SIGNATURE_HEADER = "X-Lead-Harvester-Signature"
# Must match core-newax's supported ContactType set. Filtered here (not just
# left to the receiver) so an unsupported type (e.g. "linkedin") never rides
# along in a fire-and-forget delivery that has no retry if the receiver
# rejects it -- see docs/ROADMAP.md's "Broader contact-type support" note.
SUPPORTED_CONTACT_TYPES = {"phone", "email", "whatsapp", "telegram"}


class LeadSyncEmitter:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def emit_institution_upserted(
        self,
        institution: CanonicalInstitution,
        branches: list[Branch],
        contact_points: list[ContactPoint],
    ) -> None:
        if not self.settings.lead_sync_enabled or not self.settings.lead_sync_webhook_url:
            return

        supported_contacts = []
        for contact in contact_points:
            if contact.contact_type in SUPPORTED_CONTACT_TYPES:
                supported_contacts.append(contact)
            else:
                print(
                    f"lead_sync: skipping contact {contact.id} with unsupported "
                    f"contact_type={contact.contact_type!r} for institution {institution.id}"
                )

        payload = self._build_payload(institution, branches, supported_contacts)
        body = json.dumps(payload, separators=(",", ":"))
        timestamp = str(int(time.time()))
        signature = self._sign(timestamp, body)

        try:
            async with httpx.AsyncClient(
                timeout=self.settings.lead_sync_webhook_timeout_seconds
            ) as client:
                response = await client.post(
                    self.settings.lead_sync_webhook_url,
                    content=body,
                    headers={
                        "Content-Type": "application/json",
                        TIMESTAMP_HEADER: timestamp,
                        SIGNATURE_HEADER: signature,
                    },
                )
                response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"lead_sync webhook delivery failed for institution {institution.id}: {e}")

    def _build_payload(
        self,
        institution: CanonicalInstitution,
        branches: list[Branch],
        contact_points: list[ContactPoint],
    ) -> dict[str, Any]:
        return {
            "schemaVersion": SCHEMA_VERSION,
            "eventId": str(uuid.uuid4()),
            "eventType": "institution.upserted",
            "occurredAt": self._isoformat_now(),
            "institution": {
                "id": str(institution.id),
                "canonicalName": institution.canonical_name,
                "institutionType": institution.institution_type,
                "domain": institution.domain,
                "website": institution.website,
                "status": self._enum_value(institution.status),
            },
            "branches": [
                {
                    "id": str(branch.id),
                    "branchName": branch.branch_name,
                    "address": branch.address,
                    "city": branch.city,
                    "countryCode": branch.country_code,
                }
                for branch in branches
            ],
            "contactPoints": [
                {
                    "id": str(contact.id),
                    "contactType": contact.contact_type,
                    "contactValue": contact.contact_value,
                    "personName": contact.person_name,
                    "role": contact.role,
                    "isPubliclyListed": contact.is_publicly_listed,
                }
                for contact in contact_points
            ],
        }

    def _sign(self, timestamp: str, body: str) -> str:
        message = f"{timestamp}.{body}".encode()
        return hmac.new(
            self.settings.lead_sync_webhook_secret.encode(), message, hashlib.sha256
        ).hexdigest()

    @staticmethod
    def _enum_value(value: Any) -> Any:
        return value.value if hasattr(value, "value") else value

    @staticmethod
    def _isoformat_now() -> str:
        return datetime.now(UTC).isoformat()
