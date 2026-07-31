from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CRMContact:
    contact_type: str  # e.g. "phone", "email"
    value: str
    person_name: str | None = None
    role: str | None = None


@dataclass(slots=True)
class CRMSyncPayload:
    institution_name: str
    domain: str | None
    website: str | None
    contacts: list[CRMContact]
    # The CRM's own ID from a previous sync, if any -- lets a connector
    # decide whether to create a new record or update an existing one.
    external_id: str | None = None


@dataclass(slots=True)
class CRMSyncOutcome:
    external_id: str
    raw_response: dict[str, Any] = field(default_factory=dict)


class CRMConnector(ABC):
    """Shared adapter interface for pushing qualified institutions into an external CRM."""

    name: str

    @abstractmethod
    async def upsert_company(self, payload: CRMSyncPayload) -> CRMSyncOutcome:
        """Create or update the institution's record in the CRM and return its external ID."""
        raise NotImplementedError
