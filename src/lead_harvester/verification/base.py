from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from lead_harvester.models.verification import VerificationStatus


@dataclass(slots=True)
class VerificationOutcome:
    provider: str
    status: VerificationStatus
    is_disposable: bool = False
    is_role_account: bool = False
    mx_found: bool | None = None
    raw_response: dict[str, Any] = field(default_factory=dict)


class EmailVerificationProvider(ABC):
    """Shared adapter interface for anything that can assess an email address's deliverability."""

    name: str

    @abstractmethod
    async def verify(self, email: str) -> VerificationOutcome:
        raise NotImplementedError
