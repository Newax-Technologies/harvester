import uuid
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import func, select

from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.models.allocation import LeadReservation
from lead_harvester.models.audit import AuditLog
from lead_harvester.models.canonical import Branch, CanonicalInstitution, ContactPoint
from lead_harvester.models.compliance import (
    DeletionRequestStatus,
    DeletionSubjectType,
    SuppressionReason,
)
from lead_harvester.models.outbox import EventOutbox, OutboxStatus
from lead_harvester.models.outreach import AccountBrief, DraftStatus, OutreachDraft, OutreachOutcome
from lead_harvester.models.person import PersonCandidate
from lead_harvester.models.profile import LeadProfile, LeadScoreSnapshot
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.qualification import QualificationAssessment
from lead_harvester.models.research import FindingType, JobStatus, ResearchFinding, ResearchJob
from lead_harvester.models.resolution import (
    MatchAssessment,
    MatchDecision,
    ResolutionCandidate,
    ReviewOutcome,
)
from lead_harvester.models.signal import Signal, SignalType
from lead_harvester.models.source import (
    RawPageSnapshot,
    RawSourceRecord,
    RunStatus,
    SourceRun,
    SourceType,
)
from lead_harvester.models.verification import DataQualityFlag, FlagType
from lead_harvester.services.compliance_service import (
    add_suppression,
    find_applicable_suppression,
    fulfill_deletion,
    is_eligible_to_contact,
    list_deletion_requests,
    list_suppressions,
    normalize_contact_value,
    purge_expired_raw_records,
    reject_deletion,
    remove_suppression,
    request_deletion,
)


def test_normalize_contact_value_handles_email_phone_and_linkedin_url():
    assert normalize_contact_value("Jane@Example.com") == "jane@example.com"
    assert normalize_contact_value("+92 300 1234567") == "+923001234567"
    assert (
        normalize_contact_value("HTTPS://linkedin.com/in/JaneDoe/")
        == "https://linkedin.com/in/janedoe"
    )


@pytest.mark.asyncio
async def test_add_and_find_suppression_blanket_channel(db_session):
    await add_suppression(
        db_session, "jane@example.com", SuppressionReason.OPT_OUT, note="unsubscribed"
    )

    found = await find_applicable_suppression(db_session, "Jane@Example.com", channel="email")
    assert found is not None
    assert found.reason == SuppressionReason.OPT_OUT


@pytest.mark.asyncio
async def test_find_suppression_returns_none_when_not_suppressed(db_session):
    found = await find_applicable_suppression(db_session, "nobody@example.com", channel="email")
    assert found is None


@pytest.mark.asyncio
async def test_is_eligible_to_contact_respects_channel_scoping(db_session):
    await add_suppression(
        db_session, "jane@example.com", SuppressionReason.BOUNCED, channel="email"
    )

    email_result = await is_eligible_to_contact(db_session, "jane@example.com", "email")
    linkedin_result = await is_eligible_to_contact(db_session, "jane@example.com", "linkedin")

    assert email_result.eligible is False
    assert linkedin_result.eligible is True


@pytest.mark.asyncio
async def test_remove_suppression_un_suppresses_the_contact(db_session):
    entry = await add_suppression(db_session, "jane@example.com", SuppressionReason.MANUAL)

    await remove_suppression(db_session, entry.id)

    found = await find_applicable_suppression(db_session, "jane@example.com", channel="email")
    assert found is None


