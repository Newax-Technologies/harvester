from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.canonical import CanonicalInstitution, ContactPoint
from lead_harvester.models.crm import CRMSyncRecord, CRMSyncStatus
from lead_harvester.models.outreach import AccountBrief, DraftStatus, OutreachDraft
from .base import CRMConnector, CRMContact, CRMSyncPayload


class CRMSyncService:
    """
    Pushes institutions to an external CRM once a human has approved outreach
    for them (DraftStatus.APPROVED or later) -- syncing happens after, never
    before, human review. Re-runs are safe: already-synced institutions are
    skipped, and failed syncs are retried on the next pass.
    """

    def __init__(self, connector: CRMConnector):
        self.connector = connector

    async def sync_pending(self, session: AsyncSession, limit: int = 50) -> int:
        stmt = (
            select(CanonicalInstitution)
            .join(AccountBrief, AccountBrief.institution_id == CanonicalInstitution.id)
            .join(OutreachDraft, OutreachDraft.brief_id == AccountBrief.id)
            .where(OutreachDraft.status.in_([DraftStatus.APPROVED, DraftStatus.SENT]))
            .distinct()
            .limit(limit)
        )
        institutions = (await session.execute(stmt)).scalars().all()

        synced = 0
        for institution in institutions:
            record = await self._get_sync_record(session, institution.id)
            if record is not None and record.status == CRMSyncStatus.SYNCED:
                continue
            await self.sync_institution(session, institution, record)
            synced += 1

        await session.commit()
        return synced

    async def _get_sync_record(self, session: AsyncSession, institution_id) -> CRMSyncRecord | None:
        stmt = select(CRMSyncRecord).where(
            CRMSyncRecord.institution_id == institution_id,
            CRMSyncRecord.provider == self.connector.name,
        )
        return (await session.execute(stmt)).scalar_one_or_none()

    async def sync_institution(
        self, session: AsyncSession, institution: CanonicalInstitution, record: CRMSyncRecord | None = None
    ) -> CRMSyncRecord:
        contacts_stmt = select(ContactPoint).where(ContactPoint.institution_id == institution.id)
        contact_points = (await session.execute(contacts_stmt)).scalars().all()

        record = record or CRMSyncRecord(institution_id=institution.id, provider=self.connector.name)

        payload = CRMSyncPayload(
            institution_name=institution.canonical_name,
            domain=institution.domain,
            website=institution.website,
            contacts=[
                CRMContact(contact_type=c.contact_type, value=c.contact_value, person_name=c.person_name, role=c.role)
                for c in contact_points
            ],
            external_id=record.external_id,
        )

        try:
            outcome = await self.connector.upsert_company(payload)
            record.external_id = outcome.external_id
            record.raw_response = outcome.raw_response
            record.status = CRMSyncStatus.SYNCED
            record.last_synced_at = datetime.now(timezone.utc)
            record.last_error = None
        except Exception as e:
            record.status = CRMSyncStatus.FAILED
            record.last_error = str(e)

        session.add(record)
        return record
