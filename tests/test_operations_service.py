import uuid
from datetime import UTC, datetime, timedelta

import pytest

from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.config import Settings
from lead_harvester.models.audit import AuditLog
from lead_harvester.models.canonical import CanonicalInstitution, OperatingStatus
from lead_harvester.models.compliance import SuppressionEntry, SuppressionReason
from lead_harvester.models.outbox import EventOutbox, OutboxStatus
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.resolution import ResolutionCandidate
from lead_harvester.models.source import (
    RawPageSnapshot,
    RawSourceRecord,
    RunStatus,
    SourceRun,
    SourceType,
)
from lead_harvester.models.verification import DataQualityFlag, FlagStatus, FlagType
from lead_harvester.services.operations_service import (
    check_health,
    compute_operational_metrics,
    compute_source_health,
    get_sanitized_config,
    get_source_run_detail,
    list_audit_log,
    list_page_snapshots,
    list_source_runs,
    list_stranded_records,
)


def _run(
    *,
    source_type: SourceType = SourceType.GOOGLE_PLACES,
    status: RunStatus = RunStatus.COMPLETED,
    started_at: datetime | None = None,
    run_metadata: dict | None = None,
) -> SourceRun:
    return SourceRun(
        source_type=source_type,
        status=status,
        started_at=started_at or datetime.now(UTC),
        run_metadata=run_metadata or {},
    )


def _record(run_id, *, source_type: SourceType = SourceType.GOOGLE_PLACES) -> RawSourceRecord:
    source_id = f"src:{uuid.uuid4().hex[:8]}"
    return RawSourceRecord(
        source_run_id=run_id,
        source_type=source_type,
        source_id=source_id,
        raw_payload={},
    )


@pytest.mark.asyncio
async def test_list_source_runs_filters_by_type_and_status(db_session):
    matching = _run(source_type=SourceType.GOOGLE_PLACES, status=RunStatus.COMPLETED)
    other_type = _run(source_type=SourceType.WEBSITE, status=RunStatus.COMPLETED)
    other_status = _run(source_type=SourceType.GOOGLE_PLACES, status=RunStatus.FAILED)
    db_session.add_all([matching, other_type, other_status])
    await db_session.flush()

    runs = await list_source_runs(
        db_session, source_type=SourceType.GOOGLE_PLACES, status=RunStatus.COMPLETED
    )

    assert [r.id for r in runs] == [matching.id]


def _snapshot(
    run_id, *, url: str = "https://example.edu/", fetch_error: str = ""
) -> RawPageSnapshot:
    return RawPageSnapshot(
        source_run_id=run_id,
        url=url,
        final_url=url if not fetch_error else "",
        status_code=200 if not fetch_error else None,
        content_type="text/html" if not fetch_error else "",
        html="<html></html>" if not fetch_error else None,
        fetch_error=fetch_error,
    )


@pytest.mark.asyncio
async def test_list_page_snapshots_filters_by_source_run(db_session):
    run_a = _run(source_type=SourceType.WEBSITE)
    run_b = _run(source_type=SourceType.WEBSITE)
    db_session.add_all([run_a, run_b])
    await db_session.flush()
    db_session.add_all(
        [_snapshot(run_a.id, url="https://a.edu/"), _snapshot(run_b.id, url="https://b.edu/")]
    )
    await db_session.flush()

    results = await list_page_snapshots(db_session, source_run_id=run_a.id)

    assert [r.url for r in results] == ["https://a.edu/"]


@pytest.mark.asyncio
async def test_list_page_snapshots_only_errors_filters_out_successes(db_session):
    run = _run(source_type=SourceType.WEBSITE)
    db_session.add(run)
    await db_session.flush()
    db_session.add_all(
        [
            _snapshot(run.id, url="https://ok.edu/"),
            _snapshot(run.id, url="https://blocked.edu/", fetch_error="robots_disallowed"),
        ]
    )
    await db_session.flush()

    results = await list_page_snapshots(db_session, source_run_id=run.id, only_errors=True)

    assert [r.url for r in results] == ["https://blocked.edu/"]


@pytest.mark.asyncio
async def test_get_source_run_detail_returns_record_count_and_unresolved(db_session):
    run = _run(run_metadata={"unresolved_records": [{"raw_record_id": "abc", "error": "boom"}]})
    db_session.add(run)
    await db_session.flush()
    db_session.add_all([_record(run.id), _record(run.id)])
    await db_session.flush()

    detail = await get_source_run_detail(db_session, run.id)

    assert detail["run"].id == run.id
    assert detail["record_count"] == 2
    assert detail["unresolved_records"] == [{"raw_record_id": "abc", "error": "boom"}]


