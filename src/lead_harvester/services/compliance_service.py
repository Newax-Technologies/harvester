"""
Suppression, channel eligibility, deletion requests, and retention -- see
docs/ROADMAP.md module 11.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import delete, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.compliance.channel_eligibility import EligibilityResult, is_channel_eligible
from lead_harvester.models.allocation import LeadReservation
from lead_harvester.models.audit import AuditLog
from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint
from lead_harvester.models.compliance import (
    DeletionRequest,
    DeletionRequestStatus,
    DeletionSubjectType,
    SuppressionEntry,
    SuppressionReason,
)
from lead_harvester.models.outbox import EventOutbox
from lead_harvester.models.outreach import AccountBrief, OutreachDraft, OutreachOutcome
from lead_harvester.models.person import PersonCandidate
from lead_harvester.models.profile import LeadProfile, LeadScoreSnapshot
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.qualification import QualificationAssessment
from lead_harvester.models.research import ResearchFinding, ResearchJob
from lead_harvester.models.resolution import MatchAssessment, ResolutionCandidate
from lead_harvester.models.signal import Signal
from lead_harvester.models.source import RawPageSnapshot, RawSourceRecord
from lead_harvester.models.verification import DataQualityFlag
from lead_harvester.resolution.normalize import normalize_phone


def normalize_contact_value(value: str, *, default_region: str | None = None) -> str:
    """
    Same normalization every other exact-match contact comparison in this
    codebase relies on (resolution/normalize.py::normalize_phone for
    phone-shaped values) -- not a separate scheme, so a suppression
    entered as "+92 300 1234567" still matches a ContactPoint stored as
    "+923001234567".

    A LinkedIn profile URL (outreach/automator.py's OutreachDraft.
    target_contact_value for LinkedIn drafts, distinguished there by
    startswith("http")) is neither email- nor phone-shaped -- normalize_
    phone would strip it down to just its digits (or an EMPTY string for
    a URL with none, e.g. "https://linkedin.com/in/janedoe"), which would
    silently collide every digit-less LinkedIn URL onto the same "" key
    and suppress all of them together. Treated as an opaque
    already-comparable identifier instead: lowercased with a trailing
    slash stripped, matching how it's stored/compared everywhere else.
    """
    if "@" in value:
        return value.strip().lower()
    if value.strip().lower().startswith("http"):
        return value.strip().lower().rstrip("/")
    return normalize_phone(value, default_region=default_region)


async def add_suppression(
    session: AsyncSession,
    contact_value: str,
    reason: SuppressionReason,
    *,
    channel: str | None = None,
    note: str = "",
    suppressed_by: str = "system",
    default_region: str | None = None,
) -> SuppressionEntry:
    entry = SuppressionEntry(
        normalized_contact_value=normalize_contact_value(
            contact_value, default_region=default_region
        ),
        channel=channel,
        reason=reason,
        note=note,
        suppressed_by=suppressed_by,
    )
    session.add(entry)
    await session.flush()
    return entry


async def remove_suppression(session: AsyncSession, suppression_id: uuid.UUID) -> None:
    entry = await session.get(SuppressionEntry, suppression_id)
    if entry is None:
        raise ResourceNotFoundError(str(suppression_id))
    await session.delete(entry)
    await session.flush()


async def find_applicable_suppression(
    session: AsyncSession,
    contact_value: str,
    *,
    channel: str | None = None,
    default_region: str | None = None,
) -> SuppressionEntry | None:
    normalized = normalize_contact_value(contact_value, default_region=default_region)
    stmt = (
        select(SuppressionEntry)
        .where(SuppressionEntry.normalized_contact_value == normalized)
        .where(or_(SuppressionEntry.channel.is_(None), SuppressionEntry.channel == channel))
        # A blanket (every-channel) suppression takes priority when both
        # a blanket and a channel-specific entry exist for the same value.
        .order_by(SuppressionEntry.channel.is_(None).desc())
        .limit(1)
    )
    return await session.scalar(stmt)


async def is_eligible_to_contact(
    session: AsyncSession,
    contact_value: str,
    channel: str,
    *,
    default_region: str | None = None,
) -> EligibilityResult:
    suppression = await find_applicable_suppression(
        session, contact_value, channel=channel, default_region=default_region
    )
    return is_channel_eligible(channel, suppression)


async def list_suppressions(session: AsyncSession, *, limit: int = 100) -> list[SuppressionEntry]:
    stmt = select(SuppressionEntry).order_by(SuppressionEntry.suppressed_at.desc()).limit(limit)
    return list(await session.scalars(stmt))


async def request_deletion(
    session: AsyncSession,
    subject_type: DeletionSubjectType,
    subject_id: uuid.UUID,
    note: str = "",
) -> DeletionRequest:
    request = DeletionRequest(subject_type=subject_type, subject_id=subject_id, requestor_note=note)
    session.add(request)
    await session.flush()
    return request


async def _count_where(session: AsyncSession, model: Any, column: Any, value: Any) -> int:
    stmt = select(func.count()).select_from(model).where(column == value)
    return int(await session.scalar(stmt) or 0)


# Correction (docs/ROADMAP.md module 11): every table directly owned by a
# CanonicalInstitution -- a real FK to canonical_institutions.id. The
# actual removal happens at the database level (ON DELETE CASCADE on each
# of these FKs, added by migration a5c7e9f1b3d5) when
# _erase_institution issues a single DELETE against the institution row;
# this list exists purely so the deletion manifest can report an exact
# per-table count of what that one statement removed.
async def _count_institution_dependents(
    session: AsyncSession, institution_id: uuid.UUID
) -> dict[str, int]:
    counts = {
        "branches": await _count_where(session, Branch, Branch.institution_id, institution_id),
        "contact_points": await _count_where(
            session, ContactPoint, ContactPoint.institution_id, institution_id
        ),
        "account_briefs": await _count_where(
            session, AccountBrief, AccountBrief.institution_id, institution_id
        ),
        "resolution_candidates": await _count_where(
            session, ResolutionCandidate, ResolutionCandidate.target_canonical_id, institution_id
        ),
        "field_provenance": await _count_where(
            session, FieldProvenance, FieldProvenance.canonical_id, institution_id
        ),
        "qualification_assessments": await _count_where(
            session, QualificationAssessment, QualificationAssessment.institution_id, institution_id
        ),
        "research_jobs": await _count_where(
            session, ResearchJob, ResearchJob.institution_id, institution_id
        ),
        "research_findings": await _count_where(
            session, ResearchFinding, ResearchFinding.institution_id, institution_id
        ),
        "person_candidates": await _count_where(
            session, PersonCandidate, PersonCandidate.institution_id, institution_id
        ),
        "signals": await _count_where(session, Signal, Signal.institution_id, institution_id),
        "data_quality_flags": await _count_where(
            session, DataQualityFlag, DataQualityFlag.institution_id, institution_id
        ),
        "lead_reservations": await _count_where(
            session, LeadReservation, LeadReservation.institution_id, institution_id
        ),
        "lead_profiles": await _count_where(
            session, LeadProfile, LeadProfile.institution_id, institution_id
        ),
        "lead_score_history": await _count_where(
            session, LeadScoreSnapshot, LeadScoreSnapshot.institution_id, institution_id
        ),
        "event_outbox": await _count_where(
            session, EventOutbox, EventOutbox.institution_id, institution_id
        ),
        "raw_page_snapshots": await _count_where(
            session, RawPageSnapshot, RawPageSnapshot.institution_id, institution_id
        ),
    }
    # Second-hop children -- cascade automatically alongside their parent
    # above (AccountBrief/ResolutionCandidate), counted separately so the
    # manifest still accounts for everything actually removed.
    counts["outreach_drafts"] = int(
        await session.scalar(
            select(func.count())
            .select_from(OutreachDraft)
            .join(AccountBrief, OutreachDraft.brief_id == AccountBrief.id)
            .where(AccountBrief.institution_id == institution_id)
        )
        or 0
    )
    counts["outreach_outcomes"] = int(
        await session.scalar(
            select(func.count())
            .select_from(OutreachOutcome)
            .join(OutreachDraft, OutreachOutcome.draft_id == OutreachDraft.id)
            .join(AccountBrief, OutreachDraft.brief_id == AccountBrief.id)
            .where(AccountBrief.institution_id == institution_id)
        )
        or 0
    )
    counts["match_assessments"] = int(
        await session.scalar(
            select(func.count())
            .select_from(MatchAssessment)
            .join(ResolutionCandidate, MatchAssessment.candidate_id == ResolutionCandidate.id)
            .where(ResolutionCandidate.target_canonical_id == institution_id)
        )
        or 0
    )
    return counts


async def _partition_institution_raw_source_records(
    session: AsyncSession, institution_id: uuid.UUID
) -> tuple[list[uuid.UUID], list[uuid.UUID]]:
    """
    RawSourceRecord carries no institution_id -- the pipeline only ever
    links it to a CanonicalInstitution indirectly, through the
    FieldProvenance rows it backs (see models/source.py::RawSourceRecord).
    A record this institution's FieldProvenance points at IS this
    subject's raw scraped evidence (raw_payload's name/phone/email) and
    must be erased with it -- UNLESS that same record is ALSO evidence for
    a DIFFERENT institution (FieldProvenance.raw_record_id shared across
    canonical_ids), in which case deleting it would destroy that other
    institution's evidence trail, so it is retained and reported instead
    of erased. In this pipeline's actual resolution flow one raw record
    normally backs exactly one canonical institution, so the "shared" set
    is expected to be empty in practice; this still checks explicitly
    rather than assuming it.
    """
    candidate_ids = set(
        (
            await session.scalars(
                select(FieldProvenance.raw_record_id)
                .where(FieldProvenance.canonical_id == institution_id)
                .distinct()
            )
        ).all()
    )
    if not candidate_ids:
        return [], []

    shared_ids = set(
        (
            await session.scalars(
                select(FieldProvenance.raw_record_id)
                .where(FieldProvenance.raw_record_id.in_(candidate_ids))
                .where(FieldProvenance.canonical_id != institution_id)
                .distinct()
            )
        ).all()
    )
    exclusive_ids = candidate_ids - shared_ids
    return sorted(exclusive_ids), sorted(shared_ids)


async def _erase_institution(session: AsyncSession, institution_id: uuid.UUID) -> dict[str, Any]:
    """
    The explicit deletion graph for an institution-level erasure request,
    run as part of the caller's single transaction (see fulfill_deletion):

    1. Count every dependent row (the manifest's "deleted_counts") before
       touching anything.
    2. Partition this institution's raw evidence (RawSourceRecord, via
       FieldProvenance) into exclusive (erase) vs shared (retain, report).
    3. Delete the exclusive RawSourceRecord rows -- DB-level CASCADE (see
       migration a5c7e9f1b3d5) takes their own FieldProvenance/
       ResolutionCandidate/RawPageSnapshot rows with them.
    4. Delete the institution row itself -- DB-level CASCADE removes every
       remaining directly- and indirectly-owned table in the same
       statement (Branch, ContactPoint, AccountBrief+drafts+outcomes,
       ResolutionCandidate+assessments, FieldProvenance,
       QualificationAssessment, ResearchJob+findings, PersonCandidate,
       Signal, DataQualityFlag, LeadReservation, LeadProfile,
       LeadScoreSnapshot, EventOutbox, RawPageSnapshot).
    5. Re-run the same counts (the verification result) to confirm nothing
       was left behind.

    AuditLog is deliberately untouched throughout -- see models/audit.py:
    entity_id is not a real FK specifically so audit history survives a
    subject's erasure, the "retained for lawful audit" branch of this
    correction. SuppressionEntry is unrelated to institution lifecycle
    (keyed by normalized_contact_value, not institution_id) and is also
    untouched, so a suppressed contact stays suppressed even after the
    institution it was attached to is gone.
    """
    deleted_counts = await _count_institution_dependents(session, institution_id)
    (
        exclusive_raw_record_ids,
        shared_raw_record_ids,
    ) = await _partition_institution_raw_source_records(session, institution_id)
    deleted_counts["raw_source_records"] = len(exclusive_raw_record_ids)

    if exclusive_raw_record_ids:
        await session.execute(
            delete(RawSourceRecord)
            .where(RawSourceRecord.id.in_(exclusive_raw_record_ids))
            .execution_options(synchronize_session=False)
        )

    await session.execute(
        delete(CanonicalInstitution)
        .where(CanonicalInstitution.id == institution_id)
        .execution_options(synchronize_session=False)
    )
    await session.flush()

    # Deliberately a fresh COUNT query, not session.get() -- the DELETEs
    # above were issued as Core statements (so the DB-level CASCADE fires
    # uniformly for every dependent table in one round trip) and never
    # touched SQLAlchemy's identity map. session.get() checks the identity
    # map BEFORE the database, so it would return this session's own
    # already-loaded (now stale) institution object instead of correctly
    # reporting it gone; a real SELECT always reflects the database.
    residual_counts = await _count_institution_dependents(session, institution_id)
    residual_counts["raw_source_records"] = (
        int(
            await session.scalar(
                select(func.count())
                .select_from(RawSourceRecord)
                .where(RawSourceRecord.id.in_(exclusive_raw_record_ids))
            )
            or 0
        )
        if exclusive_raw_record_ids
        else 0
    )
    institution_still_present = (
        await _count_where(session, CanonicalInstitution, CanonicalInstitution.id, institution_id)
        > 0
    )
    verified = not institution_still_present and all(
        count == 0 for count in residual_counts.values()
    )

    return {
        "subject_type": DeletionSubjectType.INSTITUTION.value,
        "subject_id": str(institution_id),
        "deleted_counts": deleted_counts,
        "retained": {
            "audit_logs": "retained_for_lawful_audit",
            "suppression_entries": "not_linked_to_institution_lifecycle",
            "shared_raw_source_records": [str(record_id) for record_id in shared_raw_record_ids],
        },
        "verified": verified,
        "residual_counts": {k: v for k, v in residual_counts.items() if v},
    }


async def _erase_contact_point(
    session: AsyncSession, contact_point_id: uuid.UUID
) -> dict[str, Any]:
    """
    No table holds a real FK to contact_points.id, so a single-row delete
    is already transactionally complete -- this still returns the same
    manifest/verification shape as an institution erasure so
    DeletionRequest.manifest has one consistent contract regardless of
    subject_type.
    """
    await session.execute(
        delete(ContactPoint)
        .where(ContactPoint.id == contact_point_id)
        .execution_options(synchronize_session=False)
    )
    await session.flush()
    still_present = await _count_where(session, ContactPoint, ContactPoint.id, contact_point_id) > 0

    return {
        "subject_type": DeletionSubjectType.CONTACT_POINT.value,
        "subject_id": str(contact_point_id),
        "deleted_counts": {"contact_points": 1},
        "retained": {"audit_logs": "retained_for_lawful_audit"},
        "verified": not still_present,
        "residual_counts": {} if not still_present else {"contact_points": 1},
    }


async def fulfill_deletion(
    session: AsyncSession, deletion_request_id: uuid.UUID
) -> DeletionRequest:
    """
    Actually deletes the requested subject, following the explicit
    deletion graph in _erase_institution/_erase_contact_point, and writes
    the resulting manifest onto the request. Deliberately a separate call
    from request_deletion -- creating the request never deletes anything
    by itself, so a request sitting PENDING is always safe to review
    before anyone chooses to call this.

    Runs as one transaction: every DELETE issued here (directly, or via
    the ON DELETE CASCADE it triggers) is flushed on this same session,
    which the caller commits or rolls back as a single unit -- a failure
    partway through (there shouldn't be one, given the exclusive/shared
    raw-record partitioning above, but if the database ever rejects a
    statement) leaves nothing partially deleted.
    """
    request = await session.get(DeletionRequest, deletion_request_id)
    if request is None:
        raise ResourceNotFoundError(str(deletion_request_id))
    if request.status != DeletionRequestStatus.PENDING:
        raise ValueError(
            f"Deletion request {deletion_request_id} is {request.status.value}, not pending."
        )

    if request.subject_type == DeletionSubjectType.INSTITUTION:
        subject = await session.get(CanonicalInstitution, request.subject_id)
        if subject is None:
            raise ResourceNotFoundError(str(request.subject_id))
        manifest = await _erase_institution(session, request.subject_id)
    else:
        subject = await session.get(ContactPoint, request.subject_id)
        if subject is None:
            raise ResourceNotFoundError(str(request.subject_id))
        manifest = await _erase_contact_point(session, request.subject_id)
    # The DELETEs above ran as Core statements (so the DB-level CASCADE
    # fires uniformly for every dependent table, see _erase_institution),
    # which never told this session's identity map that `subject` is gone.
    # Without this, a caller's session.get() for the same id right after
    # this call returns -- e.g. to confirm the deletion -- would silently
    # get back the stale, already-loaded (pre-delete) object instead of
    # None.
    session.expunge(subject)

    request.status = DeletionRequestStatus.COMPLETED
    request.fulfilled_at = datetime.now(UTC)
    request.manifest = manifest
    session.add(
        AuditLog(
            action="deletion_request.fulfilled",
            actor="system",
            entity_type="DeletionRequest",
            entity_id=request.id,
            new_state=manifest,
        )
    )
    await session.flush()
    return request


async def reject_deletion(
    session: AsyncSession, deletion_request_id: uuid.UUID, reason: str
) -> DeletionRequest:
    request = await session.get(DeletionRequest, deletion_request_id)
    if request is None:
        raise ResourceNotFoundError(str(deletion_request_id))
    if request.status != DeletionRequestStatus.PENDING:
        raise ValueError(
            f"Deletion request {deletion_request_id} is {request.status.value}, not pending."
        )
    request.status = DeletionRequestStatus.REJECTED
    request.rejection_reason = reason
    request.fulfilled_at = datetime.now(UTC)
    await session.flush()
    return request


async def list_deletion_requests(
    session: AsyncSession, *, status: DeletionRequestStatus | None = None, limit: int = 100
) -> list[DeletionRequest]:
    stmt = select(DeletionRequest).order_by(DeletionRequest.requested_at.desc()).limit(limit)
    if status is not None:
        stmt = stmt.where(DeletionRequest.status == status)
    return list(await session.scalars(stmt))


async def purge_expired_raw_records(session: AsyncSession, *, retention_days: int) -> int:
    """
    Deletes RawSourceRecord rows older than retention_days that have NO
    FieldProvenance referencing them at all -- i.e. rows that never
    contributed to a canonical entity (a duplicate scrape, a failed/
    superseded import row). Scoped this narrowly on purpose: a
    RawSourceRecord that DID produce provenance is load-bearing evidence
    for confidence_score / conflict detection (see verification/checks.py)
    and canonical/merger.py's own field synthesis -- purging it would
    silently corrupt data other live features still depend on. This is
    v1's entire retention enforcement; a broader policy (e.g. expiring
    old-but-referenced records after re-verifying the institution some
    other way) is bigger, separate follow-up work.
    """
    cutoff = datetime.now(UTC) - timedelta(days=retention_days)
    referenced = select(FieldProvenance.raw_record_id).distinct()
    result = await session.execute(
        delete(RawSourceRecord)
        .where(RawSourceRecord.extracted_at < cutoff)
        .where(RawSourceRecord.id.not_in(referenced))
    )
    await session.flush()
    return result.rowcount or 0
