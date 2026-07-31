import uuid
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select

from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.models.canonical import CanonicalInstitution, ContactPoint
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.verification import DataQualityFlag, FlagStatus, FlagType
from lead_harvester.services.verification_service import (
    dismiss_flag,
    flag_contact_unreachable,
    list_flags,
    resolve_flag,
    run_verification_checks,
    run_verification_sweep,
)
from lead_harvester.verification.confidence import confidence_for_source_count


async def _seed_institution(db_session, **overrides) -> CanonicalInstitution:
    defaults = {"canonical_name": "Riverside Academy", "confidence_score": 10.0}
    defaults.update(overrides)
    institution = CanonicalInstitution(**defaults)
    db_session.add(institution)
    await db_session.flush()
    return institution


async def _add_branch_membership(db_session, institution_id, *, created_at=None):
    from lead_harvester.models.source import RawSourceRecord, RunStatus, SourceRun, SourceType

    run = SourceRun(source_type=SourceType.GOOGLE_PLACES, run_metadata={}, status=RunStatus.STARTED)
    db_session.add(run)
    await db_session.flush()
    record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.GOOGLE_PLACES,
        source_id=f"gp:{uuid.uuid4().hex[:8]}",
        raw_payload={},
    )
    db_session.add(record)
    await db_session.flush()
    fp = FieldProvenance(
        canonical_id=institution_id,
        raw_record_id=record.id,
        field_name="branch_membership",
        asserted_value=record.source_id,
    )
    if created_at is not None:
        fp.created_at = created_at
    db_session.add(fp)
    await db_session.flush()
    return fp


@pytest.mark.asyncio
async def test_run_verification_checks_flags_confidence_drift(db_session):
    institution = await _seed_institution(db_session, confidence_score=10.0)
    await _add_branch_membership(db_session, institution.id)
    await _add_branch_membership(db_session, institution.id)

    created = await run_verification_checks(db_session, institution.id)

    drift_flags = [f for f in created if f.flag_type == FlagType.CONFIDENCE_DRIFT]
    assert len(drift_flags) == 1
    assert drift_flags[0].details["expected"] == confidence_for_source_count(2)


@pytest.mark.asyncio
async def test_run_verification_checks_does_not_flag_matching_confidence(db_session):
    institution = await _seed_institution(
        db_session, confidence_score=confidence_for_source_count(1)
    )
    await _add_branch_membership(db_session, institution.id)

    created = await run_verification_checks(db_session, institution.id)

    assert [f for f in created if f.flag_type == FlagType.CONFIDENCE_DRIFT] == []


@pytest.mark.asyncio
async def test_run_verification_checks_does_not_duplicate_an_existing_open_flag(db_session):
    institution = await _seed_institution(db_session, confidence_score=10.0)
    await _add_branch_membership(db_session, institution.id)
    await _add_branch_membership(db_session, institution.id)

    first_pass = await run_verification_checks(db_session, institution.id)
    second_pass = await run_verification_checks(db_session, institution.id)

    assert len(first_pass) == 1
    assert second_pass == []

    all_flags = (
        await db_session.scalars(
            select(DataQualityFlag).where(DataQualityFlag.institution_id == institution.id)
        )
    ).all()
    assert len(all_flags) == 1


@pytest.mark.asyncio
async def test_run_verification_checks_flags_stale_evidence(db_session):
    institution = await _seed_institution(
        db_session, confidence_score=confidence_for_source_count(1)
    )
    await _add_branch_membership(
        db_session, institution.id, created_at=datetime.now(UTC) - timedelta(days=200)
    )

    created = await run_verification_checks(db_session, institution.id, freshness_days=90)

    stale_flags = [f for f in created if f.flag_type == FlagType.STALE_EVIDENCE]
    assert len(stale_flags) == 1


@pytest.mark.asyncio
async def test_run_verification_checks_flags_conflicting_canonical_name(db_session):
    institution = await _seed_institution(
        db_session, confidence_score=confidence_for_source_count(1)
    )
    fp = await _add_branch_membership(db_session, institution.id)
    db_session.add(
        FieldProvenance(
            canonical_id=institution.id,
            raw_record_id=fp.raw_record_id,
            field_name="canonical_name",
            asserted_value="Riverside Academy",
        )
    )
    db_session.add(
        FieldProvenance(
            canonical_id=institution.id,
            raw_record_id=fp.raw_record_id,
            field_name="canonical_name",
            asserted_value="Completely Different School",
        )
    )
    await db_session.flush()

    created = await run_verification_checks(db_session, institution.id)

    conflict_flags = [f for f in created if f.flag_type == FlagType.CONFLICTING_FIELD]
    assert len(conflict_flags) == 1
    assert conflict_flags[0].field_name == "canonical_name"


