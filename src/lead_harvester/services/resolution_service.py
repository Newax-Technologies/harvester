from uuid import UUID

from fastapi import BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from lead_harvester.api.errors import (
    AlreadyReviewedError,
    RecordAlreadyCanonicalizedError,
    ResourceNotFoundError,
    StaleDataError,
    TargetHasPendingConflictError,
)
from lead_harvester.canonical.merger import (
    attach_record_to_institution,
    display_fields,
    find_branch_for_raw_record,
    find_canonical_for_raw_record,
    merge_records,
)
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.integrations.lead_sync_resync import resync_institution
from lead_harvester.models.audit import AuditLog
from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.resolution import (
    MatchAssessment,
    MatchDecision,
    ResolutionCandidate,
    ReviewOutcome,
)
from lead_harvester.models.source import RawSourceRecord
from lead_harvester.resolution.orchestrator import _has_other_pending_candidate
from lead_harvester.schemas.resolution import ResolutionDecisionRequest
from lead_harvester.services.lead_profile_service import link_page_snapshots_to_institution

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
        already_canonicalized = (
            select(FieldProvenance.raw_record_id)
            .where(FieldProvenance.raw_record_id == ResolutionCandidate.raw_record_id)
            .exists()
        )
        stmt = select(ResolutionCandidate, MatchAssessment).join(
            MatchAssessment, MatchAssessment.candidate_id == ResolutionCandidate.id
        )
        stmt = stmt.where(
            MatchAssessment.decision == MatchDecision.PENDING,
            ResolutionCandidate.review_outcome.is_(None),
            # A sibling candidate for the same raw record (matched against a
            # different target) may already have been decided, or automated
            # resolution may have already canonicalized this record entirely
            # -- either way, merge_records/attach_record_to_institution
            # always write a "branch_membership" FieldProvenance row, so its
            # presence means this candidate is moot and shouldn't linger in
            # the queue as an item that will just 409 if acted on.
            ~already_canonicalized,
        )
        result = await session.execute(stmt)

        summaries = []
        for candidate, assessment in result.all():
            record = await session.get(RawSourceRecord, candidate.raw_record_id)
            candidate_name = display_fields(record)["name"] if record else "Unknown"
            target_name = (await _target_evidence(session, candidate))["name"]

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
        session: AsyncSession,
        review_id: UUID,
        req: ResolutionDecisionRequest,
        actor: str,
        *,
        background_tasks: BackgroundTasks | None = None,
        lead_sync_emitter: LeadSyncEmitter | None = None,
    ) -> dict:
        if req.decision not in _OUTCOME_BY_DECISION:
            raise ValueError(
                f"Invalid decision {req.decision!r}: must be one of {sorted(_OUTCOME_BY_DECISION)}"
            )

        resync_institution_id: UUID | None = None

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

            # Locking only this candidate row isn't enough to serialize
            # against a SIBLING candidate (a different ResolutionCandidate
            # row for the same raw_record_id, matched against a different
            # target -- OR a different candidate that happens to target the
            # SAME target_raw_record_id, e.g. two reviewers deciding
            # A->T and B->T concurrently). Either shape lets two concurrent
            # make_decision calls both pass the find_canonical_for_raw_record
            # check below before either commits, and both proceed to
            # canonicalize the same raw record -- so lock BOTH this
            # candidate's own raw_record_id and its target_raw_record_id (if
            # any). Locked together in one id-ordered query so two
            # transactions that both need to lock the same pair of rows
            # always acquire them in the same order, avoiding a deadlock.
            lock_ids = {candidate.raw_record_id}
            if candidate.target_raw_record_id is not None:
                lock_ids.add(candidate.target_raw_record_id)
            await session.execute(
                select(RawSourceRecord)
                .where(RawSourceRecord.id.in_(lock_ids))
                .order_by(RawSourceRecord.id)
                .with_for_update()
            )

            # The candidate itself may be unreviewed, but its raw record can
            # already be canonicalized -- via a sibling candidate (the same
            # record matched against a different target through a different
            # blocking strategy) that was already decided, or via automated
            # resolution picking a MERGE for a different candidate and
            # leaving this one PENDING. Either way, deciding this candidate
            # now would create a second institution for (or re-attach) an
            # already-canonicalized record.
            if await find_canonical_for_raw_record(session, candidate.raw_record_id) is not None:
                raise RecordAlreadyCanonicalizedError(str(candidate.raw_record_id))

            resync_institution_id = await _apply_decision(session, candidate, req.decision)

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

        # Scheduled only after the transaction above has committed -- a
        # reviewer's merge/branch decision can update a branch/institution
        # that was already synced to core-newax via
        # api/routes/manual_leads.py; without this, that mirror silently
        # goes stale after the decision. Uses a fresh session/query (see
        # resync_institution) rather than the objects touched above, since
        # this runs after `session`'s own transaction has ended.
        if (
            resync_institution_id is not None
            and background_tasks is not None
            and lead_sync_emitter is not None
        ):
            background_tasks.add_task(resync_institution, lead_sync_emitter, resync_institution_id)

        return detail


def _record_evidence(record: RawSourceRecord | None) -> dict:
    fields = display_fields(record) if record else {}
    return {
        "name": fields.get("name"),
        "address": fields.get("address"),
        "phone": record.normalized_phone if record else None,
        "website": fields.get("website"),
    }


