from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Institution:
    id: str
    canonical_name: str
    institution_type: str = ""
    ownership_type: str = ""
    website: str = ""
    domain: str = ""
    primary_phone: str = ""
    primary_email: str = ""
    status: str = "OPERATIONAL"
    estimated_size: str = ""
    estimated_value_tier: str = ""
    confidence: float = 0.0
    discovered_at: str = ""
    raw_data: dict[str, Any] = field(default_factory=dict)

    def to_db_tuple(self) -> tuple[Any, ...]:
        import json

        return (
            self.id,
            self.canonical_name,
            self.institution_type,
            self.ownership_type,
            self.website,
            self.domain,
            self.primary_phone,
            self.primary_email,
            self.status,
            self.estimated_size,
            self.estimated_value_tier,
            self.confidence,
            self.discovered_at,
            json.dumps(self.raw_data, ensure_ascii=False),
        )
