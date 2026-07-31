from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from lead_harvester.models.canonical import CanonicalInstitution, ContactPoint
from lead_harvester.models.outreach import AccountBrief, OutreachDraft, BriefStatus, DraftStatus

class OutreachGenerator:
    """
    Simulates the AI generation of Account Briefs and Outreach Drafts.
    """

    async def generate_brief(self, session: AsyncSession, institution: CanonicalInstitution) -> AccountBrief:
        """
        Synthesizes research into an Account Brief.
        """

        # MOCK AI GENERATION
        hypotheses = [
            f"{institution.canonical_name} likely struggles with manual lead tracking.",
            "Their current toolset is likely fragmented across multiple campuses."
        ]

        # Rank stakeholders from any known ContactPoints with a role first, since a
        # real name/role beats a generic guess; fall back to generic titles otherwise.
        known_contacts_stmt = select(ContactPoint).where(
            ContactPoint.institution_id == institution.id,
            ContactPoint.role.is_not(None)
        )
        known_contacts = (await session.execute(known_contacts_stmt)).scalars().all()

        if known_contacts:
            stakeholders = [
                {"role": c.role, "name": c.person_name or "Unknown", "score": 90 if idx == 0 else 75}
                for idx, c in enumerate(known_contacts)
            ]
        else:
            stakeholders = [
                {"role": "Principal", "name": "Unknown", "score": 90},
                {"role": "IT Director", "name": "Unknown", "score": 75}
            ]

        summary = f"{institution.canonical_name} is a strong candidate for outreach based on our qualification rules."

        brief = AccountBrief(
            institution_id=institution.id,
            status=BriefStatus.READY_FOR_REVIEW,
            value_hypotheses=hypotheses,
            stakeholder_ranking=stakeholders,
            executive_summary=summary
        )

        session.add(brief)
        return brief

    async def generate_draft(self, session: AsyncSession, brief: AccountBrief, target_role: str) -> OutreachDraft:
        """
        Drafts a specific message for a stakeholder.
        """

        stakeholder = next(
            (s for s in (brief.stakeholder_ranking or []) if s.get("role") == target_role),
            None
        )

        contacts_stmt = select(ContactPoint).where(ContactPoint.institution_id == brief.institution_id)
        contact_points = (await session.execute(contacts_stmt)).scalars().all()

        # Prefer a contact matching the target role with an email, then any email,
        # then any contact at all.
        contact = next((c for c in contact_points if c.role == target_role and c.contact_type == "email"), None)
        if contact is None:
            contact = next((c for c in contact_points if c.contact_type == "email"), None)
        if contact is None and contact_points:
            contact = contact_points[0]

        target_name = (stakeholder.get("name") if stakeholder else None) or (contact.person_name if contact else None) or "Unknown"
        target_contact_value = contact.contact_value if contact else ""

        # MOCK AI GENERATION
        subject = f"Streamlining operations at {brief.institution.canonical_name}"
        body = f"Hi,\n\nI noticed {brief.institution.canonical_name} might be looking for ways to improve efficiency. I'd love to chat.\n\nBest,\nSales"

        draft = OutreachDraft(
            brief_id=brief.id,
            status=DraftStatus.PENDING_GENERATION,
            target_name=target_name,
            target_role=target_role,
            target_contact_value=target_contact_value,
            subject_line=subject,
            body=body
        )

        session.add(draft)

        # Without a real contact address there's nothing to send to, so leave it
        # for a human to fill in rather than marking it ready to go out.
        draft.status = DraftStatus.GENERATED if target_contact_value else DraftStatus.NEEDS_REVISION

        return draft
