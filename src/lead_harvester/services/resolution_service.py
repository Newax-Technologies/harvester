from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import ResourceNotFoundError, StaleDataError
from lead_harvester.models.audit import AuditLog
from lead_harvester.models.resolution import ResolutionCandidate
from lead_harvester.schemas.resolution import ResolutionDecisionRequest


class ResolutionService:
    @staticmethod
    async def get_candidate(session: AsyncSession, review_id: UUID) -> ResolutionCandidate:
        candidate = await session.get(ResolutionCandidate, review_id)
        if not candidate:
            raise ResourceNotFoundError(str(review_id))
        return candidate

    @staticmethod
    async def make_decision(
        session: AsyncSession, review_id: UUID, req: ResolutionDecisionRequest, actor: str
    ) -> ResolutionCandidate:
        async with session.begin():
            stmt = (
                select(ResolutionCandidate)
                .where(ResolutionCandidate.id == review_id)
                .with_for_update()
            )
            result = await session.execute(stmt)
            candidate = result.scalar_one_or_none()

            if not candidate:
                raise ResourceNotFoundError(str(review_id))

            if candidate.version != req.expected_version:
                raise StaleDataError(
                    resource_id=str(review_id),
                    expected_version=req.expected_version,
                    current_version=candidate.version,
                )

            candidate.version += 1

            audit = AuditLog(
                action=f"resolution.{req.decision}",
                actor=actor,
                entity_type="ResolutionCandidate",
                entity_id=str(candidate.id),
                previous_state={},
                new_state={"decision": req.decision},
                feedback=req.feedback,
            )

            session.add(audit)
            await session.flush()

        return candidate