@pytest.mark.asyncio
async def test_remove_suppression_raises_not_found(db_session):
    with pytest.raises(ResourceNotFoundError):
        await remove_suppression(db_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_list_suppressions_returns_most_recent_first(db_session):
    await add_suppression(db_session, "a@example.com", SuppressionReason.MANUAL)
    await add_suppression(db_session, "b@example.com", SuppressionReason.MANUAL)

    entries = await list_suppressions(db_session)

    assert len(entries) == 2
    assert entries[0].suppressed_at >= entries[1].suppressed_at


@pytest.mark.asyncio
async def test_fulfill_deletion_deletes_the_institution(db_session):
    institution = CanonicalInstitution(canonical_name="To Be Deleted School")
    db_session.add(institution)
    await db_session.flush()
    institution_id = institution.id

    request = await request_deletion(
        db_session, DeletionSubjectType.INSTITUTION, institution_id, "GDPR request"
    )

    fulfilled = await fulfill_deletion(db_session, request.id)

    assert fulfilled.status == DeletionRequestStatus.COMPLETED
    assert fulfilled.fulfilled_at is not None
    remaining = await db_session.get(CanonicalInstitution, institution_id)
    assert remaining is None


@pytest.mark.asyncio
async def test_fulfill_deletion_deletes_a_single_contact_point(db_session):
    institution = CanonicalInstitution(canonical_name="Contact Deletion School")
    db_session.add(institution)
    await db_session.flush()
    contact = ContactPoint(
        institution_id=institution.id, contact_type="email", contact_value="a@b.com"
    )
    db_session.add(contact)
    await db_session.flush()
    contact_id = contact.id

    request = await request_deletion(db_session, DeletionSubjectType.CONTACT_POINT, contact_id)
    fulfilled = await fulfill_deletion(db_session, request.id)

    remaining_contact = await db_session.get(ContactPoint, contact_id)
    assert remaining_contact is None
    # The institution itself is untouched -- only the one contact was deleted.
    remaining_institution = await db_session.get(CanonicalInstitution, institution.id)
    assert remaining_institution is not None
    assert fulfilled.manifest == {
        "subject_type": "contact_point",
        "subject_id": str(contact_id),
        "deleted_counts": {"contact_points": 1},
        "retained": {"audit_logs": "retained_for_lawful_audit"},
        "redacted_source_records": 0,
        "downstream_resync_enqueued": False,
        "verified": True,
        "residual_counts": {},
    }
    # A blanket suppression must exist for the erased value -- the exact
    # mechanism outreach/automator.py checks before ever sending, so any
    # OutreachDraft still targeting this value can no longer be delivered.
    suppression = await find_applicable_suppression(db_session, "a@b.com", channel="email")
    assert suppression is not None
    assert suppression.channel is None
    assert suppression.reason == SuppressionReason.LEGAL_REQUEST


@pytest.mark.asyncio
async def test_fulfill_deletion_erases_contact_source_evidence_and_lead_profile(db_session):
    # Correction regression test: deleting the ContactPoint row alone left
    # the same value sitting in FieldProvenance.asserted_value and in the
    # contributing RawSourceRecord's raw_payload/normalized_phone -- a
    # contact-level erasure reported verified: true while the value was
    # still stored locally in source evidence, and LeadProfile.has_phone
    # stayed stale.
    run = SourceRun(source_type=SourceType.WEBSITE, run_metadata={}, status=RunStatus.COMPLETED)
    db_session.add(run)
    await db_session.flush()

    raw_record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.WEBSITE,
        source_id=f"web:{uuid.uuid4().hex[:8]}",
        raw_payload={
            "phone": "+15550009999",
            "organization": "Evidence School",
            "email": "keep@example.com",
        },
        normalized_phone="+15550009999",
    )
    db_session.add(raw_record)
    await db_session.flush()

    institution = CanonicalInstitution(canonical_name="Evidence School")
    db_session.add(institution)
    await db_session.flush()

    contact = ContactPoint(
        institution_id=institution.id, contact_type="phone", contact_value="+15550009999"
    )
    db_session.add(contact)
    db_session.add(
        FieldProvenance(
            canonical_id=institution.id,
            raw_record_id=raw_record.id,
            field_name="contact_phone",
            asserted_value="+15550009999",
            assertion_trust=1.0,
        )
    )
    await db_session.flush()
    contact_id = contact.id
    raw_record_id = raw_record.id
    institution_id = institution.id

    request = await request_deletion(db_session, DeletionSubjectType.CONTACT_POINT, contact_id)
    fulfilled = await fulfill_deletion(db_session, request.id)

    assert fulfilled.manifest["redacted_source_records"] == 1

    remaining_provenance = (
        await db_session.scalars(
            select(FieldProvenance).where(
                FieldProvenance.canonical_id == institution_id,
                FieldProvenance.field_name == "contact_phone",
            )
        )
    ).all()
    assert remaining_provenance == []

    redacted_record = await db_session.get(RawSourceRecord, raw_record_id)
    assert redacted_record.normalized_phone is None
    assert redacted_record.raw_payload["phone"] == "[REDACTED]"
    # Unrelated evidence on the SAME raw record must survive untouched.
    assert redacted_record.raw_payload["organization"] == "Evidence School"
    assert redacted_record.raw_payload["email"] == "keep@example.com"

    profile = await db_session.scalar(
        select(LeadProfile).where(LeadProfile.institution_id == institution_id)
    )
    assert profile is not None
    assert profile.has_phone is False


