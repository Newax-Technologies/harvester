"""Read access to Signal rows -- see docs/ROADMAP.md module 1 ("Entity Registry")."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.signal import Signal, SignalType


async def list_signals(
    session: AsyncSession,
    *,
    institution_id: uuid.UUID | None = None,
    signal_type: SignalType | None = None,
    limit: int = 100,
) -> list[Signal]:
    stmt = select(Signal).order_by(Signal.detected_at.desc()).limit(limit)
    if institution_id is not None:
        stmt = stmt.where(Signal.institution_id == institution_id)
    if signal_type is not None:
        stmt = stmt.where(Signal.signal_type == signal_type)
    return list(await session.scalars(stmt))
