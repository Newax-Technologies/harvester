from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.qualification import QualificationAssessment, QualificationStatus


class QualificationAgent:
    """
    Simulates an AI Subagent (or wraps a real LLM call) to evaluate a CanonicalInstitution
    against an Ideal Customer Profile (ICP).
    """

    def __init__(self, criteria_version: int = 1):
        self.criteria_version = criteria_version

    async def evaluate_institution(
        self, session: AsyncSession, institution: CanonicalInstitution
    ) -> QualificationAssessment:
        """
        Evaluates the institution and creates a QualificationAssessment.
        In the future, this will build a prompt with the institution's data,
        call an LLM, and parse the JSON response.
        """

        # --- MOCK AI LOGIC ---
        # We will qualify them if they have a website and their name doesn't contain "middle school"
        has_website = bool(institution.website)
        name_lower = institution.canonical_name.lower()
        is_target_demographic = "middle school" not in name_lower and "elementary" not in name_lower

        checklist = {"has_website": has_website, "is_target_demographic": is_target_demographic}

        is_qualified = False
        rationale = ""
        status = QualificationStatus.DISQUALIFIED

        if has_website and is_target_demographic:
            is_qualified = True
            status = QualificationStatus.QUALIFIED
            rationale = "Institution has a valid web presence and fits the target demographic (not elementary/middle school)."
        elif not has_website:
            rationale = "Disqualified: No website found to verify operations."
        else:
            rationale = "Disqualified: Institution appears to be outside of our target demographic."

        # --- END MOCK AI LOGIC ---

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