@pytest.mark.asyncio
async def test_fulfill_deletion_raises_not_found_for_unknown_request(db_session):
    with pytest.raises(ResourceNotFoundError):
        await fulfill_deletion(db_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_fulfill_deletion_raises_not_found_when_subject_already_gone(db_session):
    institution = CanonicalInstitution(canonical_name="Already Gone School")
    db_session.add(institution)
    await db_session.flush()
    institution_id = institution.id
    request = await request_deletion(db_session, DeletionSubjectType.INSTITUTION, institution_id)
    await db_session.delete(institution)
    await db_session.flush()

    with pytest.raises(ResourceNotFoundError):
        await fulfill_deletion(db_session, request.id)


@pytest.mark.asyncio
async def test_fulfill_an_already_fulfilled_request_raises(db_session):
    institution = CanonicalInstitution(canonical_name="Double Fulfill School")
    db_session.add(institution)
    await db_session.flush()
    request = await request_deletion(db_session, DeletionSubjectType.INSTITUTION, institution.id)
    await fulfill_deletion(db_session, request.id)

    with pytest.raises(ValueError, match="not pending"):
        await fulfill_deletion(db_session, request.id)


@pytest.mark.asyncio
async def test_reject_deletion_marks_it_rejected_without_deleting_anything(db_session):
    institution = CanonicalInstitution(canonical_name="Rejected Deletion School")
    db_session.add(institution)
    await db_session.flush()
    institution_id = institution.id
    request = await request_deletion(db_session, DeletionSubjectType.INSTITUTION, institution_id)

    rejected = await reject_deletion(db_session, request.id, "insufficient verification")

    assert rejected.status == DeletionRequestStatus.REJECTED
    assert rejected.rejection_reason == "insufficient verification"
    remaining = await db_session.get(CanonicalInstitution, institution_id)
    assert remaining is not None


@pytest.mark.asyncio
async def test_list_deletion_requests_filters_by_status(db_session):
    institution = CanonicalInstitution(canonical_name="Filter Test School")
    db_session.add(institution)
    await db_session.flush()
    pending_request = await request_deletion(
        db_session, DeletionSubjectType.INSTITUTION, uuid.uuid4()
    )
    completed_request = await request_deletion(
        db_session, DeletionSubjectType.INSTITUTION, institution.id
    )
    await fulfill_deletion(db_session, completed_request.id)

    pending = await list_deletion_requests(db_session, status=DeletionRequestStatus.PENDING)
    completed = await list_deletion_requests(db_session, status=DeletionRequestStatus.COMPLETED)

    assert {r.id for r in pending} == {pending_request.id}
    assert {r.id for r in completed} == {completed_request.id}


async def _seed_raw_record(db_session, *, extracted_at, with_provenance: bool) -> RawSourceRecord:
    run = SourceRun(source_type=SourceType.GOOGLE_PLACES, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()
    record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.GOOGLE_PLACES,
        source_id=f"gp:{uuid.uuid4().hex[:8]}",
        raw_payload={},
        extracted_at=extracted_at,
    )
    db_session.add(record)
    await db_session.flush()
    if with_provenance:
        institution = CanonicalInstitution(canonical_name="Referenced School")
        db_session.add(institution)
        await db_session.flush()
        db_session.add(
            FieldProvenance(
                canonical_id=institution.id,
                raw_record_id=record.id,
                field_name="branch_membership",
                asserted_value=record.source_id,
            )
        )
        await db_session.flush()
    return record


@pytest.mark.asyncio
async def test_purge_expired_raw_records_deletes_only_old_unreferenced_rows(db_session):
    old_unreferenced = await _seed_raw_record(
        db_session,
        extracted_at=datetime.now(UTC) - timedelta(days=400),
        with_provenance=False,
    )
    old_referenced = await _seed_raw_record(
        db_session,
        extracted_at=datetime.now(UTC) - timedelta(days=400),
        with_provenance=True,
    )
    recent_unreferenced = await _seed_raw_record(
        db_session, extracted_at=datetime.now(UTC), with_provenance=False
    )

    deleted_count = await purge_expired_raw_records(db_session, retention_days=365)

    assert deleted_count == 1
    assert await db_session.get(RawSourceRecord, old_unreferenced.id) is None
    assert await db_session.get(RawSourceRecord, old_referenced.id) is not None
    assert await db_session.get(RawSourceRecord, recent_unreferenced.id) is not None


@pytest.mark.asyncio
async def test_purge_expired_raw_records_excludes_pending_review_candidates(db_session):
    # Correction: resolution_candidates' FKs to raw_source_records are now
    # ON DELETE CASCADE (added for _erase_institution's sake) -- without
    # this exclusion, purging an old, FieldProvenance-unreferenced raw
    # record would silently cascade-delete a live ResolutionCandidate (and
    # its MatchAssessment) still sitting in the resolution-reviews queue,
    # destroying real pending work instead of the FK violation this would
    # previously have raised.
    old_raw_record_pending = await _seed_raw_record(
        db_session, extracted_at=datetime.now(UTC) - timedelta(days=400), with_provenance=False
    )
    old_target_pending = await _seed_raw_record(
        db_session, extracted_at=datetime.now(UTC) - timedelta(days=400), with_provenance=False
    )
    old_raw_record_decided = await _seed_raw_record(
        db_session, extracted_at=datetime.now(UTC) - timedelta(days=400), with_provenance=False
    )
    other_record = await _seed_raw_record(
        db_session, extracted_at=datetime.now(UTC), with_provenance=False
    )

    db_session.add_all(
        [
            # Pending on the raw_record_id side.
            ResolutionCandidate(raw_record_id=old_raw_record_pending.id, blocking_strategy="phone"),
            # Pending on the target_raw_record_id side.
            ResolutionCandidate(
                raw_record_id=other_record.id,
                target_raw_record_id=old_target_pending.id,
                blocking_strategy="phone",
            ),
            # Already decided -- no longer blocks the purge.
            ResolutionCandidate(
                raw_record_id=old_raw_record_decided.id,
                blocking_strategy="phone",
                review_outcome=ReviewOutcome.SEPARATED,
            ),
        ]
    )
    await db_session.flush()

    deleted_count = await purge_expired_raw_records(db_session, retention_days=365)

    assert deleted_count == 1
    assert await db_session.get(RawSourceRecord, old_raw_record_pending.id) is not None
    assert await db_session.get(RawSourceRecord, old_target_pending.id) is not None
    assert await db_session.get(RawSourceRecord, old_raw_record_decided.id) is None


# Correction (docs/ROADMAP.md module 11): the deletion graph itself --
# fulfill_deletion must erase every dependent record type in one
# transaction, retain what's meant to be retained (AuditLog for lawful
# audit, SuppressionEntry as unrelated to institution lifecycle, a shared
# RawSourceRecord still evidencing another institution), and produce a
# manifest + verification result that actually reflects what happened.

_DEPENDENT_MODELS = (
    Branch,
    ContactPoint,
    AccountBrief,
    OutreachDraft,
    OutreachOutcome,
    ResolutionCandidate,
    MatchAssessment,
    FieldProvenance,
    QualificationAssessment,
    ResearchJob,
    ResearchFinding,
    PersonCandidate,
    Signal,
    DataQualityFlag,
    LeadReservation,
    LeadProfile,
    LeadScoreSnapshot,
    EventOutbox,
    RawPageSnapshot,
)


async def _seed_institution_with_every_dependent(db_session, *, name: str = "Full Graph School"):
    institution = CanonicalInstitution(canonical_name=name)
    db_session.add(institution)
    await db_session.flush()

    run = SourceRun(source_type=SourceType.WEBSITE, run_metadata={}, status=RunStatus.COMPLETED)
    db_session.add(run)
    await db_session.flush()

    raw_record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.WEBSITE,
        source_id=f"web:{uuid.uuid4().hex[:8]}",
        raw_payload={"phone": "+1 555 0100"},
    )
    db_session.add(raw_record)
    await db_session.flush()

    db_session.add(
        FieldProvenance(
            canonical_id=institution.id,
            raw_record_id=raw_record.id,
            field_name="canonical_name",
            asserted_value=name,
        )
    )

    db_session.add(
        Branch(
            institution_id=institution.id,
            branch_name="Main",
            address="1 Main St",
            city="Testville",
            country_code="US",
        )
    )

    person = PersonCandidate(
        institution_id=institution.id, display_name="Jane Doe", normalized_name="jane doe"
    )
    db_session.add(person)
    await db_session.flush()

    db_session.add(
        ContactPoint(
            institution_id=institution.id,
            contact_type="email",
            contact_value="jane@example.com",
            person_candidate_id=person.id,
        )
    )

    brief = AccountBrief(institution_id=institution.id)
    db_session.add(brief)
    await db_session.flush()

    draft = OutreachDraft(
        brief_id=brief.id,
        target_name="Jane Doe",
        target_role="Principal",
        target_contact_value="jane@example.com",
        status=DraftStatus.SENT,
    )
    db_session.add(draft)
    await db_session.flush()

    db_session.add(OutreachOutcome(draft_id=draft.id, opened=True))

    candidate = ResolutionCandidate(
        raw_record_id=raw_record.id,
        target_canonical_id=institution.id,
        blocking_strategy="blocking_domain",
    )
    db_session.add(candidate)
    await db_session.flush()

    db_session.add(
        MatchAssessment(candidate_id=candidate.id, decision=MatchDecision.MERGE, total_score=95.0)
    )

    db_session.add(
        QualificationAssessment(
            institution_id=institution.id, is_qualified=True, rationale="Good fit"
        )
    )

    job = ResearchJob(institution_id=institution.id, status=JobStatus.COMPLETED)
    db_session.add(job)
    await db_session.flush()

    db_session.add(
        ResearchFinding(
            institution_id=institution.id,
            job_id=job.id,
            finding_type=FindingType.FACT,
            finding_key="decision_maker_email",
            finding_value="jane@example.com",
        )
    )

    db_session.add(
        Signal(
            institution_id=institution.id,
            signal_type=SignalType.BUYING_SIGNAL,
            signal_text="Hiring a new IT director",
        )
    )

    db_session.add(
        DataQualityFlag(institution_id=institution.id, flag_type=FlagType.STALE_EVIDENCE)
    )

    db_session.add(
        LeadReservation(
            institution_id=institution.id,
            score_at_reservation=80,
            batch_label="2026-08-01",
            expires_at=datetime.now(UTC) + timedelta(days=1),
        )
    )

    db_session.add(LeadProfile(institution_id=institution.id, overall_score=80))
    db_session.add(LeadScoreSnapshot(institution_id=institution.id, overall_score=80))

    db_session.add(
        EventOutbox(
            institution_id=institution.id,
            event_type="institution.upserted",
            payload={"institution": {"id": str(institution.id)}},
            status=OutboxStatus.DELIVERED,
        )
    )

    db_session.add(
        RawPageSnapshot(
            source_run_id=run.id,
            url="https://example.com",
            final_url="https://example.com",
            normalized_domain="example.com",
            raw_source_record_id=raw_record.id,
            institution_id=institution.id,
            status_code=200,
        )
    )

    # Retained-for-lawful-audit: an AuditLog row about this institution
    # must survive the erasure untouched -- see models/audit.py.
    db_session.add(
        AuditLog(
            action="institution.created",
            actor="system",
            entity_type="CanonicalInstitution",
            entity_id=institution.id,
        )
    )

    # Retained-as-unrelated-to-institution-lifecycle: a suppression keyed
    # by this institution's contact's email must also survive.
    await add_suppression(db_session, "jane@example.com", SuppressionReason.OPT_OUT)

    await db_session.flush()
    return institution, raw_record


