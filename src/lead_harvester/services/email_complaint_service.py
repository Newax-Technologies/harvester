from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.models.compliance import SuppressionReason
from lead_harvester.models.email_complaint import EmailComplaintProjection, EmailComplaintType
from lead_harvester.services.compliance_service import add_suppression, normalize_contact_value


async def record_email_complaint(
    session: AsyncSession,
    *,
    source_system: str,
    source_complaint_id: str,
    contact_value: str,
    complaint_type: EmailComplaintType,
    provider: str,
    occurred_at: datetime,
    provider_message_id: str = "",
    evidence_metadata: dict | None = None,
) -> EmailComplaintProjection:
    """Record one source complaint and create one email-scoped suppression.

    Source retries return the existing projection, so they cannot manufacture
    duplicate suppressions.
    """

    existing = await session.scalar(
        select(EmailComplaintProjection).where(
            EmailComplaintProjection.source_system == source_system,
            EmailComplaintProjection.source_complaint_id == source_complaint_id,
        )
    )
    if existing is not None:
        return existing

    normalized_contact = normalize_contact_value(contact_value)
    suppression = await add_suppression(
        session,
        normalized_contact,
        SuppressionReason.EMAIL_COMPLAINT,
        channel="email",
        note=f"{complaint_type.value} reported by {provider}",
        suppressed_by=source_system,
    )
    projection = EmailComplaintProjection(
        source_system=source_system,
        source_complaint_id=source_complaint_id,
        normalized_contact_value=normalized_contact,
        complaint_type=complaint_type,
        provider=provider,
        provider_message_id=provider_message_id,
        evidence_metadata=evidence_metadata or {},
        suppression_entry_id=suppression.id,
        occurred_at=occurred_at,
    )
    session.add(projection)
    await session.flush()
    return projection
