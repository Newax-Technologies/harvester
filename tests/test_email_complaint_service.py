from datetime import UTC, datetime

import pytest
from sqlalchemy import func, select

from lead_harvester.models.compliance import SuppressionEntry, SuppressionReason
from lead_harvester.models.email_complaint import EmailComplaintProjection, EmailComplaintType
from lead_harvester.services.email_complaint_service import record_email_complaint


@pytest.mark.asyncio
async def test_record_email_complaint_creates_one_email_suppression(db_session):
    values = {
        "source_system": "communicator",
        "source_complaint_id": "complaint-001",
        "contact_value": " Recipient@Example.COM ",
        "complaint_type": EmailComplaintType.RECIPIENT_SPAM,
        "provider": "postmark",
        "occurred_at": datetime(2026, 8, 4, tzinfo=UTC),
        "evidence_metadata": {"record_type": "spam_complaint"},
    }

    first = await record_email_complaint(db_session, **values)
    second = await record_email_complaint(db_session, **values)

    assert second.id == first.id
    assert first.normalized_contact_value == "recipient@example.com"

    suppression = await db_session.get(SuppressionEntry, first.suppression_entry_id)
    assert suppression is not None
    assert suppression.channel == "email"
    assert suppression.reason is SuppressionReason.EMAIL_COMPLAINT

    projection_count = await db_session.scalar(
        select(func.count()).select_from(EmailComplaintProjection)
    )
    suppression_count = await db_session.scalar(select(func.count()).select_from(SuppressionEntry))
    assert projection_count == 1
    assert suppression_count == 1