@pytest.mark.asyncio
async def test_fulfill_deletion_erases_every_dependent_record_type_in_one_transaction(db_session):
    institution, raw_record = await _seed_institution_with_every_dependent(db_session)
    institution_id = institution.id
    raw_record_id = raw_record.id

    request = await request_deletion(
        db_session, DeletionSubjectType.INSTITUTION, institution_id, "GDPR request"
    )
    fulfilled = await fulfill_deletion(db_session, request.id)

    assert fulfilled.status == DeletionRequestStatus.COMPLETED
    manifest = fulfilled.manifest
    assert manifest["verified"] is True
    assert manifest["residual_counts"] == {}
    assert manifest["deleted_counts"] == {
        "branches": 1,
        "contact_points": 1,
        "account_briefs": 1,
        "outreach_drafts": 1,
        "outreach_outcomes": 1,
        "resolution_candidates": 1,
        "match_assessments": 1,
        "field_provenance": 1,
        "qualification_assessments": 1,
        "research_jobs": 1,
        "research_findings": 1,
        "person_candidates": 1,
        "signals": 1,
        "data_quality_flags": 1,
        "lead_reservations": 1,
        "lead_profiles": 1,
        "lead_score_history": 1,
        "event_outbox": 1,
        "raw_page_snapshots": 1,
        "raw_source_records": 1,
    }
    assert manifest["retained"]["shared_raw_source_records"] == []

    assert await db_session.get(CanonicalInstitution, institution_id) is None
    # A fresh query, not db_session.get() -- the exclusive RawSourceRecord
    # purge runs as a Core DELETE (see _erase_institution), which never
    # updates this session's identity map for objects it didn't load
    # itself, so only a real SELECT reliably reflects the database here.
    remaining_raw_records = await db_session.scalar(
        select(func.count()).select_from(RawSourceRecord).where(RawSourceRecord.id == raw_record_id)
    )
    assert remaining_raw_records == 0
    for model in _DEPENDENT_MODELS:
        count = await db_session.scalar(select(func.count()).select_from(model))
        assert count == 0, f"{model.__name__} rows survived erasure"

    # Retained for lawful audit: the pre-existing AuditLog row about this
    # institution, plus the new one fulfill_deletion itself writes.
    audit_rows = (await db_session.scalars(select(AuditLog))).all()
    assert any(row.entity_id == institution_id for row in audit_rows)
    fulfillment_rows = [row for row in audit_rows if row.action == "deletion_request.fulfilled"]
    assert len(fulfillment_rows) == 1
    assert fulfillment_rows[0].entity_id == request.id
    assert fulfillment_rows[0].new_state == manifest

    # Retained as unrelated to institution lifecycle: the suppression entry.
    suppressed = await find_applicable_suppression(db_session, "jane@example.com", channel="email")
    assert suppressed is not None


