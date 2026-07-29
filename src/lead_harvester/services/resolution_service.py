from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from lead_harvester.api.errors import AlreadyReviewedError, ResourceNotFoundError, StaleDataError
from lead_harvester.canonical.merger import (
    attach_record_to_institution,
    display_fields,
    find_branch_for_raw_record,
    find_canonical_for_raw_record,
    merge_records,
)
from lead_harvester.models.audit import AuditLog
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.resolution import (
    MatchAssessment,
    MatchDecision,
    ResolutionCandidate,
    ReviewOutcome,
)
from lead_harvester.models.source import RawSourceRecord
from lead_harvester.schemas.resolution import ResolutionDecisionRequest

_OUTCOME_BY_DECISION = {
    "merge": ReviewOutcome.MERGED,
    "branch": ReviewOutcome.BRANCHED,
    "separate": ReviewOutcome.SEPARATED,
}


class ResolutionService:
    @staticmethod
    async def get_candidate(session: AsyncSession, review_id: UUID) -> ResolutionCandidate:
        stmt = (
            select(ResolutionCandidate)
            .options(selectinload(ResolutionCandidate.assessments))
            .where(ResolutionCandidate.id == review_id)
        )
        result = await session.execute(stmt)
        candidate = result.scalar_one_or_none()
        if not candidate:
            raise ResourceNotFoundError(str(review_id))
        return candidate

    @staticmethod
    async def list_pending(session: AsyncSession) -> list[dict]:
        """
        Candidates the automated scorer couldn't confidently resolve
        (MatchDecision.PENDING) and that no human has acted on yet
        (review_outcome is still null) -- shape matches
        frontend/src/pages/ResolutionQueue.tsx.
        """
        stmt = select(ResolutionCandidate, MatchAssessment).join(
            MatchAssessment, MatchAssessment.candidate_id == ResolutionCandidate.id
        )
        stmt = stmt.where(
            MatchAssessment.decision == MatchDecision.PENDING,
            ResolutionCandidate.review_outcome.is_(None),
        )
        result = await session.execute(stmt)

        summaries = []
        for candidate, assessment in result.all():
            record = await session.get(RawSourceRecord, candidate.raw_record_id)
            candidate_name = display_fields(record)["name"] if record else "Unknown"
            target_name = await _target_display_name(session, candidate)

            summaries.append(
                {
                    "id": candidate.id,
                    "candidateName": candidate_name,
                    "targetName": target_name,
                    "strategy": candidate.blocking_strategy,
                    "score": assessment.total_score,
                }
            )
        return summaries

    @staticmethod
    async def get_review_detail(session: AsyncSession, review_id: UUID) -> dict:
        candidate = await ResolutionService.get_candidate(session, review_id)
        return await _assemble_detail(session, candidate)

    @staticmethod
    async def make_decision(
        session: AsyncSession, review_id: UUID, req: ResolutionDecisionRequest, actor: str
    ) -> dict:
        if req.decision not in _OUTCOME_BY_DECISION:
            raise ValueError(
                f"Invalid decision {req.decision!r}: must be one of {sorted(_OUTCOME_BY_DECISION)}"
            )

        async with session.begin():
            stmt = (
                select(ResolutionCandidate)
                .options(selectinload(ResolutionCandidate.assessments))
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

            # A version match alone doesn't rule out "already decided" -- the
            # client could have fetched the post-decision version and
            # resubmitted. Without this, a second decision would merge/
            # attach/separate the same record again, creating a duplicate
            # institution or double-attaching it.
            if candidate.review_outcome is not None:
                raise AlreadyReviewedError(str(review_id), candidate.review_outcome.value)

            await _apply_decision(session, candidate, req.decision)

            candidate.review_outcome = _OUTCOME_BY_DECISION[req.decision]
            candidate.version += 1

            audit = AuditLog(
                action=f"resolution.{req.decision}",
                actor=actor,
                entity_type="ResolutionCandidate",
                entity_id=str(candidate.id),
                previous_state={"review_outcome": None},
                new_state={"review_outcome": candidate.review_outcome.value},
                feedback=req.feedback,
            )

            session.add(audit)
            await session.flush()

            # Assembled while still inside this transaction (rather than via
            # a second, separate call after this block exits) so the
            # session doesn't end the request sitting on a dangling
            # autobegin transaction -- which would break a subsequent
            # request sharing this session, as happens under the test
            # client's shared-session dependency override.
            detail = await _assemble_detail(session, candidate)

        return detail


async def _assemble_detail(session: AsyncSession, candidate: ResolutionCandidate) -> dict:
    record = await session.get(RawSourceRecord, candidate.raw_record_id)
    fields = display_fields(record) if record else {}
    best_score = max((a.total_score for a in candidate.assessments), default=0.0)

    return {
        "id": candidate.id,
        "raw_record_id": candidate.raw_record_id,
        "target_canonical_id": candidate.target_canonical_id,
        "target_raw_record_id": candidate.target_raw_record_id,
        "blocking_strategy": candidate.blocking_strategy,
        "version": candidate.version,
        "created_at": candidate.created_at,
        "assessments": candidate.assessments,
        "confidence_score": best_score,
        "incoming_data": {
            "name": fields.get("name"),
            "address": fields.get("address"),
            "phone": record.normalized_phone if record else None,
            "website": fields.get("website"),
        },
    }


async def _target_display_name(session: AsyncSession, candidate: ResolutionCandidate) -> str:
    if candidate.target_raw_record_id:
        target_record = await session.get(RawSourceRecord, candidate.target_raw_record_id)
        if target_record:
            return display_fields(target_record)["name"]
    elif candidate.target_canonical_id:
        institution = await session.get(CanonicalInstitution, candidate.target_canonical_id)
        if institution:
            return institution.canonical_name
    return "Unknown"


async def _apply_decision(
    session: AsyncSession, candidate: ResolutionCandidate, decision: str
) -> None:
    """
    Mutates the actual entity data per the human's decision -- until this
    was added, make_decision only wrote an AuditLog row and never touched
    any CanonicalInstitution/Branch/ContactPoint.
    """
    record = await session.get(RawSourceRecord, candidate.raw_record_id)
    matched_record = None
    if candidate.target_raw_record_id:
        matched_record = await session.get(RawSourceRecord, candidate.target_raw_record_id)

    if decision == "separate":
        # Confidently distinct: the incoming record gets its own institution.
        # The matched record (if any) is left untouched.
        await merge_records(session, [record])
        return

    if matched_record is None:
        # "merge"/"branch" both require something to attach to; without a
        # raw-record match there is nothing to merge or branch onto.
        raise ValueError(f"Cannot apply decision {decision!r} without a matched record")

    existing_canonical_id = await find_canonical_for_raw_record(session, matched_record.id)
    same_location = decision == "merge"

    if existing_canonical_id is not None:
        institution = await session.get(CanonicalInstitution, existing_canonical_id)
        target_branch = None
        if same_location:
            target_branch = await find_branch_for_raw_record(
                session, institution.id, matched_record
            )
        await attach_record_to_institution(
            session, record, institution, target_branch=target_branch
        )
        return

    await merge_records(session, [record, matched_record], same_location=same_location)
