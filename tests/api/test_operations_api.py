import uuid
from datetime import UTC, datetime, timedelta

import pytest

from lead_harvester.models.audit import AuditLog
from lead_harvester.models.source import RawSourceRecord, RunStatus, SourceRun, SourceType


def _run(
    *, status: RunStatus = RunStatus.COMPLETED, source_type: SourceType = SourceType.GOOGLE_PLACES
):
    return SourceRun(source_type=source_type, status=status, run_metadata={})


@pytest.mark.asyncio
async def test_list_source_runs_route(client_a, db_session):
    run = _run()
    db_session.add(run)
    await db_session.commit()

    response = await client_a.get("/api/v1/operations/source-runs")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == str(run.id)


@pytest.mark.asyncio
async def test_get_source_run_detail_route(client_a, db_session):
    run = _run()
    db_session.add(run)
    await db_session.flush()
    db_session.add(
        RawSourceRecord(
            source_run_id=run.id,
            source_type=SourceType.GOOGLE_PLACES,
            source_id="gp:1",
            raw_payload={},
        )
    )
    await db_session.commit()

    response = await client_a.get(f"/api/v1/operations/source-runs/{run.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["run"]["id"] == str(run.id)
    assert body["record_count"] == 1


@pytest.mark.asyncio
async def test_get_source_run_detail_route_404s_for_unknown_id(client_a):
    response = await client_a.get(f"/api/v1/operations/source-runs/{uuid.uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_source_health_route(client_a, db_session):
    db_session.add(_run())
    await db_session.commit()

    response = await client_a.get("/api/v1/operations/source-health")

    assert response.status_code == 200
    body = response.json()
    assert any(h["source_type"] == "google_places" for h in body)


@pytest.mark.asyncio
async def test_list_stranded_records_route(client_a, db_session):
    run = _run()
    db_session.add(run)
    await db_session.flush()
    record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.GOOGLE_PLACES,
        source_id="gp:stranded",
        raw_payload={},
    )
    db_session.add(record)
    await db_session.commit()

    response = await client_a.get("/api/v1/operations/stranded-records")

    assert response.status_code == 200
    body = response.json()
    assert [r["id"] for r in body] == [str(record.id)]


@pytest.mark.asyncio
async def test_list_audit_log_route_filters(client_a, db_session):
    entry = AuditLog(
        action="draft.approved",
        actor="reviewer-1",
        entity_type="OutreachDraft",
        entity_id=uuid.uuid4(),
    )
    other = AuditLog(
        action="resolution.merged",
        actor="reviewer-2",
        entity_type="ResolutionCandidate",
        entity_id=uuid.uuid4(),
    )
    db_session.add_all([entry, other])
    await db_session.commit()

    response = await client_a.get(
        "/api/v1/operations/audit-log", params={"entity_type": "OutreachDraft"}
    )

    assert response.status_code == 200
    body = response.json()
    assert [e["id"] for e in body] == [str(entry.id)]


@pytest.mark.asyncio
async def test_get_config_route_excludes_secrets(client_a):
    response = await client_a.get("/api/v1/operations/config")

    assert response.status_code == 200
    body = response.json()
    assert "database_url" not in body
    assert "lead_sync_webhook_secret" not in body
    assert "google_places_api_key" not in body
    assert "app_env" in body


@pytest.mark.asyncio
async def test_get_metrics_route(client_a, db_session):
    db_session.add(_run())
    await db_session.commit()

    response = await client_a.get("/api/v1/operations/metrics")

    assert response.status_code == 200
    body = response.json()
    assert "outbox_pending" in body
    assert "total_canonical_institutions" in body


@pytest.mark.asyncio
async def test_get_health_route_reports_healthy(client_a, db_session):
    db_session.add(_run())
    await db_session.commit()

    response = await client_a.get("/api/v1/operations/health")

    assert response.status_code == 200
    body = response.json()
    assert body["database_ok"] is True
    assert body["healthy"] is True


@pytest.mark.asyncio
async def test_get_health_route_reports_unhealthy_for_stuck_run(client_a, db_session):
    stuck = SourceRun(
        source_type=SourceType.GOOGLE_PLACES,
        status=RunStatus.STARTED,
        run_metadata={},
        started_at=datetime.now(UTC) - timedelta(hours=6),
    )
    db_session.add(stuck)
    await db_session.commit()

    response = await client_a.get("/api/v1/operations/health")

    assert response.status_code == 200
    body = response.json()
    assert body["healthy"] is False
    assert body["stuck_run_count"] == 1