@pytest.mark.asyncio
async def test_fulfill_deletion_retains_a_raw_source_record_shared_with_another_institution(
    db_session,
):
    institution_a = CanonicalInstitution(canonical_name="Institution A")
    institution_b = CanonicalInstitution(canonical_name="Institution B")
    db_session.add_all([institution_a, institution_b])
    await db_session.flush()

    run = SourceRun(
        source_type=SourceType.GOOGLE_PLACES, run_metadata={}, status=RunStatus.COMPLETED
    )
    db_session.add(run)
    await db_session.flush()

    shared_record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.GOOGLE_PLACES,
        source_id=f"gp:{uuid.uuid4().hex[:8]}",
        raw_payload={},
    )
    db_session.add(shared_record)
    await db_session.flush()

    db_session.add_all(
        [
            FieldProvenance(
                canonical_id=institution_a.id,
                raw_record_id=shared_record.id,
                field_name="canonical_name",
                asserted_value="Institution A",
            ),
            FieldProvenance(
                canonical_id=institution_b.id,
                raw_record_id=shared_record.id,
                field_name="canonical_name",
                asserted_value="Institution B",
            ),
        ]
    )
    await db_session.flush()

    request = await request_deletion(db_session, DeletionSubjectType.INSTITUTION, institution_a.id)
    fulfilled = await fulfill_deletion(db_session, request.id)

    manifest = fulfilled.manifest
    assert manifest["verified"] is True
    assert manifest["deleted_counts"]["raw_source_records"] == 0
    assert manifest["retained"]["shared_raw_source_records"] == [str(shared_record.id)]

    assert await db_session.get(CanonicalInstitution, institution_a.id) is None
    assert await db_session.get(CanonicalInstitution, institution_b.id) is not None
    assert await db_session.get(RawSourceRecord, shared_record.id) is not None
    remaining_provenance = (
        await db_session.scalars(
            select(FieldProvenance).where(FieldProvenance.raw_record_id == shared_record.id)
        )
    ).all()
    assert len(remaining_provenance) == 1
    assert remaining_provenance[0].canonical_id == institution_b.id


