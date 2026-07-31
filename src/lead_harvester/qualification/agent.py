from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.canonical import CanonicalInstitution, ContactPoint, OperatingStatus
from lead_harvester.models.qualification import QualificationAssessment, QualificationStatus


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
    """

    def __init__(self, criteria_version: int = 2):
        self.criteria_version = criteria_version

    async def evaluate_institution(
        self, session: AsyncSession, institution: CanonicalInstitution
    ) -> QualificationAssessment:
        """
        Queried explicitly rather than via institution.contact_points --
        touching an unloaded relationship attribute on an AsyncSession
        raises MissingGreenlet if `institution` came from the session's
        identity map instead of this call's own query (see
        services/lead_profile_service.py::refresh_lead_profile's own
        comment on the same issue).
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

        checklist = {
            "is_reachable": is_reachable,
            "is_active": is_active,
            "has_website": has_website,
        }

        if not is_reachable:
            status = QualificationStatus.DISQUALIFIED
            rationale = "Disqualified: no contact information on file to reach this lead."
        elif not is_active:
            status = QualificationStatus.DISQUALIFIED
            rationale = "Disqualified: institution is permanently closed."
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
