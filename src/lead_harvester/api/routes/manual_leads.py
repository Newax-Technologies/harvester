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

from lead_harvester.api.dependencies import (
    User,
    get_current_user,
    get_db_session,
    get_lead_sync_emitter,
)
from lead_harvester.config import settings
from lead_harvester.database import get_session
from lead_harvester.integrations.lead_sync_emitter import LeadSyncEmitter
from lead_harvester.models.canonical import (
    Branch,
    CanonicalInstitution,
    ContactPoint,
    OperatingStatus,
)
from lead_harvester.models.provenance import FieldProvenance
from lead_harvester.models.source import RawSourceRecord, RunStatus, SourceRun, SourceType
from lead_harvester.resolution.normalize import (
    normalize_domain,
    normalize_name,
    normalize_phone,
    normalize_website,
)
from lead_harvester.services.lead_profile_service import refresh_lead_profile
from lead_harvester.services.outbox_service import enqueue_and_attempt_delivery
from lead_harvester.services.person_candidate_service import resolve_person_candidate
from lead_harvester.services.sector_service import classify_institution_sector

router = APIRouter(prefix="/leads", tags=["Manual Lead Entry"])


# ---------------------------------------------------------------------------
# Request schema
# ---------------------------------------------------------------------------


class ContactEntry(BaseModel):
    contact_type: str = Field(..., description="phone | email | whatsapp | linkedin | other")
    contact_value: str = Field(..., min_length=1)
    person_name: str | None = None
    role: str | None = None

    @field_validator("contact_type")
    @classmethod
    def _normalize_contact_type(cls, value: str) -> str:
        # Every downstream exact-match comparison (this route's own
        # first_phone/phone-normalization lookups by contact_type == "phone",
        # LeadSyncEmitter.SUPPORTED_CONTACT_TYPES) expects the exact lowercase
        # form -- a caller sending "Phone" or " phone " would otherwise pass
        # this unconstrained field but silently fail every one of those
        # comparisons, leaving the contact unnormalized and dropped from sync.
        return value.strip().lower()


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
    # Routed through the durable outbox (services/outbox_service.py) rather
    # than calling the emitter directly, so a delivery failure becomes a
    # PENDING row that gets retried instead of a lost event. enqueue_and_
    # attempt_delivery/the emitter itself never raise on delivery failure,
    # but this endpoint's contract ("a webhook problem never fails a lead
    # submission") shouldn't depend on trusting that implementation detail
    # -- belt and suspenders. Scheduled as a background task (runs after the
    # response is sent) so a slow or unavailable downstream never delays the
    # caller's own response. institution/branch/contact_points come from the
    # now-closed request session -- expire_on_commit=False keeps their
    # already-loaded attributes readable, so a fresh session here is only
    # needed to persist the new EventOutbox row, not to re-read them.
    try:
        async with get_session() as session:
            await enqueue_and_attempt_delivery(
                session, lead_sync_emitter, institution, [branch], contact_points
            )
    except Exception as e:
        print(f"lead_sync outbox enqueue raised unexpectedly for institution {institution.id}: {e}")


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
    current_user: User = Depends(get_current_user),
) -> ManualLeadOut:
    """
    Record a lead discovered manually (cold call, referral, field visit, etc.)
    into the same database pipeline as automated sources. Requires
    authentication (previously this endpoint had none) because writing a
    tenant-scoped CanonicalInstitution/Branch/ContactPoint needs to know
    which tenant the caller belongs to.
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

    # Extract first phone/email for normalized index fields. Normalized with
    # the same helpers used by every other ingestion path (resolution/
    # normalize.py) -- otherwise a manual entry's phone/domain are stored in
    # a different format (e.g. "+92 300 1234567" vs the digits-only form, or
    # "www.example.edu" vs the stripped host), and the resolution blocker's
    # exact-string comparisons can never match them against a later scraped
    # record for the same institution.
    first_phone = next(
        (c.contact_value for c in payload.contacts if c.contact_type == "phone"), None
    )
    domain = normalize_domain(payload.website) if payload.website else None

    # 3. Raw source record
    source_id = f"manual:{uuid.uuid4().hex[:12]}"
    record = RawSourceRecord(
        source_run_id=run.id,
        source_type=SourceType.MANUAL,
        source_id=source_id,
        raw_payload=raw_payload,
        normalized_name=normalize_name(payload.institution_name),
        normalized_phone=(
            normalize_phone(first_phone, default_region=payload.country_code)
            if first_phone
            else None
        ),
        normalized_domain=domain or None,
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
        tenant_id=current_user.tenant_id,
        canonical_name=payload.institution_name.strip(),
        institution_type=payload.institution_type,
        domain=domain,
        website=normalize_website(payload.website) if payload.website else None,
        status=op_status,
        # confidence_score is a 0-100 scale (an API/UI-facing percentage --
        # see verification/confidence.py, canonical/merger.py's own
        # +10-per-source/capped-at-100 convention), NOT a 0-1 fraction.
        # This was previously 0.7 -- effectively the lowest possible score
        # against that scale, the opposite of the "high base confidence"
        # this comment always intended, since a human directly vouching
        # for a lead should outscore a single-source scraped record.
        confidence_score=70.0,
    )
    session.add(institution)
    await session.flush()

    # docs/ROADMAP.md module 16: auto-classify into a Sector from
    # institution_type, same as canonical/merger.py does for scraped/
    # imported institutions.
    await classify_institution_sector(session, institution)

    # Same "branch_membership" FieldProvenance link canonical/merger.py's
    # merge_records() always writes. Without it, find_canonical_for_raw_record
    # can never discover that this raw record already produced a canonical
    # institution -- a later scraped record matching this one as a resolution
    # candidate would create a second, duplicate institution instead of
    # attaching to this one.
    session.add(
        FieldProvenance(
            canonical_id=institution.id,
            raw_record_id=record.id,
            field_name="branch_membership",
            asserted_value=source_id,
            assertion_trust=1.0,
        )
    )

    # 5. Branch (physical location)
    branch = Branch(
        institution_id=institution.id,
        tenant_id=current_user.tenant_id,
        branch_name=payload.institution_name.strip(),
        address=full_address,
        city=payload.city.strip(),
        country_code=payload.country_code,
        # Keyed by source_type with a list of source_ids -- the same shape
        # canonical/merger.py's _provider_ids_for/find_branch_for_raw_record
        # use. A different key ("manual_record_id") or a bare scalar here
        # would mean find_branch_for_raw_record could never locate this
        # branch for a later reviewer decision that targets this manual
        # record, creating an erroneous "Additional Campus" instead of
        # enriching this one.
        provider_ids={SourceType.MANUAL.value: [source_id]},
    )
    session.add(branch)

    # 6. Contact points
    contact_points: list[ContactPoint] = []
    for c in payload.contacts:
        contact_value = c.contact_value.strip()
        if c.contact_type == "phone":
            # canonical/merger.py's own contact-writing path
            # (_add_contact_if_present) always stores record.normalized_phone,
            # not a raw formatted string -- storing an unnormalized value here
            # instead (e.g. "+92 300 111 2222") means its exact-match dedup
            # lookup can never recognize a later scraped record sharing this
            # same phone (normalized to "+923001112222"), creating a
            # duplicate ContactPoint instead of reusing this one.
            contact_value = normalize_phone(contact_value, default_region=payload.country_code)
        candidate = await resolve_person_candidate(session, institution.id, c.person_name)
        cp = ContactPoint(
            institution_id=institution.id,
            tenant_id=current_user.tenant_id,
            contact_type=c.contact_type,
            contact_value=contact_value,
            person_name=c.person_name,
            role=c.role,
            is_publicly_listed=False,  # manually entered = not scraped from public web
            person_candidate_id=candidate.id if candidate else None,
        )
        session.add(cp)
        contact_points.append(cp)

    # 7. Mark run as complete
    run.status = RunStatus.COMPLETED
    run.completed_at = datetime.now(UTC)

    # Marks this institution as having had a sync attempted, so a later
    # resolution-driven update (automated pipeline attach, or a reviewer
    # merge/branch decision) knows to re-emit rather than letting the
    # core-newax mirror silently go stale after this first sync. Gated on
    # the same lead_sync_enabled flag the emitter itself checks -- when
    # sync is disabled, no delivery is ever attempted here, so nothing
    # should claim one was.
    if settings.lead_sync_enabled:
        institution.lead_synced_at = datetime.now(UTC)

    # Gives a manually-entered lead an initial LeadProfile immediately
    # (contactability from the contacts just entered, a baseline score)
    # instead of leaving it profile-less until some later automated pass
    # happens to touch this institution.
    await refresh_lead_profile(session, institution.id)

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