@pytest.mark.asyncio
async def test_fulfill_deletion_counts_candidates_cascaded_via_raw_record_id(db_session):
    # Correction: resolution/blocking.py's normal candidate-generation
    # shape uses raw_record_id/target_raw_record_id, not target_canonical_id
    # -- a candidate shaped this way still gets cascade-deleted when its
    # raw record is exclusively purged, and the manifest must count it,
    # not just the target_canonical_id shape covered by the other tests.
    institution = CanonicalInstitution(canonical_name="Blocking Path School")
    db_session.add(institution)
    await db_session.flush()

    run = SourceRun(
        source_type=SourceType.GOOGLE_PLACES, run_metadata={}, status=RunStatus.COMPLETED
    )
    db_session.add(run)
    await db_session.flush()

    raw_record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.GOOGLE_PLACES,
        source_id=f"gp:{uuid.uuid4().hex[:8]}",
        raw_payload={},
    )
    other_record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.GOOGLE_PLACES,
        source_id=f"gp:{uuid.uuid4().hex[:8]}",
        raw_payload={},
    )
    db_session.add_all([raw_record, other_record])
    await db_session.flush()

    db_session.add(
        FieldProvenance(
            canonical_id=institution.id,
            raw_record_id=raw_record.id,
            field_name="canonical_name",
            asserted_value="Blocking Path School",
        )
    )

    # No target_canonical_id at all -- exactly the shape blocking.py
    # actually produces, and the shape the old count missed.
    candidate = ResolutionCandidate(
        raw_record_id=raw_record.id,
        target_raw_record_id=other_record.id,
        blocking_strategy="blocking_domain",
    )
    db_session.add(candidate)
    await db_session.flush()

    db_session.add(
        MatchAssessment(candidate_id=candidate.id, decision=MatchDecision.PENDING, total_score=40.0)
    )
    await db_session.flush()

    request = await request_deletion(db_session, DeletionSubjectType.INSTITUTION, institution.id)
    fulfilled = await fulfill_deletion(db_session, request.id)

    manifest = fulfilled.manifest
    assert manifest["verified"] is True
    assert manifest["deleted_counts"]["resolution_candidates"] == 1
    assert manifest["deleted_counts"]["match_assessments"] == 1
    assert (await db_session.scalar(select(func.count()).select_from(ResolutionCandidate))) == 0
    assert (await db_session.scalar(select(func.count()).select_from(MatchAssessment))) == 0