@pytest.mark.asyncio
async def test_get_source_run_detail_raises_not_found_for_unknown_id(db_session):
    with pytest.raises(ResourceNotFoundError):
        await get_source_run_detail(db_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_compute_source_health_reports_last_run_and_recent_failures(db_session):
    old_success = _run(
        source_type=SourceType.GOOGLE_PLACES,
        status=RunStatus.COMPLETED,
        started_at=datetime.now(UTC) - timedelta(days=3),
    )
    recent_failure = _run(
        source_type=SourceType.GOOGLE_PLACES,
        status=RunStatus.FAILED,
        started_at=datetime.now(UTC) - timedelta(hours=1),
    )
    db_session.add_all([old_success, recent_failure])
    await db_session.flush()

    health = await compute_source_health(db_session)

    google_places_health = next(
        h for h in health if h["source_type"] == SourceType.GOOGLE_PLACES.value
    )
    assert google_places_health["last_run_status"] == "failed"
    assert google_places_health["last_successful_run_at"] == old_success.started_at
    assert google_places_health["failed_run_count_last_7d"] == 1


@pytest.mark.asyncio
async def test_compute_source_health_omits_source_types_with_no_runs(db_session):
    health = await compute_source_health(db_session)
    assert health == []


@pytest.mark.asyncio
async def test_list_stranded_records_excludes_canonicalized_and_pending_review(db_session):
    run = _run()
    db_session.add(run)
    await db_session.flush()

    stranded = _record(run.id, source_type=SourceType.GOOGLE_PLACES)
    canonicalized = _record(run.id, source_type=SourceType.GOOGLE_PLACES)
    pending_review = _record(run.id, source_type=SourceType.GOOGLE_PLACES)
    ineligible_type = _record(run.id, source_type=SourceType.LINKEDIN)
    db_session.add_all([stranded, canonicalized, pending_review, ineligible_type])
    await db_session.flush()

    institution = CanonicalInstitution(canonical_name="Provenance School")
    db_session.add(institution)
    await db_session.flush()
    db_session.add(
        FieldProvenance(
            canonical_id=institution.id,
            raw_record_id=canonicalized.id,
            field_name="branch_membership",
            asserted_value=canonicalized.source_id,
        )
    )
    db_session.add(
        ResolutionCandidate(
            raw_record_id=pending_review.id,
            target_canonical_id=institution.id,
            blocking_strategy="phone",
            version=1,
        )
    )
    await db_session.flush()

    results = await list_stranded_records(db_session)

    assert [r.id for r in results] == [stranded.id]


@pytest.mark.asyncio
async def test_list_audit_log_filters_by_entity_type_and_actor(db_session):
    matching = AuditLog(
        action="draft.approved",
        actor="reviewer-1",
        entity_type="OutreachDraft",
        entity_id=uuid.uuid4(),
    )
    other_actor = AuditLog(
        action="draft.approved",
        actor="reviewer-2",
        entity_type="OutreachDraft",
        entity_id=uuid.uuid4(),
    )
    other_entity_type = AuditLog(
        action="resolution.merged",
        actor="reviewer-1",
        entity_type="ResolutionCandidate",
        entity_id=uuid.uuid4(),
    )
    db_session.add_all([matching, other_actor, other_entity_type])
    await db_session.flush()

    results = await list_audit_log(db_session, entity_type="OutreachDraft", actor="reviewer-1")

    assert [r.id for r in results] == [matching.id]


def test_get_sanitized_config_excludes_secrets_and_credentials():
    settings = Settings(
        lead_sync_enabled=True,
        lead_sync_webhook_url="https://core-newax.test/webhook",
        lead_sync_webhook_secret="a-very-secret-value-that-must-never-leak",
        google_places_api_key="also-a-secret-api-key",
    )

    config = get_sanitized_config(settings)

    assert "database_url" not in config
    assert "test_database_url" not in config
    assert "google_places_api_key" not in config
    assert "lead_sync_webhook_secret" not in config
    assert "lead_sync_webhook_url" not in config
    assert config["lead_sync_enabled"] is True
    assert config["app_env"] == "development"


@pytest.mark.asyncio
async def test_compute_operational_metrics_aggregates_across_modules(db_session):
    institution = CanonicalInstitution(
        canonical_name="Metrics School", status=OperatingStatus.OPERATIONAL
    )
    db_session.add(institution)
    await db_session.flush()

    db_session.add(
        EventOutbox(
            institution_id=institution.id,
            event_type="institution.upserted",
            payload={"eventId": str(uuid.uuid4())},
            status=OutboxStatus.PENDING,
            next_attempt_at=datetime.now(UTC),
        )
    )
    db_session.add(
        EventOutbox(
            institution_id=institution.id,
            event_type="institution.upserted",
            payload={"eventId": str(uuid.uuid4())},
            status=OutboxStatus.DEAD_LETTER,
            next_attempt_at=datetime.now(UTC),
        )
    )
    db_session.add(
        DataQualityFlag(
            institution_id=institution.id,
            flag_type=FlagType.STALE_EVIDENCE,
            details={},
            status=FlagStatus.OPEN,
        )
    )
    db_session.add(
        SuppressionEntry(normalized_contact_value="+923001234567", reason=SuppressionReason.MANUAL)
    )
    await db_session.flush()

    metrics = await compute_operational_metrics(db_session)

    assert metrics["outbox_pending"] == 1
    assert metrics["outbox_dead_letter"] == 1
    assert metrics["open_data_quality_flags"] == 1
    assert metrics["suppressed_contacts"] == 1
    assert metrics["total_canonical_institutions"] >= 1


@pytest.mark.asyncio
async def test_check_health_reports_healthy_with_no_stuck_runs(db_session):
    db_session.add(_run(status=RunStatus.COMPLETED))
    await db_session.flush()

    result = await check_health(db_session)

    assert result["database_ok"] is True
    assert result["stuck_run_count"] == 0
    assert result["healthy"] is True


@pytest.mark.asyncio
async def test_check_health_flags_a_run_stuck_in_started(db_session):
    stuck = _run(status=RunStatus.STARTED, started_at=datetime.now(UTC) - timedelta(hours=6))
    recent = _run(status=RunStatus.STARTED, started_at=datetime.now(UTC) - timedelta(minutes=5))
    db_session.add_all([stuck, recent])
    await db_session.flush()

    result = await check_health(db_session)

    assert result["stuck_run_count"] == 1
    assert result["stuck_run_ids"] == [str(stuck.id)]
    assert result["healthy"] is False
