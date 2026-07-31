from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from lead_harvester.models.resolution import ResolutionCandidate, MatchAssessment, MatchDecision
from lead_harvester.models.audit import AuditLog
from lead_harvester.api.errors import ResourceNotFoundError, StaleDataError
from lead_harvester.schemas.resolution import ResolutionDecisionRequest

# Human-facing decision labels (from the review UI) mapped onto the MatchDecision enum
# stored on the candidate's MatchAssessment.
DECISION_MAP = {
    "same_business": MatchDecision.MERGE,
    "same_branch": MatchDecision.LINK_ONLY,
    "keep_separate": MatchDecision.REJECT,
}

class ResolutionService:
    @staticmethod
    async def get_candidate(session: AsyncSession, review_id: UUID) -> ResolutionCandidate:
        stmt = select(ResolutionCandidate).options(
            selectinload(ResolutionCandidate.assessments)
        ).where(ResolutionCandidate.id == review_id)
        candidate = (await session.execute(stmt)).scalar_one_or_none()
        if not candidate:
            raise ResourceNotFoundError(str(review_id))
        return candidate

    @staticmethod
    async def make_decision(session: AsyncSession, review_id: UUID, req: ResolutionDecisionRequest, actor: str) -> ResolutionCandidate:
        if req.decision not in DECISION_MAP:
            raise ValueError(f"Invalid decision: {req.decision!r}")

        async with session.begin():
            stmt = select(ResolutionCandidate).options(
                selectinload(ResolutionCandidate.assessments)
            ).where(ResolutionCandidate.id == review_id).with_for_update()
            result = await session.execute(stmt)
            candidate = result.scalar_one_or_none()

            if not candidate:
                raise ResourceNotFoundError(str(review_id))

            if candidate.version != req.expected_version:
                raise StaleDataError(resource_id=str(review_id), expected_version=req.expected_version, current_version=candidate.version)

            candidate.version += 1
            new_decision = DECISION_MAP[req.decision]

            latest_assessment = max(candidate.assessments, key=lambda a: a.assessed_at, default=None)
            if latest_assessment is not None:
                previous_decision = latest_assessment.decision
                latest_assessment.decision = new_decision
            else:
                previous_decision = None
                latest_assessment = MatchAssessment(
                    candidate_id=candidate.id,
                    decision=new_decision,
                )
                session.add(latest_assessment)

            audit = AuditLog(
                action=f"resolution.{req.decision}",
                actor=actor,
                entity_type="ResolutionCandidate",
                entity_id=str(candidate.id),
                previous_state={"decision": previous_decision.value if previous_decision else None},
                new_state={"decision": new_decision.value},
                feedback=req.feedback
            )

            session.add(audit)
            await session.flush()

        return candidate
