"""Add compliance models

Revision ID: b2d4f6a8c0e2
Revises: a1c3e5f7b9d1
Create Date: 2026-07-31 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b2d4f6a8c0e2"
down_revision: str | Sequence[str] | None = "a1c3e5f7b9d1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "suppression_entries",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("normalized_contact_value", sa.String(length=255), nullable=False),
        sa.Column("channel", sa.String(length=50), nullable=True),
        sa.Column(
            "reason",
            sa.Enum("OPT_OUT", "BOUNCED", "LEGAL_REQUEST", "MANUAL", name="suppressionreason"),
            nullable=False,
        ),
        sa.Column("note", sa.Text(), nullable=False),
        sa.Column("suppressed_by", sa.String(length=255), nullable=False),
        sa.Column("suppressed_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_suppression_entries_normalized_contact_value"),
        "suppression_entries",
        ["normalized_contact_value"],
        unique=False,
    )

    op.create_table(
        "deletion_requests",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "subject_type",
            sa.Enum("INSTITUTION", "CONTACT_POINT", name="deletionsubjecttype"),
            nullable=False,
        ),
        sa.Column("subject_id", sa.UUID(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("PENDING", "COMPLETED", "REJECTED", name="deletionrequeststatus"),
            nullable=False,
        ),
        sa.Column("requestor_note", sa.Text(), nullable=False),
        sa.Column("rejection_reason", sa.Text(), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("fulfilled_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_deletion_requests_subject_id"), "deletion_requests", ["subject_id"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_deletion_requests_subject_id"), table_name="deletion_requests")
    op.drop_table("deletion_requests")
    op.execute("DROP TYPE IF EXISTS deletionrequeststatus")
    op.execute("DROP TYPE IF EXISTS deletionsubjecttype")

    op.drop_index(
        op.f("ix_suppression_entries_normalized_contact_value"), table_name="suppression_entries"
    )
    op.drop_table("suppression_entries")
    op.execute("DROP TYPE IF EXISTS suppressionreason")
