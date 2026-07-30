"""
CSV/JSON lead export -- see docs/ROADMAP.md module 13's export piece.

One row per ContactPoint (the actual contactable unit a downstream
consumer would act on), carrying its owning institution's identity/score
fields and a summary of that institution's branches. ContactPoint has no
direct link to a specific Branch (models/canonical.py: contacts are
institution-wide, not branch-scoped), so branch info is summarized
per-institution rather than joined per-row.

Reuses LeadProfile for score/qualification fields instead of recomputing
them -- see models/profile.py's own docstring: "downstream consumers
(ranking, review UIs, exports) never need to re-derive
score/contactability/qualification from scratch".

Suppressed contacts (services/compliance_service.py) are still included --
an export is a data extract, not an outreach action -- but every row
carries is_suppressed so a downstream consumer can't accidentally treat a
suppressed contact as safe to message without a signal to check first.
"""

from __future__ import annotations

import csv
import io
import json
from dataclasses import asdict, dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from lead_harvester.models.canonical import CanonicalInstitution, OperatingStatus
from lead_harvester.models.profile import LeadProfile
from lead_harvester.models.qualification import QualificationStatus
from lead_harvester.services.compliance_service import find_applicable_suppression


@dataclass
class LeadExportRow:
    institution_id: str
    institution_name: str
    institution_type: str
    domain: str
    website: str
    operating_status: str
    confidence_score: float
    overall_score: int | None
    qualification_status: str | None
    branch_count: int
    primary_city: str
    primary_country_code: str
    contact_id: str
    contact_type: str
    contact_value: str
    person_name: str
    role: str
    is_publicly_listed: bool
    is_suppressed: bool


async def build_lead_export_rows(
    session: AsyncSession,
    *,
    status: OperatingStatus | None = None,
    min_score: int | None = None,
    qualification_status: QualificationStatus | None = None,
    limit: int = 1000,
) -> list[LeadExportRow]:
    """
    Builds one export row per ContactPoint across institutions matching
    the given filters, highest-confidence institution first. min_score/
    qualification_status filter against LeadProfile -- an institution with
    no LeadProfile yet (never scored) is excluded by either filter, since
    neither can be evaluated without one.
    """
    stmt = (
        select(CanonicalInstitution)
        .options(
            selectinload(CanonicalInstitution.branches),
            selectinload(CanonicalInstitution.contact_points),
        )
        .order_by(CanonicalInstitution.confidence_score.desc(), CanonicalInstitution.id.asc())
        .limit(limit)
    )
    if status is not None:
        stmt = stmt.where(CanonicalInstitution.status == status)
    if min_score is not None or qualification_status is not None:
        eligible_institutions = select(LeadProfile.institution_id)
        if min_score is not None:
            eligible_institutions = eligible_institutions.where(
                LeadProfile.overall_score >= min_score
            )
        if qualification_status is not None:
            eligible_institutions = eligible_institutions.where(
                LeadProfile.qualification_status == qualification_status
            )
        stmt = stmt.where(CanonicalInstitution.id.in_(eligible_institutions))

    institutions = list((await session.scalars(stmt)).unique())
    if not institutions:
        return []

    profile_by_institution = {
        p.institution_id: p
        for p in await session.scalars(
            select(LeadProfile).where(
                LeadProfile.institution_id.in_([inst.id for inst in institutions])
            )
        )
    }

    rows: list[LeadExportRow] = []
    for institution in institutions:
        profile = profile_by_institution.get(institution.id)
        branches = institution.branches
        primary_city = branches[0].city if branches else ""
        primary_country_code = branches[0].country_code if branches else ""

        for contact in institution.contact_points:
            suppression = await find_applicable_suppression(
                session, contact.contact_value, channel=contact.contact_type
            )
            rows.append(
                LeadExportRow(
                    institution_id=str(institution.id),
                    institution_name=institution.canonical_name,
                    institution_type=institution.institution_type,
                    domain=institution.domain or "",
                    website=institution.website or "",
                    operating_status=institution.status.value,
                    confidence_score=institution.confidence_score,
                    overall_score=profile.overall_score if profile else None,
                    qualification_status=(
                        profile.qualification_status.value
                        if profile is not None and profile.qualification_status is not None
                        else None
                    ),
                    branch_count=len(branches),
                    primary_city=primary_city,
                    primary_country_code=primary_country_code,
                    contact_id=str(contact.id),
                    contact_type=contact.contact_type,
                    contact_value=contact.contact_value,
                    person_name=contact.person_name or "",
                    role=contact.role or "",
                    is_publicly_listed=contact.is_publicly_listed,
                    is_suppressed=suppression is not None,
                )
            )
    return rows


def rows_to_csv(rows: list[LeadExportRow]) -> str:
    buffer = io.StringIO()
    fieldnames = [f for f in LeadExportRow.__dataclass_fields__]
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(asdict(row))
    return buffer.getvalue()


def rows_to_json(rows: list[LeadExportRow]) -> str:
    return json.dumps([asdict(row) for row in rows], separators=(",", ":"))
