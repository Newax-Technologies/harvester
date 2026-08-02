"""
Suppression, channel eligibility, deletion requests, and retention -- see
docs/ROADMAP.md module 11.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.compliance.channel_eligibility import EligibilityResult, is_channel_eligible
from lead_harvester.models.canonical import CanonicalInstitution, ContactPoint
from lead_harvester.models.compliance import (
    DeletionRequest,
    DeletionRequestStatus,
    DeletionSubjectType,
    SuppressionEntry,
    SuppressionReason,
)
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.source import RawSourceRecord
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


async def fulfill_deletion(
    session: AsyncSession, deletion_request_id: uuid.UUID
) -> DeletionRequest:
    """
    Actually deletes the requested subject. Deliberately a separate call
    from request_deletion -- creating the request never deletes anything
    by itself, so a request sitting PENDING is always safe to review
    before anyone chooses to call this.
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
    else:
        subject = await session.get(ContactPoint, request.subject_id)

    if subject is None:
        raise ResourceNotFoundError(str(request.subject_id))

    await session.delete(subject)
    request.status = DeletionRequestStatus.COMPLETED
    request.fulfilled_at = datetime.now(UTC)
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
