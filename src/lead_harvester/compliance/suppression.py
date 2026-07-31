from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.compliance import IdentifierType, SuppressionEntry, SuppressionReason
from lead_harvester.resolution.normalize import normalize_domain, normalize_phone


def normalize_identifier(identifier_type: IdentifierType, value: str) -> str:
    """Matches the normalization already applied to ContactPoint/RawSourceRecord values."""
    if identifier_type == IdentifierType.PHONE:
        return normalize_phone(value)
    if identifier_type == IdentifierType.DOMAIN:
        return normalize_domain(value)
    return (value or "").strip().lower()


class SuppressionService:
    """Hard block list: anything here must never be selected as an outreach target."""

    @staticmethod
    async def is_suppressed(session: AsyncSession, identifier_type: IdentifierType, value: str | None) -> bool:
        if not value:
            return False
        stmt = select(SuppressionEntry.id).where(
            SuppressionEntry.identifier_type == identifier_type,
            SuppressionEntry.identifier_value == normalize_identifier(identifier_type, value),
        )
        return (await session.execute(stmt)).first() is not None

    @staticmethod
    async def suppress(
        session: AsyncSession,
        identifier_type: IdentifierType,
        value: str,
        reason: SuppressionReason,
        note: str = "",
    ) -> SuppressionEntry:
        normalized = normalize_identifier(identifier_type, value)
        existing_stmt = select(SuppressionEntry).where(
            SuppressionEntry.identifier_type == identifier_type,
            SuppressionEntry.identifier_value == normalized,
        )
        existing = (await session.execute(existing_stmt)).scalar_one_or_none()
        if existing is not None:
            existing.reason = reason
            if note:
                existing.note = note
            return existing

        entry = SuppressionEntry(identifier_type=identifier_type, identifier_value=normalized, reason=reason, note=note)
        session.add(entry)
        return entry
