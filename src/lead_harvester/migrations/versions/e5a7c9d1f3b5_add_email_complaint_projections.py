"""Add email complaint projections and suppression reason

Revision ID: e5a7c9d1f3b5
Revises: d3f5a7c9e1b3
Create Date: 2026-08-04 01:25:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "e5a7c9d1f3b5"
down_revision: str | Sequence[str] | None = "d3f5a7c9e1b3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TYPE suppressionreason ADD VALUE IF NOT EXISTS 'EMAIL_COMPLAINT'")
    op.create_table(
        "email_complaint_projections",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("source_system", sa.String(length=64), nullable=False),
        sa.Column("source_complaint_id", sa.String(length=255), nullable=False),
        sa.Column("normalized_contact_value", sa.String(length=255), nullable=False),
        sa.Column(
            "complaint_type",
            sa.Enum(
                "RECIPIENT_SPAM",
                "FEEDBACK_LOOP",
                "DMARC_FORENSIC",
                "AUTHENTICATION_FAILURE",
                "OTHER",
                name="emailcomplainttype",
            ),
            nullable=False,
        ),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("provider_message_id", sa.String(length=255), nullable=False),
        sa.Column(
            "evidence_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("suppression_entry_id", sa.UUID(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["suppression_entry_id"], ["suppression_entries.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_system", "source_complaint_id"),
    )
    op.create_index(
        op.f("ix_email_complaint_projections_normalized_contact_value"),
        "email_complaint_projections",
        ["normalized_contact_value"],
        unique=False,
    )
    op.create_index(
        op.f("ix_email_complaint_projections_suppression_entry_id"),
        "email_complaint_projections",
        ["suppression_entry_id"],
        unique=False,
    )
    op.create_index(
        "ix_email_complaint_projections_contact_occurred",
        "email_complaint_projections",
        ["normalized_contact_value", "occurred_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_email_complaint_projections_contact_occurred",
        table_name="email_complaint_projections",
    )
    op.drop_index(
        op.f("ix_email_complaint_projections_suppression_entry_id"),
        table_name="email_complaint_projections",
    )
    op.drop_index(
        op.f("ix_email_complaint_projections_normalized_contact_value"),
        table_name="email_complaint_projections",
    )
    op.drop_table("email_complaint_projections")
    op.execute("DROP TYPE IF EXISTS emailcomplainttype")
    # PostgreSQL enum values cannot be removed safely without rebuilding the
    # shared suppressionreason type; the additive EMAIL_COMPLAINT value is retained.
