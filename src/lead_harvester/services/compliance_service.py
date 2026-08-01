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
from lead_harvester.config import settings as app_settings
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
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
from lead_harvester.models.outbox import EventOutbox, OutboxStatus
from lead_harvester.models.outreach import AccountBrief, OutreachDraft, OutreachOutcome
from lead_harvester.models.person import PersonCandidate
from lead_harvester.models.profile import LeadProfile, LeadScoreSnapshot
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.qualification import QualificationAssessment
from lead_harvester.models.research import ResearchFinding, ResearchJob
from lead_harvester.models.resolution import MatchAssessment, ResolutionCandidate
from lead_harvester.models.signal import Signal
from lead_harvester.models.source import RawPageSnapshot, RawSourceRecord, SourceRun, SourceType
from lead_harvester.models.verification import DataQualityFlag
from lead_harvester.resolution.normalize import normalize_phone
from lead_harvester.services.lead_profile_service import refresh_lead_profile
from lead_harvester.services.outbox_service import enqueue_and_attempt_delivery


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


def _resolution_candidate_condition(
    institution_id: uuid.UUID, exclusive_raw_record_ids: list[uuid.UUID]
):
    """
    A ResolutionCandidate is reachable from this institution's erasure two
    ways: directly (target_canonical_id -- the automated-resolution-
    against-an-existing-institution shape) or indirectly, because
    blocking.py's normal candidate-generation shape (raw_record_id/
    target_raw_record_id) points at a RawSourceRecord this institution's
    own erasure is about to purge (see
    _partition_institution_raw_source_records) -- DB-level CASCADE on
    those two FKs (migration a5c7e9f1b3d5) removes the second kind just as
    surely as the first, so both must count as "deleted" here, not just
    the target_canonical_id shape.
    """
    conditions = [ResolutionCandidate.target_canonical_id == institution_id]
    if exclusive_raw_record_ids:
        conditions.append(ResolutionCandidate.raw_record_id.in_(exclusive_raw_record_ids))
        conditions.append(ResolutionCandidate.target_raw_record_id.in_(exclusive_raw_record_ids))
    return or_(*conditions)


