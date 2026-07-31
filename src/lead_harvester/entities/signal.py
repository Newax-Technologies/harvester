from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class OpportunitySignal:
    id: str
    institution_id: str
    signal_type: str = ""
    signal_text: str = ""
    source_url: str = ""
    detected_at: str = ""
    confidence: float = 0.0
    freshness: int = 0
    commercial_relevance: float = 0.0

    def to_db_tuple(self) -> tuple[Any, ...]:
        return (
            self.id,
            self.institution_id,
            self.signal_type,
            self.signal_text,
            self.source_url,
            self.detected_at,
            self.confidence,
            self.freshness,
            self.commercial_relevance,
        )