@pytest.mark.asyncio
async def test_run_verification_checks_raises_not_found_for_unknown_institution(db_session):
    with pytest.raises(ResourceNotFoundError):
        await run_verification_checks(db_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_run_verification_sweep_isolates_one_institutions_failure(db_session, monkeypatch):
    # Savepoint isolation (docs/CODE_REVIEW_LESSONS.md pattern 3) -- one
    # institution's check failing must not stop the others from being
    # checked.
    good_one = await _seed_institution(
        db_session, canonical_name="Good School One", confidence_score=10.0
    )
    await _add_branch_membership(db_session, good_one.id)
    await _add_branch_membership(db_session, good_one.id)
    bad_one = await _seed_institution(
        db_session, canonical_name="Bad School", confidence_score=10.0
    )
    await _add_branch_membership(db_session, bad_one.id)
    await _add_branch_membership(db_session, bad_one.id)
    good_two = await _seed_institution(
        db_session, canonical_name="Good School Two", confidence_score=10.0
    )
    await _add_branch_membership(db_session, good_two.id)
    await _add_branch_membership(db_session, good_two.id)

    from lead_harvester.services import verification_service as service_module

    real_run_checks = service_module.run_verification_checks

    async def flaky_run_checks(session, institution_id, **kwargs):
        if institution_id == bad_one.id:
            raise RuntimeError("simulated check failure")
        return await real_run_checks(session, institution_id, **kwargs)

    monkeypatch.setattr(service_module, "run_verification_checks", flaky_run_checks)

    total_created = await run_verification_sweep(db_session, limit=200)

    assert total_created == 2
    for inst in (good_one, good_two):
        flags = (
            await db_session.scalars(
                select(DataQualityFlag).where(DataQualityFlag.institution_id == inst.id)
            )
        ).all()
        assert len(flags) == 1
    bad_flags = (
        await db_session.scalars(
            select(DataQualityFlag).where(DataQualityFlag.institution_id == bad_one.id)
        )
    ).all()
    assert bad_flags == []


@pytest.mark.asyncio
async def test_resolve_flag_transitions_status(db_session):
    institution = await _seed_institution(db_session, confidence_score=10.0)
    await _add_branch_membership(db_session, institution.id)
    await _add_branch_membership(db_session, institution.id)
    created = await run_verification_checks(db_session, institution.id)
    flag_id = created[0].id

    resolved = await resolve_flag(db_session, flag_id, "fixed manually")

    assert resolved.status == FlagStatus.RESOLVED
    assert resolved.resolved_at is not None
    assert resolved.resolution_note == "fixed manually"


@pytest.mark.asyncio
async def test_dismiss_flag_transitions_status(db_session):
    institution = await _seed_institution(db_session, confidence_score=10.0)
    await _add_branch_membership(db_session, institution.id)
    await _add_branch_membership(db_session, institution.id)
    created = await run_verification_checks(db_session, institution.id)
    flag_id = created[0].id

    dismissed = await dismiss_flag(db_session, flag_id, "false positive")

    assert dismissed.status == FlagStatus.DISMISSED
    assert dismissed.resolution_note == "false positive"


@pytest.mark.asyncio
async def test_resolve_flag_raises_not_found(db_session):
    with pytest.raises(ResourceNotFoundError):
        await resolve_flag(db_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_resolve_an_already_resolved_flag_raises(db_session):
    institution = await _seed_institution(db_session, confidence_score=10.0)
    await _add_branch_membership(db_session, institution.id)
    await _add_branch_membership(db_session, institution.id)
    created = await run_verification_checks(db_session, institution.id)
    flag_id = created[0].id
    await resolve_flag(db_session, flag_id)

    with pytest.raises(ValueError, match="not open"):
        await resolve_flag(db_session, flag_id)


@pytest.mark.asyncio
async def test_flag_contact_unreachable_creates_a_flag(db_session):
    institution = await _seed_institution(db_session)
    contact = ContactPoint(
        institution_id=institution.id, contact_type="email", contact_value="a@b.com"
    )
    db_session.add(contact)
    await db_session.flush()

    flag = await flag_contact_unreachable(db_session, contact.id, "bounced")

    assert flag.flag_type == FlagType.UNREACHABLE_CONTACT
    assert flag.institution_id == institution.id
    assert flag.details["contact_value"] == "a@b.com"
    assert flag.details["note"] == "bounced"


@pytest.mark.asyncio
async def test_flag_contact_unreachable_does_not_duplicate_an_open_flag(db_session):
    institution = await _seed_institution(db_session)
    contact = ContactPoint(
        institution_id=institution.id, contact_type="email", contact_value="a@b.com"
    )
    db_session.add(contact)
    await db_session.flush()

    first = await flag_contact_unreachable(db_session, contact.id)
    second = await flag_contact_unreachable(db_session, contact.id)

    assert first.id == second.id
    flags = (
        await db_session.scalars(
            select(DataQualityFlag).where(DataQualityFlag.institution_id == institution.id)
        )
    ).all()
    assert len(flags) == 1


@pytest.mark.asyncio
async def test_flag_contact_unreachable_raises_not_found(db_session):
    with pytest.raises(ResourceNotFoundError):
        await flag_contact_unreachable(db_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_list_flags_filters_by_status_and_type(db_session):
    institution = await _seed_institution(db_session, confidence_score=10.0)
    await _add_branch_membership(db_session, institution.id)
    await _add_branch_membership(db_session, institution.id)
    created = await run_verification_checks(db_session, institution.id)
    await resolve_flag(db_session, created[0].id)

    open_flags = await list_flags(db_session, status=FlagStatus.OPEN)
    resolved_flags = await list_flags(db_session, status=FlagStatus.RESOLVED)
    drift_flags = await list_flags(db_session, flag_type=FlagType.CONFIDENCE_DRIFT)

    assert open_flags == []
    assert len(resolved_flags) == 1
    assert len(drift_flags) == 1
