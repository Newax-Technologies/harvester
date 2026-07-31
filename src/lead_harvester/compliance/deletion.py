from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.canonical import ContactPoint
from lead_harvester.models.compliance import DeletionRequest, DeletionRequestStatus, IdentifierType, SuppressionReason
from lead_harvester.models.outreach import OutreachDraft
from lead_harvester.models.source import RawSourceRecord
from .suppression import SuppressionService, normalize_identifier


class DeletionService:
    """
    Handles right-to-be-forgotten / opt-out requests. Processing a request:
      1. Deletes matching ContactPoints (email/phone) and any OutreachDraft
         targeting that value.
      2. Purges matching raw ledger records -- only possible for phone/domain,
         since RawSourceRecord doesn't index email out of its unstructured
         raw_payload JSON; this limitation is recorded in the request notes.
      3. Adds a SuppressionEntry so the identifier can't silently re-enter the
         pipeline on a future re-scrape.
    """

    @staticmethod
    async def request_deletion(
        session: AsyncSession, identifier_type: IdentifierType, value: str, notes: str = ""
    ) -> DeletionRequest:
        request = DeletionRequest(
            identifier_type=identifier_type,
            identifier_value=normalize_identifier(identifier_type, value),
            notes=notes,
        )
        session.add(request)
        return request

    @staticmethod
    async def process_pending(session: AsyncSession, limit: int = 50) -> int:
        stmt = select(DeletionRequest).where(DeletionRequest.status == DeletionRequestStatus.PENDING).limit(limit)
        requests = (await session.execute(stmt)).scalars().all()

        for request in requests:
            await DeletionService._process_one(session, request)

        await session.commit()
        return len(requests)

    @staticmethod
    async def _process_one(session: AsyncSession, request: DeletionRequest) -> None:
        try:
            counts: dict[str, int | str] = {}

            if request.identifier_type in (IdentifierType.EMAIL, IdentifierType.PHONE):
                contacts_stmt = select(ContactPoint).where(
                    ContactPoint.contact_type == request.identifier_type.value,
                    ContactPoint.contact_value == request.identifier_value,
                )
                contacts = (await session.execute(contacts_stmt)).scalars().all()
                for contact in contacts:
                    await session.delete(contact)
                counts["contact_points"] = len(contacts)

            drafts_stmt = select(OutreachDraft).where(OutreachDraft.target_contact_value == request.identifier_value)
            drafts = (await session.execute(drafts_stmt)).scalars().all()
            for draft in drafts:
                await session.delete(draft)
            counts["outreach_drafts"] = len(drafts)

            if request.identifier_type == IdentifierType.PHONE:
                raw_stmt = select(RawSourceRecord).where(RawSourceRecord.normalized_phone == request.identifier_value)
                raw_records = (await session.execute(raw_stmt)).scalars().all()
                for record in raw_records:
                    await session.delete(record)
                counts["raw_source_records"] = len(raw_records)
            elif request.identifier_type == IdentifierType.DOMAIN:
                raw_stmt = select(RawSourceRecord).where(RawSourceRecord.normalized_domain == request.identifier_value)
                raw_records = (await session.execute(raw_stmt)).scalars().all()
                for record in raw_records:
                    await session.delete(record)
                counts["raw_source_records"] = len(raw_records)
            else:
                counts["raw_source_records"] = "not purged: email isn't an indexed column on RawSourceRecord's raw payload"

            await SuppressionService.suppress(
                session,
                request.identifier_type,
                request.identifier_value,
                SuppressionReason.LEGAL_REQUEST,
                note=f"Auto-suppressed from deletion request {request.id}",
            )

            request.status = DeletionRequestStatus.COMPLETED
            request.completed_at = datetime.now(timezone.utc)
            request.notes = f"{request.notes}\nDeleted: {counts}".strip()
        except Exception as e:
            request.status = DeletionRequestStatus.FAILED
            request.notes = f"{request.notes}\nError: {e}".strip()