@pytest.mark.asyncio
async def test_fulfill_deletion_enqueues_downstream_event_when_previously_synced(
    db_session, monkeypatch
):
    from lead_harvester.config import settings as app_settings

    monkeypatch.setattr(app_settings, "lead_sync_enabled", True)
    monkeypatch.setattr(app_settings, "lead_sync_webhook_url", "https://core-newax.test/webhook")

    institution = CanonicalInstitution(
        canonical_name="Already Synced School", lead_synced_at=datetime.now(UTC)
    )
    db_session.add(institution)
    await db_session.flush()
    institution_id = institution.id

    request = await request_deletion(db_session, DeletionSubjectType.INSTITUTION, institution_id)
    fulfilled = await fulfill_deletion(db_session, request.id)

    assert fulfilled.manifest["downstream_deletion_event_enqueued"] is True

    tombstones = (
        await db_session.scalars(
            select(EventOutbox).where(EventOutbox.event_type == "institution.deleted")
        )
    ).all()
    assert len(tombstones) == 1
    tombstone = tombstones[0]
    # NULL, not institution_id -- the institution row it's about is gone
    # in this same transaction; this FK's CASCADE would otherwise delete
    # the tombstone right along with it. See models/outbox.py.
    assert tombstone.institution_id is None
    assert tombstone.status == OutboxStatus.PENDING
    assert tombstone.payload["institution"]["id"] == str(institution_id)


@pytest.mark.asyncio
async def test_fulfill_deletion_skips_downstream_event_when_never_synced(db_session, monkeypatch):
    from lead_harvester.config import settings as app_settings

    monkeypatch.setattr(app_settings, "lead_sync_enabled", True)
    monkeypatch.setattr(app_settings, "lead_sync_webhook_url", "https://core-newax.test/webhook")

    # lead_synced_at is never set -- this institution was never mirrored,
    # so there is nothing downstream to tell about its erasure.
    institution = CanonicalInstitution(canonical_name="Never Synced School")
    db_session.add(institution)
    await db_session.flush()

    request = await request_deletion(db_session, DeletionSubjectType.INSTITUTION, institution.id)
    fulfilled = await fulfill_deletion(db_session, request.id)

    assert fulfilled.manifest["downstream_deletion_event_enqueued"] is False
    tombstones = (
        await db_session.scalars(
            select(EventOutbox).where(EventOutbox.event_type == "institution.deleted")
        )
    ).all()
    assert tombstones == []


