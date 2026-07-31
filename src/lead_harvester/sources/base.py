from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from ..models.source import SourceType


@dataclass(slots=True)
class NormalizedRecord:
    """
    One record produced by a SourceConnector, ready to be persisted as a
    RawSourceRecord. Connectors do their own source-specific normalization;
    the pipeline just needs this common shape to write to the ledger.
    """
    source_id: str
    raw_payload: dict[str, Any]
    normalized_name: str | None = None
    normalized_phone: str | None = None
    normalized_domain: str | None = None
    location_wkt: str | None = None  # e.g. "SRID=4326;POINT(lng lat)"


class SourceConnector(ABC):
    """
    Shared adapter interface for official platform connectors (Google Places,
    Brave Search + web crawling, and future licensed APIs). Each connector
    knows how to talk to one external source and turn its results into
    NormalizedRecords; the pipeline persists them uniformly without needing
    to know source-specific details.
    """

    source_type: SourceType

    @abstractmethod
    async def fetch(self, job_config: dict[str, Any]) -> list[NormalizedRecord]:
        """Run one connector pass over the job config and return normalized records."""
        raise NotImplementedError
