from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import ResourceNotFoundError, StaleDataError
from lead_harvester.models.audit import AuditLog
from lead_harvester.models.outreach import DraftStatus, OutreachDraft
from lead_harvester.schemas.outreach import DraftDecisionRequest, DraftEditRequest


class DraftReviewService:
    @staticmethod
    async def get_draft(session: AsyncSession, draft_id: UUID) -> OutreachDraft:
        draft = await session.get(OutreachDraft, draft_id)
        if not draft:
            raise ResourceNotFoundError(str(draft_id))
        return draft

    @staticmethod
    async def edit_draft(
        session: AsyncSession, draft_id: UUID, req: DraftEditRequest, actor: str
    ) -> OutreachDraft:
        async with session.begin():
            stmt = select(OutreachDraft).where(OutreachDraft.id == draft_id).with_for_update()
            result = await session.execute(stmt)
            draft = result.scalar_one_or_none()

            if not draft:
                raise ResourceNotFoundError(str(draft_id))

            if draft.version != req.expected_version:
                raise StaleDataError(
                    resource_id=str(draft_id),
                    expected_version=req.expected_version,
                    current_version=draft.version,
                )

            previous_body = draft.body
            draft.body = req.message
            draft.version += 1

            audit = AuditLog(
                action="draft.edited",
                actor=actor,
                entity_type="OutreachDraft",
                entity_id=str(draft.id),
                previous_state={"body": previous_body},
                new_state={"body": draft.body},
            )

            session.add(audit)
            await session.flush()

        return draft

    @staticmethod
    async def make_decision(
        session: AsyncSession, draft_id: UUID, req: DraftDecisionRequest, actor: str
    ) -> OutreachDraft:
        async with session.begin():
            stmt = select(OutreachDraft).where(OutreachDraft.id == draft_id).with_for_update()
            result = await session.execute(stmt)
            draft = result.scalar_one_or_none()

            if not draft:
                raise ResourceNotFoundError(str(draft_id))

            if draft.version != req.expected_version:
                raise StaleDataError(
                    resource_id=str(draft_id),
                    expected_version=req.expected_version,
                    current_version=draft.version,
                )

            previous_status = draft.status

            if req.decision == "approved":
                draft.status = DraftStatus.APPROVED
            elif req.decision == "rejected":
                draft.status = DraftStatus.NEEDS_REVISION
            else:
                raise ValueError("Invalid decision")

            draft.human_feedback = req.feedback
            draft.version += 1

            audit = AuditLog(
                action=f"draft.{req.decision}",
                actor=actor,
                entity_type="OutreachDraft",
                entity_id=str(draft.id),
                previous_state={"status": previous_status.value},
                new_state={"status": draft.status.value},
                feedback=req.feedback,
            )

            session.add(audit)
            await session.flush()

        return draft