@pytest.mark.asyncio
async def test_fulfill_deletion_persists_tombstone_even_when_lead_sync_currently_disabled(
    db_session,
):
    # Correction regression test: lead_sync is disabled by default in test
    # settings, but a previously-synced institution's tombstone must still
    # be persisted -- the institution and its own EventOutbox history are
    # both about to be deleted in this same transaction, so skipping the
    # tombstone here would silently drop it forever with no later chance to
    # reconstruct it once sync is re-enabled. Delivery is deferred to the
    # normal outbox retry machinery, not creation.
    institution = CanonicalInstitution(
        canonical_name="Synced But Sync Now Off School", lead_synced_at=datetime.now(UTC)
    )
    db_session.add(institution)
    await db_session.flush()
    institution_id = institution.id

    request = await request_deletion(db_session, DeletionSubjectType.INSTITUTION, institution.id)
    fulfilled = await fulfill_deletion(db_session, request.id)

    assert fulfilled.manifest["downstream_deletion_event_enqueued"] is True
    tombstones = (
        await db_session.scalars(
            select(EventOutbox).where(EventOutbox.event_type == "institution.deleted")
        )
    ).all()
    assert len(tombstones) == 1
    assert tombstones[0].institution_id is None
    assert tombstones[0].status == OutboxStatus.PENDING
    assert tombstones[0].payload["institution"]["id"] == str(institution_id)


@pytest.mark.asyncio
async def test_fulfill_deletion_resyncs_institution_after_contact_erasure_when_synced(
    db_session, monkeypatch
):
    from unittest.mock import AsyncMock, patch

    import httpx

    from lead_harvester.config import settings as app_settings

    monkeypatch.setattr(app_settings, "lead_sync_enabled", True)
    monkeypatch.setattr(app_settings, "lead_sync_webhook_url", "https://core-newax.test/webhook")
    monkeypatch.setattr(
        app_settings, "lead_sync_webhook_secret", "test-secret-with-more-than-32-characters"
    )

    institution = CanonicalInstitution(
        canonical_name="Synced Contact School", lead_synced_at=datetime.now(UTC)
    )
    db_session.add(institution)
    await db_session.flush()
    kept_contact = ContactPoint(
        institution_id=institution.id, contact_type="phone", contact_value="+15550001111"
    )
    erased_contact = ContactPoint(
        institution_id=institution.id, contact_type="email", contact_value="erase-me@example.com"
    )
    db_session.add_all([kept_contact, erased_contact])
    await db_session.flush()
    erased_contact_id = erased_contact.id

    mock_response = httpx.Response(
        200, request=httpx.Request("POST", "https://core-newax.test/webhook")
    )
    with patch.object(httpx.AsyncClient, "post", new=AsyncMock(return_value=mock_response)):
        request = await request_deletion(
            db_session, DeletionSubjectType.CONTACT_POINT, erased_contact_id
        )
        fulfilled = await fulfill_deletion(db_session, request.id)

    assert fulfilled.manifest["downstream_resync_enqueued"] is True

    outbox_rows = (
        await db_session.scalars(
            select(EventOutbox).where(EventOutbox.event_type == "institution.upserted")
        )
    ).all()
    assert len(outbox_rows) == 1
    contact_values = {c["contactValue"] for c in outbox_rows[0].payload["contactPoints"]}
    # The erased contact must be absent from the re-synced payload, not
    # just from our own local table -- otherwise the mirror still has it.
    assert "erase-me@example.com" not in contact_values
    assert "+15550001111" in contact_values
    assert outbox_rows[0].status == OutboxStatus.DELIVERED


@pytest.mark.asyncio
async def test_fulfill_deletion_skips_resync_after_contact_erasure_when_never_synced(db_session):
    institution = CanonicalInstitution(canonical_name="Never Synced Contact School")
    db_session.add(institution)
    await db_session.flush()
    contact = ContactPoint(
        institution_id=institution.id, contact_type="email", contact_value="a@b.com"
    )
    db_session.add(contact)
    await db_session.flush()

    request = await request_deletion(db_session, DeletionSubjectType.CONTACT_POINT, contact.id)
    fulfilled = await fulfill_deletion(db_session, request.id)

    assert fulfilled.manifest["downstream_resync_enqueued"] is False
    outbox_rows = (await db_session.scalars(select(EventOutbox))).all()
    assert outbox_rows == []
