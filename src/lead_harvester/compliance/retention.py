from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.source import RawSourceRecord


class RetentionService:
    """
    Ages out raw scraped payloads that were never merged into a
    CanonicalInstitution -- once a raw record has been merged, it's kept
    indefinitely as provenance for the canonical data it helped build, but
    unmerged raw leads (duplicates, rejected matches, low-value hits) have no
    ongoing business purpose past the retention window.
    """

    @staticmethod
    async def purge_expired(session: AsyncSession, retention_days: int) -> int:
        cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)

        has_provenance = select(FieldProvenance.id).where(FieldProvenance.raw_record_id == RawSourceRecord.id)
        stmt = select(RawSourceRecord).where(
            RawSourceRecord.extracted_at < cutoff,
            ~exists(has_provenance),
        )
        expired = (await session.execute(stmt)).scalars().all()

        for record in expired:
            await session.delete(record)

        await session.commit()
        return len(expired)
