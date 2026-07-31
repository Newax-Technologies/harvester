from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Branch:
    id: str
    institution_id: str
    branch_name: str = ""
    address: str = ""
    city: str = ""
    area: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    map_provider_ids: dict[str, str] = field(default_factory=dict)
    phones: list[str] = field(default_factory=list)
    opening_hours: str = ""

    def to_db_tuple(self) -> tuple[Any, ...]:
        import json

        return (
            self.id,
            self.institution_id,
            self.branch_name,
            self.address,
            self.city,
            self.area,
            self.latitude,
            self.longitude,
            json.dumps(self.map_provider_ids, ensure_ascii=False),
            json.dumps(self.phones, ensure_ascii=False),
            self.opening_hours,
        )
