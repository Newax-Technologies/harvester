from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.canonical import (
    Branch,
    CanonicalInstitution,
    ContactPoint,
    OperatingStatus,
)
from lead_harvester.models.qualification import QualificationAssessment, QualificationStatus
from lead_harvester.models.sector import Sector


class QualificationAgent:
    """
    Evaluates whether a CanonicalInstitution is a viable lead for NEWAX's
    business-infrastructure offering (websites, LMS/operational software,
    IoT hardware+software integration) -- see docs/ROADMAP.md module 20.

    Qualification here is a reachability/viability gate ("can we actually
    engage this lead at all"), deliberately separate from opportunity
    ranking ("how much of what we sell do they not already have") -- the
    latter belongs in profiles/scoring.py's score, not this pass/fail
    verdict. Earlier logic conflated the two, requiring a website to
    qualify at all -- backwards for a business that sells websites, since
    a lead having one makes them a WEAKER website-sale opportunity, not a
    disqualifying trait. It also disqualified anything with "elementary"
    or "middle school" in its name, an arbitrary rule with no basis in
    this business's actual targeting criteria.

    docs/ROADMAP.md module 17 layers one further, genuinely per-sector
    check on top of that base gate: institution.sector.qualification_rules
    (`disqualifying_name_keywords`, `min_branch_count`) for sector-specific
    disqualifiers that actually make sense (e.g. a franchise-only real-
    estate sector excluding solo agents) -- evaluated IN ADDITION to the
    base reachability/viability gate above, never in place of it. An
    institution with no sector, or a sector with empty qualification_rules
    (every seeded sector starts this way), skips this layer entirely.
    """

    def __init__(self, criteria_version: int = 3):
        self.criteria_version = criteria_version

    async def evaluate_institution(
        self, session: AsyncSession, institution: CanonicalInstitution
    ) -> QualificationAssessment:
        """
        Queried explicitly rather than via institution.contact_points/
        .branches -- touching an unloaded relationship attribute on an
        AsyncSession raises MissingGreenlet if `institution` came from the
        session's identity map instead of this call's own query (see
        services/lead_profile_service.py::refresh_lead_profile's own
        comment on the same issue). institution.sector_id is a plain
        scalar column, not a relationship, so reading it directly is safe.
        """
        contact_points = list(
            (
                await session.scalars(
                    select(ContactPoint).where(ContactPoint.institution_id == institution.id)
                )
            ).all()
        )
        is_reachable = len(contact_points) > 0
        is_active = institution.status != OperatingStatus.CLOSED_PERMANENTLY
        has_website = bool(institution.website)

        sector = await session.get(Sector, institution.sector_id) if institution.sector_id else None
        qualification_rules = sector.qualification_rules if sector is not None else {}
        disqualifying_keywords = qualification_rules.get("disqualifying_name_keywords") or []
        sector_min_branch_count = qualification_rules.get("min_branch_count", 0)

        name_lower = institution.canonical_name.lower()
        matched_keyword = next(
            (kw for kw in disqualifying_keywords if kw.lower() in name_lower), None
        )

        branch_count = await session.scalar(
            select(func.count()).select_from(Branch).where(Branch.institution_id == institution.id)
        )

        checklist = {
            "is_reachable": is_reachable,
            "is_active": is_active,
            "has_website": has_website,
            "sector_code": sector.code if sector is not None else None,
            "matched_disqualifying_keyword": matched_keyword,
            "branch_count": branch_count,
        }

        if not is_reachable:
            status = QualificationStatus.DISQUALIFIED
            rationale = "Disqualified: no contact information on file to reach this lead."
        elif not is_active:
            status = QualificationStatus.DISQUALIFIED
            rationale = "Disqualified: institution is permanently closed."
        elif matched_keyword is not None:
            status = QualificationStatus.DISQUALIFIED
            rationale = (
                f"Disqualified: name matches the {sector.code!r} sector's disqualifying "
                f"keyword {matched_keyword!r}."
            )
        elif sector_min_branch_count > 0 and branch_count < sector_min_branch_count:
            status = QualificationStatus.DISQUALIFIED
            rationale = (
                f"Disqualified: below the {sector.code!r} sector's minimum branch count "
                f"({branch_count} < {sector_min_branch_count})."
            )
        else:
            status = QualificationStatus.QUALIFIED
            opportunity_note = (
                "already has a website -- lower website-sale opportunity"
                if has_website
                else "no website on file -- website-sale opportunity"
            )
            rationale = f"Qualified: reachable and operating ({opportunity_note})."

        is_qualified = status == QualificationStatus.QUALIFIED

        assessment = QualificationAssessment(
            institution_id=institution.id,
            criteria_version=self.criteria_version,
            status=status,
            is_qualified=is_qualified,
            rationale=rationale,
            criteria_checklist=checklist,
        )

        session.add(assessment)
        return assessment
