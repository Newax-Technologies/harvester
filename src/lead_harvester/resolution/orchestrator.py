"""
Wires the blocking + scoring resolution pipeline (resolution/blocking.py,
resolution/scoring.py) -- previously dead code, per docs/ROADMAP.md's
tracked follow-up #2 -- into live ingestion. Every newly created
RawSourceRecord is meant to eventually become part of exactly one
CanonicalInstitution; resolve_incoming_record decides which.
"""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import TargetHasPendingConflictError
from lead_harvester.canonical.merger import (
    attach_record_to_institution,
    find_branch_for_raw_record,
    find_canonical_for_raw_record,
    merge_records,
)
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.resolution import MatchAssessment, MatchDecision, ResolutionCandidate
from lead_harvester.models.source import RawSourceRecord
from lead_harvester.resolution.blocking import generate_candidates
from lead_harvester.resolution.scoring import score_candidate

_ScoredCandidate = tuple[ResolutionCandidate, MatchAssessment]


async def resolve_incoming_record(
    session: AsyncSession,
    record: RawSourceRecord,
    *,
    resync_ids: set[uuid.UUID] | None = None,
) -> CanonicalInstitution | None:
    """
    Runs blocking + scoring for one newly ingested record and decides its
    fate:
      - ANY candidate scored PENDING (ambiguous) -> leave unresolved for
        human review via the resolution-reviews queue; returns None. This
        applies even if another candidate ALSO scored a confident MERGE --
        auto-merging into that target while a genuinely competing,
        already-canonicalized PENDING match exists would silently hide the
        ambiguity: both raw records would end up provenanced to the MERGE
        target, and list_pending()'s already-canonicalized exclusion would
        then hide the PENDING sibling from the review queue too, leaving no
        path back to the conflict a human needs to actually resolve.
      - otherwise, a confident MERGE match (see resolution/scoring.py:
        name_similarity >0.8 AND distance<100m, i.e. score_candidate has
        already confirmed this is the same physical location) against an
        already-resolved record -> attach to that existing institution's
        matching branch.
      - otherwise, a confident MERGE match against another brand-new
        (unresolved) record -> merge both into one freshly created
        institution, collapsed to a single shared branch.
      - only LINK_ONLY/REJECT candidates, or no candidates at all -> the
        record is confidently its own distinct entity; give it its own
        institution.

    Only ever generates candidates against other raw records: blocking.py
    has no target_canonical_id case, and score_candidate raises
    NotImplementedError for it. An already-resolved match is discovered
    afterwards via find_canonical_for_raw_record, not via blocking itself.

    Known v1 limitation: this runs per-record within a single ingestion
    run's session/transaction. Two concurrent runs (e.g. an overlapping
    schedule, or google_places + web crawler running in parallel) each only
    see their own uncommitted records, so two records that should resolve to
    the same institution can independently create two separate
    CanonicalInstitutions if their runs overlap. Documented, not solved,
    here -- a full fix (advisory locks, per-record commits, or a unique
    constraint on some normalized key) is separate follow-up work.

    resync_ids: when given, the id of any institution this call attaches
    new evidence to (via attach_record_to_institution) is added to it if
    that institution has previously been offered to the lead_sync webhook
    (CanonicalInstitution.lead_synced_at is set) -- letting the caller
    re-emit a sync event for it once the enclosing transaction commits,
    instead of the core-newax mirror silently going stale after the first
    sync. A freshly merge_records()-created institution is never added
    here: it has no lead_synced_at yet (nothing has offered it to the
    webhook before), so there's nothing to keep in sync.
    """
    candidates = await generate_candidates(session, record)
    for candidate in candidates:
        session.add(candidate)
    await session.flush()

    scored: list[_ScoredCandidate] = []
    for candidate in candidates:
        assessment = await score_candidate(session, candidate)
        scored.append((candidate, assessment))

    if any(assessment.decision == MatchDecision.PENDING for _candidate, assessment in scored):
        return None

    merge_pair = _best_merge_pair(scored)

    if merge_pair is not None:
        candidate, _assessment = merge_pair
        matched_record = await session.get(RawSourceRecord, candidate.target_raw_record_id)
        existing_canonical_id = await find_canonical_for_raw_record(session, matched_record.id)

        if existing_canonical_id is not None:
            institution = await session.get(CanonicalInstitution, existing_canonical_id)
            target_branch = await find_branch_for_raw_record(
                session, institution.id, matched_record
            )
            await attach_record_to_institution(
                session, record, institution, target_branch=target_branch
            )
            if resync_ids is not None and institution.lead_synced_at is not None:
                resync_ids.add(institution.id)
            return institution

        # matched_record (B) is itself still unresolved -- unlike the
        # existing_canonical_id branch above (where B is already
        # canonicalized, so any B-target candidate is already excluded from
        # list_pending independent of this decision), merging A into B here
        # is what WOULD canonicalize B for the first time. If B has its own
        # separate pending candidate (e.g. B was also blocked against C and
        # that pairing scored PENDING), auto-merging A into B now makes
        # list_pending's already-canonicalized exclusion silently drop that
        # B/C candidate from the queue -- hiding a genuine, never-actually-
        # resolved ambiguity (is B the same institution as C?) behind an
        # automated decision that only ever evaluated "is A the same
        # institution as B?". Same guard ResolutionService._apply_decision
        # already applies for the human-decision path -- block it here too
        # rather than merging out from under a conflict nobody has reviewed.
        if await _has_other_pending_candidate(session, matched_record.id, exclude_id=candidate.id):
            raise TargetHasPendingConflictError(str(matched_record.id))

        return await merge_records(session, [record, matched_record], same_location=True)

    return await merge_records(session, [record])


