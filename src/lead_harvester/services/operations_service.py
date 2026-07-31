"""
Operations and Administration (see docs/ROADMAP.md module 15) -- job
visibility, source health, the failure queue, a safe read-only config
view, the audit trail, aggregated metrics, and a real health check.

No new tables: every piece here reads/aggregates data already written by
other modules (SourceRun/RawSourceRecord, AuditLog, EventOutbox,
DataQualityFlag, SuppressionEntry) rather than introducing a parallel
tracking scheme this codebase would have to keep in sync by hand.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.config import Settings
from lead_harvester.config import settings as app_settings
from lead_harvester.models.audit import AuditLog
from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.compliance import SuppressionEntry
from lead_harvester.models.outbox import EventOutbox, OutboxStatus
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.resolution import ResolutionCandidate
from lead_harvester.models.sector import Sector
from lead_harvester.models.source import (
    RawPageSnapshot,
    RawSourceRecord,
    RunStatus,
    SourceRun,
    SourceType,
)
from lead_harvester.models.verification import DataQualityFlag, FlagStatus
from lead_harvester.services.dashboard_service import DashboardService

# A SourceRun stuck in STARTED longer than this is almost certainly a
# crashed/killed worker process, not slow progress -- a healthy run always
# eventually reaches COMPLETED or FAILED. Surfaced by check_health as a
# signal for a human to investigate, never auto-resolved (this codebase
# has no way to know whether the underlying job is safe to re-run).
STUCK_RUN_THRESHOLD_HOURS = 2.0

# Explicit allowlist, not a blocklist, for get_sanitized_config -- a new
# Settings field defaults to NOT exposed until someone deliberately adds
# it here, so a future secret (an API key, a webhook secret, a
# credentialed database URL) can never leak through this endpoint just
# because nobody remembered to exclude it.
_SAFE_CONFIG_FIELDS = (
    "app_env",
    "allow_demo_seed",
    "lead_sync_enabled",
    "lead_sync_webhook_timeout_seconds",
    "lead_sync_default_country_code",
    "daily_selection_default_limit",
    "daily_selection_reservation_ttl_hours",
    "daily_selection_min_score",
    "user_agent",
    "request_timeout_seconds",
    "concurrency",
    "delay_seconds",
    "max_pages_per_domain",
    "max_depth",
)


async def list_source_runs(
    session: AsyncSession,
    *,
    source_type: SourceType | None = None,
    status: RunStatus | None = None,
    limit: int = 100,
) -> list[SourceRun]:
    stmt = select(SourceRun).order_by(SourceRun.started_at.desc()).limit(limit)
    if source_type is not None:
        stmt = stmt.where(SourceRun.source_type == source_type)
    if status is not None:
        stmt = stmt.where(SourceRun.status == status)
    return list(await session.scalars(stmt))


async def get_source_run_detail(session: AsyncSession, run_id: uuid.UUID) -> dict[str, Any]:
    run = await session.get(SourceRun, run_id)
    if run is None:
        raise ResourceNotFoundError(str(run_id))
    record_count = await session.scalar(
        select(func.count(RawSourceRecord.id)).where(RawSourceRecord.source_run_id == run.id)
    )
    return {
        "run": run,
        "record_count": record_count or 0,
        "unresolved_records": run.run_metadata.get("unresolved_records", []),
    }


async def list_page_snapshots(
    session: AsyncSession,
    *,
    source_run_id: uuid.UUID | None = None,
    only_errors: bool = False,
    limit: int = 100,
) -> list[RawPageSnapshot]:
    """
    Read visibility into docs/ROADMAP.md module 3's raw_snapshot data
    (models/source.py::RawPageSnapshot) -- every page a WEBSITE crawl
    attempted, success or failure. only_errors filters to fetch_error != ""
    (robots-disallowed, non-HTML, oversized, HTTP errors, decode
    failures), for auditing why a domain yielded fewer leads than expected
    without paging through every successful fetch too.
    """
    stmt = select(RawPageSnapshot).order_by(RawPageSnapshot.fetched_at.desc()).limit(limit)
    if source_run_id is not None:
        stmt = stmt.where(RawPageSnapshot.source_run_id == source_run_id)
    if only_errors:
        stmt = stmt.where(RawPageSnapshot.fetch_error != "")
    return list(await session.scalars(stmt))


async def compute_source_health(session: AsyncSession) -> list[dict[str, Any]]:
    """
    Per-SourceType health, for every SourceType that has ever run at
    least once: when it last ran, whether that run succeeded, when it
    last SUCCEEDED (which may be an earlier run than the most recent one,
    if recent runs have been failing), and how many of its runs failed in
    the last 7 days.
    """
    week_ago = datetime.now(UTC) - timedelta(days=7)
    results = []
    for source_type in SourceType:
        latest = await session.scalar(
            select(SourceRun)
            .where(SourceRun.source_type == source_type)
            .order_by(SourceRun.started_at.desc())
            .limit(1)
        )
        if latest is None:
            continue
        last_success = await session.scalar(
            select(SourceRun)
            .where(SourceRun.source_type == source_type)
            .where(SourceRun.status == RunStatus.COMPLETED)
            .order_by(SourceRun.started_at.desc())
            .limit(1)
        )
        failed_last_7d = await session.scalar(
            select(func.count(SourceRun.id))
            .where(SourceRun.source_type == source_type)
            .where(SourceRun.status == RunStatus.FAILED)
            .where(SourceRun.started_at >= week_ago)
        )
        results.append(
            {
                "source_type": source_type.value,
                "last_run_at": latest.started_at,
                "last_run_status": latest.status.value,
                "last_successful_run_at": last_success.started_at if last_success else None,
                "failed_run_count_last_7d": failed_last_7d or 0,
            }
        )
    return results


async def list_stranded_records(
    session: AsyncSession, *, limit: int = 100
) -> list[RawSourceRecord]:
    """
    Read-only visibility into exactly the same "stranded" set
    pipeline.py::LeadPipeline._retry_stranded_records already self-heals
    at the start of every pipeline run -- reuses its own eligibility list
    and definition (a resolution-eligible source type, not yet
    canonicalized, not already sitting in the pending human-review queue)
    rather than restating it, so this can never silently drift out of
    sync with what actually gets auto-retried.
    """
    from lead_harvester.pipeline import LeadPipeline

    canonicalized = select(FieldProvenance.raw_record_id)
    pending_review = select(ResolutionCandidate.raw_record_id).where(
        ResolutionCandidate.review_outcome.is_(None)
    )
    stmt = (
        select(RawSourceRecord)
        .where(RawSourceRecord.source_type.in_(LeadPipeline._RESOLUTION_ELIGIBLE_SOURCE_TYPES))
        .where(RawSourceRecord.id.not_in(canonicalized))
        .where(RawSourceRecord.id.not_in(pending_review))
        .order_by(RawSourceRecord.extracted_at.desc())
        .limit(limit)
    )
    return list(await session.scalars(stmt))


async def list_audit_log(
    session: AsyncSession,
    *,
    entity_type: str | None = None,
    entity_id: uuid.UUID | None = None,
    actor: str | None = None,
    limit: int = 100,
) -> list[AuditLog]:
    stmt = select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit)
    if entity_type is not None:
        stmt = stmt.where(AuditLog.entity_type == entity_type)
    if entity_id is not None:
        stmt = stmt.where(AuditLog.entity_id == entity_id)
    if actor is not None:
        stmt = stmt.where(AuditLog.actor == actor)
    return list(await session.scalars(stmt))


def get_sanitized_config(settings: Settings | None = None) -> dict[str, Any]:
    settings = settings if settings is not None else app_settings
    return {field: getattr(settings, field) for field in _SAFE_CONFIG_FIELDS}


async def compute_operational_metrics(session: AsyncSession) -> dict[str, Any]:
    """
    Extends DashboardService.get_summary (reused, not recomputed) with
    counts from the modules that landed after the dashboard was built --
    the outbox's delivery backlog/dead-letters, open data-quality flags,
    and how many contact values are currently suppressed.
    """
    summary = await DashboardService.get_summary(session)
    outbox_pending = await session.scalar(
        select(func.count(EventOutbox.id)).where(EventOutbox.status == OutboxStatus.PENDING)
    )
    outbox_dead_letter = await session.scalar(
        select(func.count(EventOutbox.id)).where(EventOutbox.status == OutboxStatus.DEAD_LETTER)
    )
    open_flags = await session.scalar(
        select(func.count(DataQualityFlag.id)).where(DataQualityFlag.status == FlagStatus.OPEN)
    )
    suppressed_contacts = await session.scalar(select(func.count(SuppressionEntry.id)))

    sector_breakdown_rows = await session.execute(
        select(Sector.code, func.count(CanonicalInstitution.id))
        .join(CanonicalInstitution, CanonicalInstitution.sector_id == Sector.id)
        .group_by(Sector.code)
    )
    institutions_by_sector = dict(sector_breakdown_rows.all())
    unclassified_count = await session.scalar(
        select(func.count(CanonicalInstitution.id)).where(CanonicalInstitution.sector_id.is_(None))
    )
    institutions_by_sector["unclassified"] = unclassified_count or 0

    return {
        **summary,
        "outbox_pending": outbox_pending or 0,
        "outbox_dead_letter": outbox_dead_letter or 0,
        "open_data_quality_flags": open_flags or 0,
        "suppressed_contacts": suppressed_contacts or 0,
        "institutions_by_sector": institutions_by_sector,
    }


async def check_health(session: AsyncSession) -> dict[str, Any]:
    """
    A real check, not just "the process is up": confirms the database is
    actually reachable right now (a hung/exhausted connection pool would
    otherwise still report healthy up until the first real query hits it),
    and surfaces SourceRuns stuck in STARTED past
    STUCK_RUN_THRESHOLD_HOURS as an operational signal worth a human's
    attention.
    """
    try:
        await session.execute(select(1))
        db_ok = True
    except Exception:
        db_ok = False

    stuck_runs: list[SourceRun] = []
    if db_ok:
        stuck_threshold = datetime.now(UTC) - timedelta(hours=STUCK_RUN_THRESHOLD_HOURS)
        stuck_runs = list(
            await session.scalars(
                select(SourceRun)
                .where(SourceRun.status == RunStatus.STARTED)
                .where(SourceRun.started_at < stuck_threshold)
                .order_by(SourceRun.started_at.asc())
            )
        )

    return {
        "database_ok": db_ok,
        "stuck_run_count": len(stuck_runs),
        "stuck_run_ids": [str(r.id) for r in stuck_runs],
        "healthy": db_ok and not stuck_runs,
    }
