from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.config import Settings
from lead_harvester.models.canonical import ContactPoint
from lead_harvester.models.verification import ContactVerification, VerificationStatus
from .base import EmailVerificationProvider
from .licensed import LicensedEmailVerificationProvider
from .local import LocalHeuristicProvider


def build_default_provider(settings: Settings) -> EmailVerificationProvider:
    """Uses the configured licensed provider if credentials are set, otherwise falls back to local heuristics."""
    if settings.email_verification_api_url and settings.email_verification_api_key:
        return LicensedEmailVerificationProvider(
            api_url=settings.email_verification_api_url,
            api_key=settings.email_verification_api_key,
        )
    return LocalHeuristicProvider()


class EmailVerificationService:
    def __init__(self, provider: EmailVerificationProvider):
        self.provider = provider

    async def verify_pending(self, session: AsyncSession, limit: int = 100) -> int:
        """Verifies up to `limit` email ContactPoints that haven't been verified yet. Returns the count verified."""
        stmt = select(ContactPoint).where(
            ContactPoint.contact_type == "email",
            ContactPoint.verification_status == VerificationStatus.PENDING,
        ).limit(limit)
        contacts = (await session.execute(stmt)).scalars().all()

        for contact in contacts:
            await self.verify_contact(session, contact)

        await session.commit()
        return len(contacts)

    async def verify_contact(self, session: AsyncSession, contact: ContactPoint) -> ContactVerification:
        outcome = await self.provider.verify(contact.contact_value)

        record = ContactVerification(
            contact_point_id=contact.id,
            provider=outcome.provider,
            status=outcome.status,
            is_disposable=outcome.is_disposable,
            is_role_account=outcome.is_role_account,
            mx_found=outcome.mx_found,
            raw_response=outcome.raw_response,
        )
        session.add(record)

        contact.verification_status = outcome.status
        contact.verified_at = datetime.now(timezone.utc)

        return record