async def _target_evidence(session: AsyncSession, candidate: ResolutionCandidate) -> dict:
    """
    Evidence for the "Record B" / target side of a review, mirroring
    incoming_data's shape -- previously only the incoming record's evidence
    was returned, forcing the frontend to hardcode the target side as
    "Unknown" (ResolutionDetail.tsx), which meant a reviewer had nothing to
    compare the incoming record against before deciding.
    """
    if candidate.target_raw_record_id:
        target_record = await session.get(RawSourceRecord, candidate.target_raw_record_id)
        if target_record:
            return _record_evidence(target_record)
    elif candidate.target_canonical_id:
        institution = await session.get(CanonicalInstitution, candidate.target_canonical_id)
        if institution:
            # A candidate can target a canonical institution directly (no
            # specific prior raw record -- see _apply_decision's
            # target_canonical_id branch), but that institution can still
            # have real, populated Branch/ContactPoint rows -- address/phone
            # were always reported null regardless, so a reviewer saw
            # "Unknown" for two primary comparison signals raw-record
            # targets already expose, even when the data existed.
            branch = (
                await session.execute(
                    select(Branch).where(Branch.institution_id == institution.id).limit(1)
                )
            ).scalar_one_or_none()
            phone_contact = (
                await session.execute(
                    select(ContactPoint)
                    .where(
                        ContactPoint.institution_id == institution.id,
                        ContactPoint.contact_type == "phone",
                    )
                    .limit(1)
                )
            ).scalar_one_or_none()
            return {
                "name": institution.canonical_name,
                "address": branch.address if branch else None,
                "phone": phone_contact.contact_value if phone_contact else None,
                "website": institution.website,
            }
    return {"name": "Unknown", "address": None, "phone": None, "website": None}


async def _assemble_detail(session: AsyncSession, candidate: ResolutionCandidate) -> dict:
    record = await session.get(RawSourceRecord, candidate.raw_record_id)
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
        "incoming_data": _record_evidence(record),
        "target_data": await _target_evidence(session, candidate),
    }


async def _apply_decision(
    session: AsyncSession, candidate: ResolutionCandidate, decision: str
) -> UUID | None:
    """
    Mutates the actual entity data per the human's decision -- until this
    was added, make_decision only wrote an AuditLog row and never touched
    any CanonicalInstitution/Branch/ContactPoint.

    Returns the id of an institution that needs a lead_sync re-emit --
    i.e. one this decision attached new evidence to (via
    attach_record_to_institution) that was already offered to the webhook
    before (CanonicalInstitution.lead_synced_at is set) -- or None when no
    re-sync is needed (a "separate" decision touches no existing
    institution; a "merge"/"branch" against a brand-new record creates a
    fresh institution via merge_records that has never been synced).
    """
    record = await session.get(RawSourceRecord, candidate.raw_record_id)
    matched_record = None
    if candidate.target_raw_record_id:
        matched_record = await session.get(RawSourceRecord, candidate.target_raw_record_id)

    if decision == "separate":
        # Confidently distinct: the incoming record gets its own institution.
        # The matched record (if any) is left untouched.
        institution = await merge_records(session, [record])
        # Correction: `record`'s RawPageSnapshot rows (if it's a WEBSITE
        # record) were persisted back when it was first crawled, with
        # institution_id still null since resolution hadn't run yet --
        # nothing else ever revisits that link once this candidate leaves
        # the pending-review queue, so it must happen here. See
        # link_page_snapshots_to_institution's own docstring.
        await link_page_snapshots_to_institution(session, record.id, institution.id)
        return None

    if matched_record is None:
        if candidate.target_canonical_id:
            # The candidate's target is a canonical institution directly
            # (not a specific prior raw record) -- the model/schema support
            # this shape even though blocking.py never actually generates
            # it today. There's no specific prior raw record here to match
            # branches against, so always attach as a new branch (the
            # "branch" semantics) rather than guessing which existing
            # branch a "merge" would enrich in place.
            institution = await session.get(CanonicalInstitution, candidate.target_canonical_id)
            if institution is None:
                raise ResourceNotFoundError(str(candidate.target_canonical_id))
            await attach_record_to_institution(session, record, institution, target_branch=None)
            await link_page_snapshots_to_institution(session, record.id, institution.id)
            return institution.id if institution.lead_synced_at is not None else None

        # "merge"/"branch" both require something to attach to; without a
        # raw-record or canonical match there is nothing to merge or branch onto.
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
        # Only `record`'s snapshots need linking here -- matched_record
        # already belongs to `institution` (that's what existing_canonical_id
        # means), so its own snapshots were already linked when IT was
        # resolved.
        await link_page_snapshots_to_institution(session, record.id, institution.id)
        return institution.id if institution.lead_synced_at is not None else None

    # matched_record (B) is itself still unresolved -- unlike the
    # existing_canonical_id branch above (where B is already canonicalized,
    # so any B-target candidate is already excluded from list_pending
    # independent of this decision), merging A into B here is what WOULD
    # canonicalize B for the first time. If B has its own separate pending
    # candidate (e.g. B was also blocked against C and that pairing scored
    # PENDING), canonicalizing B now makes list_pending's
    # already-canonicalized exclusion silently drop that B/C candidate from
    # the queue -- hiding a genuine, never-actually-resolved ambiguity
    # (is B the same institution as C?) behind a decision that only ever
    # asked "is A the same institution as B?". Block it and make the
    # reviewer resolve B's own conflict first.
    if await _has_other_pending_candidate(session, matched_record.id, exclude_id=candidate.id):
        raise TargetHasPendingConflictError(str(matched_record.id))

    institution = await merge_records(
        session, [record, matched_record], same_location=same_location
    )
    # Correction: both raw records are newly canonicalized by this merge --
    # neither had an institution before, so both may have WEBSITE
    # RawPageSnapshot rows still waiting to be linked.
    await link_page_snapshots_to_institution(session, record.id, institution.id)
    await link_page_snapshots_to_institution(session, matched_record.id, institution.id)
    return None
