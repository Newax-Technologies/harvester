from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.canonical import CanonicalInstitution
from lead_harvester.models.outreach import AccountBrief, BriefStatus, DraftStatus, OutreachDraft


class OutreachGenerator:
    """
    Simulates the AI generation of Account Briefs and Outreach Drafts.
    """

    async def generate_brief(
        self, session: AsyncSession, institution: CanonicalInstitution
    ) -> AccountBrief:
        """
        Synthesizes research into an Account Brief.
        """

        # MOCK AI GENERATION
        hypotheses = [
            f"{institution.canonical_name} likely struggles with manual lead tracking.",
            "Their current toolset is likely fragmented across multiple campuses.",
        ]

        stakeholders = [
            {"role": "Principal", "name": "Unknown", "score": 90},
            {"role": "IT Director", "name": "Unknown", "score": 75},
        ]

        summary = f"{institution.canonical_name} is a strong candidate for outreach based on our qualification rules."

        brief = AccountBrief(
            institution_id=institution.id,
            status=BriefStatus.READY_FOR_REVIEW,
            value_hypotheses=hypotheses,
            stakeholder_ranking=stakeholders,
            executive_summary=summary,
        )

        session.add(brief)
        return brief

    async def generate_draft(
        self, session: AsyncSession, brief: AccountBrief, target_role: str
    ) -> OutreachDraft:
        """
        Drafts a specific message for a stakeholder.
        """

        # MOCK AI GENERATION
        subject = f"Streamlining operations at {brief.institution.canonical_name}"
        body = f"Hi,\n\nI noticed {brief.institution.canonical_name} might be looking for ways to improve efficiency. I'd love to chat.\n\nBest,\nSales"

        draft = OutreachDraft(
            brief_id=brief.id,
            status=DraftStatus.PENDING_GENERATION,
            target_name="Unknown",
            target_role=target_role,
            target_contact_value="placeholder@example.com",
            subject_line=subject,
            body=body,
        )

        session.add(draft)

        # In reality, this would be queued for review before moving to GENERATED
        draft.status = DraftStatus.GENERATED

        return draft
