from __future__ import annotations

from dataclasses import dataclass
from typing import Any

@dataclass(slots=True)
class ContactPoint:
    id: str
    institution_id: str
    person_name: str = ""
    role: str = ""
    email: str = ""
    phone: str = ""
    whatsapp: str = ""
    contact_form_url: str = ""
    telegram_username: str = ""
    source: str = ""
    publicly_listed: bool = False
    verified_at: str = ""

    def to_db_tuple(self) -> tuple[Any, ...]:
        return (
            self.id,
            self.institution_id,
            self.person_name,
            self.role,
            self.email,
            self.phone,
            self.whatsapp,
            self.contact_form_url,
            self.telegram_username,
            self.source,
            int(self.publicly_listed),
            self.verified_at
        )
