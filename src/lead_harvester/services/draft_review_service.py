from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import DraftBeingSentError, ResourceNotFoundError, StaleDataError
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

            # OutreachAutomator.run() claims a draft to SENDING (SELECT ...
            # FOR UPDATE SKIP LOCKED, flipped in the same transaction) and
            # loads its body into memory before that claim's own commit --
            # without this check, a reviewer's concurrent edit using the
            # version they loaded before the claim would still pass the
            # version check below (claiming to SENDING doesn't bump
            # version) and silently mutate a body the automator has
            # already read and is actively sending, leaving the database
            # record content different from what was actually delivered.
            # SENT is included too: the SENDING -> SENT transition ALSO
            # doesn't bump version (see _mark_sent), so a stale-version
            # request loaded before the send still passes the version
            # check below and could rewrite the recorded body of a message
            # that has already been delivered.
            if draft.status in (DraftStatus.SENDING, DraftStatus.SENT):
                raise DraftBeingSentError(str(draft_id))

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

            # See the matching check in edit_draft above: a draft already
            # claimed by OutreachAutomator.run() (or already delivered)
            # must not have its status changed out from under the send --
            # otherwise a stale-version decision could move an already-SENT
            # draft back to APPROVED and have it sent a second time.
            if draft.status in (DraftStatus.SENDING, DraftStatus.SENT):
                raise DraftBeingSentError(str(draft_id))

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
