"""
Re-emits a lead_sync event for an institution that was already synced at
least once (CanonicalInstitution.lead_synced_at is set) but has since been
updated by a resolution codepath (automated pipeline attach, or a reviewer
merge/branch decision) -- those codepaths don't hold the institution's
freshly-committed branches/contact_points in memory the way
api/routes/manual_leads.py does, so this re-reads current state by id from
a fresh session rather than relying on possibly-stale in-memory objects.
"""

from __future__ import annotations

import uuid

from sqlalchemy import select

from lead_harvester.database import get_session
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint


async def resync_institution(emitter: LeadSyncEmitter, institution_id: uuid.UUID) -> None:
    async with get_session() as session:
        institution = await session.get(CanonicalInstitution, institution_id)
        if institution is None:
            return

        branches = (
            (await session.execute(select(Branch).where(Branch.institution_id == institution_id)))
            .scalars()
            .all()
        )
        contact_points = (
            (
                await session.execute(
                    select(ContactPoint).where(ContactPoint.institution_id == institution_id)
                )
            )
            .scalars()
            .all()
        )
        await emitter.emit_institution_upserted(institution, list(branches), list(contact_points))