def _best_merge_pair(scored: list[_ScoredCandidate]) -> _ScoredCandidate | None:
    merges = [pair for pair in scored if pair[1].decision == MatchDecision.MERGE]
    if not merges:
        return None
    return max(merges, key=lambda pair: pair[1].total_score)


async def _has_other_pending_candidate(
    session: AsyncSession, raw_record_id: uuid.UUID, *, exclude_id: uuid.UUID
) -> bool:
    """
    True if raw_record_id was ITSELF an incoming record with its own
    unresolved ambiguity -- i.e. it is the raw_record_id (not merely the
    target) of some OTHER still-open ResolutionCandidate (review_outcome is
    null) whose latest assessment is PENDING.

    Deliberately checks only the raw_record_id side, not target_raw_record_id:
    two DIFFERENT candidates both targeting the same popular target record
    (e.g. two reviewers independently deciding A->target and B->target) is
    not this risk -- deciding one legitimately canonicalizes target, and the
    other candidate's own decision (by the reviewer who owns IT) then
    correctly routes to attaching rather than re-merging; nothing gets
    silently swept away, since that second candidate is being explicitly
    decided too. The actual risk is only when raw_record_id was blocked
    against something as an INCOMING record in a still-unresolved pairing
    that nobody is deciding right now.

    exclude_id is always the candidate currently being decided -- without
    excluding it, this would find itself whenever raw_record_id is the
    current candidate's own target (the common case) and block every
    decision unconditionally.

    Shared by both the automated ingestion path (resolve_incoming_record,
    above) and the human-decision path (ResolutionService._apply_decision)
    -- the same silent-conflict-hiding risk applies to both.
    """
    stmt = (
        select(ResolutionCandidate.id)
        .join(MatchAssessment, MatchAssessment.candidate_id == ResolutionCandidate.id)
        .where(
            ResolutionCandidate.id != exclude_id,
            ResolutionCandidate.review_outcome.is_(None),
            MatchAssessment.decision == MatchDecision.PENDING,
            ResolutionCandidate.raw_record_id == raw_record_id,
        )
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is not None