# Correction (docs/ROADMAP.md module 11): every table directly owned by a
# CanonicalInstitution -- a real FK to canonical_institutions.id. The
# actual removal happens at the database level (ON DELETE CASCADE on each
# of these FKs, added by migration a5c7e9f1b3d5) when
# _erase_institution issues a single DELETE against the institution row;
# this list exists purely so the deletion manifest can report an exact
# per-table count of what that one statement removed.
async def _count_institution_dependents(
    session: AsyncSession, institution_id: uuid.UUID, exclusive_raw_record_ids: list[uuid.UUID]
) -> dict[str, int]:
    resolution_candidate_condition = _resolution_candidate_condition(
        institution_id, exclusive_raw_record_ids
    )
    counts = {
        "branches": await _count_where(session, Branch, Branch.institution_id, institution_id),
        "contact_points": await _count_where(
            session, ContactPoint, ContactPoint.institution_id, institution_id
        ),
        "account_briefs": await _count_where(
            session, AccountBrief, AccountBrief.institution_id, institution_id
        ),
        "resolution_candidates": int(
            await session.scalar(
                select(func.count())
                .select_from(ResolutionCandidate)
                .where(resolution_candidate_condition)
            )
            or 0
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
            .where(resolution_candidate_condition)
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


async def _enqueue_deletion_event(session: AsyncSession, institution_id: uuid.UUID) -> bool:
    """
    Correction (docs/ROADMAP.md module 11): an institution already
    mirrored to core-newax (CanonicalInstitution.lead_synced_at is set)
    has had its contact values/names copied into an external system this
    local erasure alone can't reach -- deleting our own EventOutbox
    ledger (which _erase_institution's cascade does, along with
    everything else) tells core-newax nothing, so its copy would
    silently survive a "completed" deletion request forever. Enqueues a
    durable "institution.deleted" event through the exact same
    retry/backoff machinery (services/outbox_service.py::
    process_pending_deliveries) every other outbound event already uses.

    institution_id is deliberately NOT set on the row itself (unlike
    every other EventOutbox row) -- see models/outbox.py's own comment:
    the institution this row is about is being deleted in the same
    transaction, and this FK's CASCADE would otherwise delete the
    tombstone right along with it before it can ever be delivered.

    Correction: persisted unconditionally once the caller confirms this
    institution was previously synced (lead_synced_at set) -- deliberately
    NOT gated on whether lead_sync is CURRENTLY enabled/configured. Gating
    on live config would silently drop the tombstone forever the moment
    sync happens to be disabled when an already-synced institution gets
    erased: the institution and its own EventOutbox history are both about
    to be deleted in this same transaction, so there is no later chance to
    reconstruct "this institution needs a deletion event." Delivery itself
    is deferred to the same outbox retry/dead-letter machinery
    (process_pending_deliveries) every other row already goes through --
    if sync is disabled, delivery attempts simply keep failing/backing off
    like any other unreachable-receiver row, eventually dead-lettering for
    a human to requeue once configuration is restored, rather than the
    event being silently lost.

    Always returns True now that creation no longer depends on live
    config -- kept as a bool (not void) so the manifest field and any
    future gating condition have somewhere to report False again.
    """
    emitter = LeadSyncEmitter(app_settings)
    payload = emitter._build_deletion_payload(institution_id)
    session.add(
        EventOutbox(
            id=uuid.UUID(payload["eventId"]),
            institution_id=None,
            event_type=payload["eventType"],
            payload=payload,
            status=OutboxStatus.PENDING,
            next_attempt_at=datetime.now(UTC),
        )
    )
    await session.flush()
    return True


async def _redact_manual_source_run_notes(
    session: AsyncSession, exclusive_raw_record_ids: list[uuid.UUID]
) -> int:
    """
    api/routes/manual_leads.py copies the submitter's free-text
    lead_source_note/notes into the PARENT SourceRun.run_metadata, not
    into the RawSourceRecord itself -- deleting the exclusive raw records
    below never touches that parent row (a SourceRun is the run those
    records belong to, not something CASCADE-owned by them), so that
    subject-specific text would otherwise survive this erasure forever.

    Only redacts a SourceRun that exclusively belongs to this erasure's
    own manual submission -- i.e. no OTHER RawSourceRecord still
    references it. A WEBSITE/GOOGLE_PLACES/etc SourceRun covers a whole
    crawl BATCH routinely shared by many unrelated institutions; blanking
    its run_metadata would destroy audit context this erasure was never
    asked to touch. A MANUAL SourceRun is created fresh per submission
    (api/routes/manual_leads.py's own request_deletion call site), so this
    exclusivity check is expected to always pass for it in practice --
    still checked explicitly rather than assumed.

    Returns the number of SourceRun rows redacted, purely for the manifest.
    """
    if not exclusive_raw_record_ids:
        return 0
    manual_records = list(
        (
            await session.scalars(
                select(RawSourceRecord).where(
                    RawSourceRecord.id.in_(exclusive_raw_record_ids),
                    RawSourceRecord.source_type == SourceType.MANUAL,
                )
            )
        ).all()
    )
    redacted_count = 0
    for record in manual_records:
        other_records_on_run = await _count_where(
            session,
            RawSourceRecord,
            RawSourceRecord.source_run_id,
            record.source_run_id,
        )
        if other_records_on_run > 1:
            continue
        run = await session.get(SourceRun, record.source_run_id)
        if run is None:
            continue
        run.run_metadata = {
            **run.run_metadata,
            "lead_source_note": "[REDACTED]",
            "notes": "[REDACTED]",
        }
        redacted_count += 1
    return redacted_count


async def _erase_institution(
    session: AsyncSession, institution: CanonicalInstitution
) -> dict[str, Any]:
    """
    The explicit deletion graph for an institution-level erasure request,
    run as part of the caller's single transaction (see fulfill_deletion,
    which locks `institution` with SELECT ... FOR UPDATE before calling
    this -- required so a concurrent writer can't add new evidence
    between the partition below and the delete; canonical/merger.py::
    attach_record_to_institution already takes the same lock before
    mutating an institution, so it blocks until this transaction ends):

    1. Partition this institution's raw evidence (RawSourceRecord, via
       FieldProvenance) into exclusive (erase) vs shared (retain, report).
    2. Count every dependent row (the manifest's "deleted_counts"),
       including what the exclusive raw-record purge itself cascades
       away, before touching anything.
    3. Enqueue a durable deletion event if this institution was ever
       mirrored downstream (see _enqueue_deletion_event).
    4. Delete the exclusive RawSourceRecord rows -- DB-level CASCADE (see
       migration a5c7e9f1b3d5) takes their own FieldProvenance/
       ResolutionCandidate/RawPageSnapshot rows with them.
    5. Delete the institution row itself -- DB-level CASCADE removes every
       remaining directly- and indirectly-owned table in the same
       statement (Branch, ContactPoint, AccountBrief+drafts+outcomes,
       ResolutionCandidate+assessments, FieldProvenance,
       QualificationAssessment, ResearchJob+findings, PersonCandidate,
       Signal, DataQualityFlag, LeadReservation, LeadProfile,
       LeadScoreSnapshot, EventOutbox, RawPageSnapshot).
    6. Re-run the same counts (the verification result) to confirm nothing
       was left behind.

    AuditLog is deliberately untouched throughout -- see models/audit.py:
    entity_id is not a real FK specifically so audit history survives a
    subject's erasure, the "retained for lawful audit" branch of this
    correction. SuppressionEntry is unrelated to institution lifecycle
    (keyed by normalized_contact_value, not institution_id) and is also
    untouched, so a suppressed contact stays suppressed even after the
    institution it was attached to is gone.
    """
    institution_id = institution.id
    (
        exclusive_raw_record_ids,
        shared_raw_record_ids,
    ) = await _partition_institution_raw_source_records(session, institution_id)
    deleted_counts = await _count_institution_dependents(
        session, institution_id, exclusive_raw_record_ids
    )
    deleted_counts["raw_source_records"] = len(exclusive_raw_record_ids)

    deletion_event_enqueued = False
    if institution.lead_synced_at is not None:
        deletion_event_enqueued = await _enqueue_deletion_event(session, institution_id)

    redacted_source_runs = await _redact_manual_source_run_notes(session, exclusive_raw_record_ids)

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
    residual_counts = await _count_institution_dependents(
        session, institution_id, exclusive_raw_record_ids
    )
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
        "downstream_deletion_event_enqueued": deletion_event_enqueued,
        "redacted_source_runs": redacted_source_runs,
        "verified": verified,
        "residual_counts": {k: v for k, v in residual_counts.items() if v},
    }


async def _resync_after_contact_erasure(session: AsyncSession, institution_id: uuid.UUID) -> bool:
    """
    Correction (docs/ROADMAP.md module 11): if this contact's institution
    was already mirrored to core-newax, LeadSyncEmitter._build_payload's
    upsert embedded this exact contact's name/value in that copy --
    deleting only the local ContactPoint row leaves it there forever
    unless something re-syncs. Re-enqueues a fresh "institution.upserted"
    event through the same durable outbox path (services/outbox_service.py
    ::enqueue_and_attempt_delivery) every ordinary institution update
    already uses, built from this institution's branches/contacts as they
    stand NOW -- read in the SAME transaction, after the delete, so the
    erased contact is correctly absent from it. Deliberately not
    resync_institution (integrations/lead_sync_resync.py): that helper
    opens its own fresh session/transaction, which would read this
    institution's contacts from BEFORE this call's still-uncommitted
    delete, re-syncing the very data being erased.

    Returns whether an event was actually enqueued, purely for the
    manifest.
    """
    emitter = LeadSyncEmitter(app_settings)
    if not emitter.settings.lead_sync_enabled or not emitter.settings.lead_sync_webhook_url:
        return False
    institution = await session.get(CanonicalInstitution, institution_id)
    if institution is None or institution.lead_synced_at is None:
        return False
    branches = list(
        (await session.scalars(select(Branch).where(Branch.institution_id == institution_id))).all()
    )
    contact_points = list(
        (
            await session.scalars(
                select(ContactPoint).where(ContactPoint.institution_id == institution_id)
            )
        ).all()
    )
    row = await enqueue_and_attempt_delivery(
        session, emitter, institution, branches, contact_points
    )
    return row is not None


def _redact_value_in_payload(payload: Any, value: str) -> tuple[Any, bool]:
    """
    Recursively walks a JSON-shaped structure (RawSourceRecord.raw_payload)
    and replaces every string exactly equal to `value` with a redaction
    marker, leaving every other key/value untouched -- a raw_payload blob
    routinely carries several unrelated fields (name, address, other
    contacts) for the SAME record, so blanking the whole record or the
    whole payload would destroy evidence this erasure was never asked to
    remove. Returns (possibly-new structure, whether anything changed) so
    the caller only reassigns/flushes when there was actually a match.
    """
    if isinstance(payload, dict):
        changed = False
        new_dict = {}
        for key, val in payload.items():
            new_val, sub_changed = _redact_value_in_payload(val, value)
            new_dict[key] = new_val
            changed = changed or sub_changed
        return new_dict, changed
    if isinstance(payload, list):
        changed = False
        new_list = []
        for item in payload:
            new_item, sub_changed = _redact_value_in_payload(item, value)
            new_list.append(new_item)
            changed = changed or sub_changed
        return new_list, changed
    if isinstance(payload, str) and payload == value:
        return "[REDACTED]", True
    return payload, False


async def _erase_contact_source_evidence(
    session: AsyncSession, institution_id: uuid.UUID, contact_type: str, contact_value: str
) -> int:
    """
    Deleting the ContactPoint row alone leaves this exact value sitting in
    two other places written by canonical/merger.py::_add_contact_if_present
    at ingestion time: a FieldProvenance row (field_name=f"contact_{type}",
    asserted_value=contact_value) and, inside the RawSourceRecord it points
    at, raw_payload (and normalized_phone, for a phone contact) -- both
    still carry the erased value even after the ContactPoint fulfilling a
    deletion request reports verified: true.

    Deletes the exact matching FieldProvenance assertions and redacts (not
    deletes) the same value out of each contributing RawSourceRecord --
    deleting the whole RawSourceRecord would also destroy any unrelated
    evidence (address, other contacts) it still carries for this
    institution or, if it's shared, for a different one entirely.

    Returns the number of RawSourceRecord rows redacted, purely so the
    manifest can report it.
    """
    # asserted_value is JSONB, not a plain string column -- Postgres has no
    # `jsonb = varchar` operator, so the value match is done in Python
    # after narrowing by the two indexed/typed columns (canonical_id,
    # field_name) rather than pushing the equality into SQL.
    candidate_rows = list(
        (
            await session.scalars(
                select(FieldProvenance).where(
                    FieldProvenance.canonical_id == institution_id,
                    FieldProvenance.field_name == f"contact_{contact_type}",
                )
            )
        ).all()
    )
    provenance_rows = [row for row in candidate_rows if row.asserted_value == contact_value]
    raw_record_ids = {row.raw_record_id for row in provenance_rows}
    for row in provenance_rows:
        await session.delete(row)

    redacted_count = 0
    for raw_record_id in raw_record_ids:
        record = await session.get(RawSourceRecord, raw_record_id)
        if record is None:
            continue
        new_payload, changed = _redact_value_in_payload(record.raw_payload, contact_value)
        if contact_type == "phone" and record.normalized_phone == contact_value:
            record.normalized_phone = None
            changed = True
        if changed:
            record.raw_payload = new_payload
            redacted_count += 1

    if provenance_rows or redacted_count:
        await session.flush()
    return redacted_count


async def _erase_contact_point(session: AsyncSession, contact: ContactPoint) -> dict[str, Any]:
    """
    No table holds a real FK to contact_points.id, so a single-row delete
    is already transactionally complete -- this still returns the same
    manifest/verification shape as an institution erasure so
    DeletionRequest.manifest has one consistent contract regardless of
    subject_type.

    Takes the already-locked ContactPoint (see fulfill_deletion's
    SELECT ... FOR UPDATE) rather than re-fetching by id, so there is no
    window between "confirm it exists" and "delete it" for a second
    overlapping request on the same contact to race through.
    """
    contact_point_id = contact.id
    institution_id = contact.institution_id
    contact_type = contact.contact_type
    contact_value = contact.contact_value

    await session.execute(
        delete(ContactPoint)
        .where(ContactPoint.id == contact_point_id)
        .execution_options(synchronize_session=False)
    )
    await session.flush()
    still_present = await _count_where(session, ContactPoint, ContactPoint.id, contact_point_id) > 0

    downstream_resync_enqueued = False
    redacted_source_records = 0
    if not still_present:
        # Compliance gate (docs/ROADMAP.md module 11): the exact same
        # suppression mechanism outreach/automator.py already checks via
        # is_eligible_to_contact before ever sending -- a blanket
        # (channel=None) LEGAL_REQUEST entry blocks every channel, so any
        # OutreachDraft still holding this value in target_contact_value
        # (pending, approved, or otherwise unsent) can no longer actually
        # be delivered, without needing a new draft-cancellation state
        # machine of its own.
        await add_suppression(
            session,
            contact_value,
            SuppressionReason.LEGAL_REQUEST,
            note="deletion_request_fulfilled",
            suppressed_by="system",
        )
        redacted_source_records = await _erase_contact_source_evidence(
            session, institution_id, contact_type, contact_value
        )
        await refresh_lead_profile(session, institution_id)
        downstream_resync_enqueued = await _resync_after_contact_erasure(session, institution_id)

    return {
        "subject_type": DeletionSubjectType.CONTACT_POINT.value,
        "subject_id": str(contact_point_id),
        "deleted_counts": {"contact_points": 1},
        "retained": {"audit_logs": "retained_for_lawful_audit"},
        "redacted_source_records": redacted_source_records,
        "downstream_resync_enqueued": downstream_resync_enqueued,
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

    Locks the DeletionRequest row itself (SELECT ... FOR UPDATE), not a
    plain session.get -- two overlapping calls for the SAME request could
    otherwise both read it as PENDING and both load the subject before
    either commits; the second erasure would then delete zero rows (the
    first already removed everything) without error, yet both would still
    write status=COMPLETED and their own "successful" manifest/AuditLog,
    with the second manifest claiming counts it never actually deleted.
    The lock makes the second call block until the first's transaction
    ends, then correctly re-read status as COMPLETED and raise below.
    """
    request = await session.scalar(
        select(DeletionRequest).where(DeletionRequest.id == deletion_request_id).with_for_update()
    )
    if request is None:
        raise ResourceNotFoundError(str(deletion_request_id))
    if request.status != DeletionRequestStatus.PENDING:
        raise ValueError(
            f"Deletion request {deletion_request_id} is {request.status.value}, not pending."
        )

    if request.subject_type == DeletionSubjectType.INSTITUTION:
        # Locked (SELECT ... FOR UPDATE), not a plain session.get -- held
        # for the rest of this transaction, so a concurrent writer that
        # also locks this same institution row (attach_record_to_
        # institution's own with_for_update, canonical/merger.py) either
        # already committed its new evidence before this lock was
        # acquired (so _erase_institution's partition sees it and erases
        # it too) or blocks until this whole erasure transaction ends, by
        # which point the institution -- and its FK target -- is gone.
        # Without this, new evidence could land between the partition
        # query and the delete below, surviving as an orphan while the
        # manifest still reports verified: true.
        subject = await session.scalar(
            select(CanonicalInstitution)
            .where(CanonicalInstitution.id == request.subject_id)
            .with_for_update()
        )
        if subject is None:
            raise ResourceNotFoundError(str(request.subject_id))
        manifest = await _erase_institution(session, subject)
    else:
        # Locked (SELECT ... FOR UPDATE), same reasoning as the institution
        # branch above: without it, two overlapping deletion requests for
        # the SAME contact could both load it here before either deletes,
        # so the second's DELETE affects zero rows without error yet still
        # reports deleted_counts: {"contact_points": 1} and completes its
        # own "successful" audit entry. The lock makes the second call
        # block until the first's transaction ends, then correctly find no
        # row and raise ResourceNotFoundError below instead.
        subject = await session.scalar(
            select(ContactPoint).where(ContactPoint.id == request.subject_id).with_for_update()
        )
        if subject is None:
            raise ResourceNotFoundError(str(request.subject_id))
        manifest = await _erase_contact_point(session, subject)
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

    Correction: also excludes a RawSourceRecord still referenced by a
    ResolutionCandidate awaiting human review (review_outcome is null),
    on either raw_record_id or target_raw_record_id. Now that
    resolution_candidates' FKs to raw_source_records are ON DELETE
    CASCADE (migration a5c7e9f1b3d5, added for
    services/compliance_service.py::_erase_institution's own sake), this
    purge would otherwise be able to silently cascade-delete a live
    ResolutionCandidate + MatchAssessment still sitting in the
    resolution-reviews queue -- previously that would have raised a loud
    FK violation instead of quietly destroying a pending review. Mirrors
    pipeline.py::_retry_stranded_records' own "stranded" query, which has
    the identical pending-review exclusion for raw_record_id alone (it
    never needed target_raw_record_id, a different concern).
    """
    cutoff = datetime.now(UTC) - timedelta(days=retention_days)
    referenced = select(FieldProvenance.raw_record_id).distinct()
    pending_review = (
        select(ResolutionCandidate.raw_record_id)
        .where(ResolutionCandidate.review_outcome.is_(None))
        .union(
            select(ResolutionCandidate.target_raw_record_id).where(
                ResolutionCandidate.review_outcome.is_(None),
                ResolutionCandidate.target_raw_record_id.is_not(None),
            )
        )
    )
    result = await session.execute(
        delete(RawSourceRecord)
        .where(RawSourceRecord.extracted_at < cutoff)
        .where(RawSourceRecord.id.not_in(referenced))
        .where(RawSourceRecord.id.not_in(pending_review))
    )
    await session.flush()
    return result.rowcount or 0
