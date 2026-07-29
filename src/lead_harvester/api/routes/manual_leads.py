"""
Manual Lead Entry API Route
===========================
POST /api/v1/leads/manual

Accepts a manually entered lead and writes it to the database as:
  1. A SourceRun  (source_type = MANUAL)
  2. A RawSourceRecord (the raw form data)
  3. A CanonicalInstitution + Branch + ContactPoints (the resolved entity)

This means manual leads go through the exact same data model as
scraped leads and appear in the same dashboard/pipeline.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import get_db_session, get_lead_sync_emitter
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.models.canonical import (
    Branch,
    CanonicalInstitution,
    ContactPoint,
    OperatingStatus,
)
from lead_harvester.models.source import RawSourceRecord, RunStatus, SourceRun, SourceType

router = APIRouter(prefix="/leads", tags=["Manual Lead Entry"])


# ---------------------------------------------------------------------------
# Request schema
# ---------------------------------------------------------------------------


class ContactEntry(BaseModel):
    contact_type: str = Field(..., description="phone | email | whatsapp | linkedin | other")
    contact_value: str = Field(..., min_length=1)
    person_name: str | None = None
    role: str | None = None


class ManualLeadIn(BaseModel):
    # Institution
    institution_name: str = Field(..., min_length=2, max_length=255)
    institution_type: str = Field(
        default="school",
        max_length=100,
        description="school | college | university | clinic | other",
    )
    website: str | None = Field(default=None, max_length=500)
    operating_status: str = Field(default="operational")

    # Location
    address: str = Field(default="", max_length=1000)
    city: str = Field(..., min_length=1, max_length=100)
    country: str = Field(default="Pakistan", max_length=100)
    country_code: str = Field(
        ..., min_length=2, max_length=2, description="ISO 3166-1 alpha-2, e.g. 'PK'"
    )

    @field_validator("country_code")
    @classmethod
    def _uppercase_country_code(cls, value: str) -> str:
        upper = value.upper()
        # .upper() can expand a single character (e.g. "ß" -> "SS"), so
        # re-check the length *after* uppercasing rather than trusting the
        # field's raw min/max_length=2 constraint on the original value.
        if len(upper) != 2 or not upper.isascii() or not upper.isalpha():
            raise ValueError("country_code must be exactly two ASCII letters (ISO 3166-1 alpha-2).")
        return upper

    @field_validator("city")
    @classmethod
    def _require_non_blank_city(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("city must not be blank.")
        return stripped

    # Contacts (at least one required)
    contacts: list[ContactEntry] = Field(..., min_length=1)

    # Notes
    notes: str | None = Field(default=None, max_length=2000)
    lead_source_note: str | None = Field(
        default=None,
        max_length=500,
        description="Where did you find this lead? e.g. 'Cold call', 'Referral from X'",
    )


class ManualLeadOut(BaseModel):
    id: str
    institution_name: str
    contacts_saved: int
    message: str


# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------


async def _deliver_lead_sync_event(
    lead_sync_emitter: LeadSyncEmitter,
    institution: CanonicalInstitution,
    branch: Branch,
    contact_points: list[ContactPoint],
) -> None:
    # The emitter itself never raises on delivery failure, but this endpoint's
    # contract ("a webhook problem never fails a lead submission") shouldn't
    # depend on trusting that implementation detail -- belt and suspenders.
    # Scheduled as a background task (runs after the response is sent) so a
    # slow or unavailable downstream never delays the caller's own response,
    # matching the emitter's fire-and-forget contract.
    try:
        await lead_sync_emitter.emit_institution_upserted(institution, [branch], contact_points)
    except Exception as e:
        print(f"lead_sync emitter raised unexpectedly for institution {institution.id}: {e}")


@router.post(
    "/manual",
    response_model=ManualLeadOut,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a manually entered lead",
)
async def create_manual_lead(
    payload: ManualLeadIn,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db_session),
    lead_sync_emitter: LeadSyncEmitter = Depends(get_lead_sync_emitter),
) -> ManualLeadOut:
    """
    Record a lead discovered manually (cold call, referral, field visit, etc.)
    into the same database pipeline as automated sources.
    """
    # 1. Create a SourceRun for this manual entry
    run = SourceRun(
        source_type=SourceType.MANUAL,
        run_metadata={
            "entry_method": "manual_form",
            "lead_source_note": payload.lead_source_note or "",
            "notes": payload.notes or "",
        },
        status=RunStatus.STARTED,
    )
    session.add(run)
    await session.flush()

    # 2. Build the raw payload (mirrors what scrapers produce)
    raw_payload: dict[str, Any] = {
        "institution_name": payload.institution_name,
        "institution_type": payload.institution_type,
        "website": payload.website,
        "address": payload.address,
        "city": payload.city,
        "country": payload.country,
        "country_code": payload.country_code,
        "operating_status": payload.operating_status,
        "contacts": [c.model_dump() for c in payload.contacts],
        "notes": payload.notes,
        "lead_source_note": payload.lead_source_note,
        "submitted_at": datetime.now(UTC).isoformat(),
    }

    # Extract first phone/email for normalized index fields
    first_phone = next(
        (c.contact_value for c in payload.contacts if c.contact_type == "phone"), None
    )
    domain = None
    if payload.website:
        from urllib.parse import urlparse

        parsed = urlparse(
            payload.website if payload.website.startswith("http") else f"https://{payload.website}"
        )
        domain = parsed.netloc or None

    # 3. Raw source record
    source_id = f"manual:{uuid.uuid4().hex[:12]}"
    record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.MANUAL,
        source_id=source_id,
        raw_payload=raw_payload,
        normalized_name=payload.institution_name.strip().lower(),
        normalized_phone=first_phone,
        normalized_domain=domain,
        location=None,
    )
    session.add(record)

    # 4. Canonical institution
    try:
        op_status = OperatingStatus(payload.operating_status)
    except ValueError:
        op_status = OperatingStatus.UNKNOWN

    full_address = ", ".join(filter(None, [payload.address, payload.city, payload.country]))

    institution = CanonicalInstitution(
        canonical_name=payload.institution_name.strip(),
        institution_type=payload.institution_type,
        domain=domain,
        website=payload.website,
        status=op_status,
        confidence_score=0.7,  # Manual entries get a high base confidence
    )
    session.add(institution)
    await session.flush()

    # 5. Branch (physical location)
    branch = Branch(
        institution_id=institution.id,
        branch_name=payload.institution_name.strip(),
        address=full_address,
        city=payload.city.strip(),
        country_code=payload.country_code,
        provider_ids={"manual_record_id": source_id},
    )
    session.add(branch)

    # 6. Contact points
    contact_points: list[ContactPoint] = []
    for c in payload.contacts:
        cp = ContactPoint(
            institution_id=institution.id,
            contact_type=c.contact_type,
            contact_value=c.contact_value.strip(),
            person_name=c.person_name,
            role=c.role,
            is_publicly_listed=False,  # manually entered = not scraped from public web
        )
        session.add(cp)
        contact_points.append(cp)

    # 7. Mark run as complete
    run.status = RunStatus.COMPLETED
    run.completed_at = datetime.now(UTC)

    # Commit explicitly here (rather than relying solely on get_db_session's
    # own commit-on-teardown) so the background task below is only ever
    # scheduled once these rows are guaranteed durable.
    await session.commit()

    background_tasks.add_task(
        _deliver_lead_sync_event, lead_sync_emitter, institution, branch, contact_points
    )

    return ManualLeadOut(
        id=str(institution.id),
        institution_name=institution.canonical_name,
        contacts_saved=len(payload.contacts),
        message=f"Lead '{institution.canonical_name}' saved successfully with {len(payload.contacts)} contact(s).",
    )
