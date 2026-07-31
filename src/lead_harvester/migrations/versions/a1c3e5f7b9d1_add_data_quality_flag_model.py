"""Add data quality flag model

Revision ID: a1c3e5f7b9d1
Revises: f9c1a3e5b7d9
Create Date: 2026-07-30 22:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a1c3e5f7b9d1"
down_revision: str | Sequence[str] | None = "f9c1a3e5b7d9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "data_quality_flags",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("institution_id", sa.UUID(), nullable=False),
        sa.Column(
            "flag_type",
            sa.Enum(
                "CONFIDENCE_DRIFT",
                "CONFLICTING_FIELD",
                "STALE_EVIDENCE",
                "UNREACHABLE_CONTACT",
                name="flagtype",
            ),
            nullable=False,
        ),
        sa.Column("field_name", sa.String(length=255), nullable=True),
        sa.Column("details", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "status",
            sa.Enum("OPEN", "RESOLVED", "DISMISSED", name="flagstatus"),
            nullable=False,
        ),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolution_note", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["institution_id"],
            ["canonical_institutions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_data_quality_flags_institution_id"),
        "data_quality_flags",
        ["institution_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_data_quality_flags_flag_type"), "data_quality_flags", ["flag_type"], unique=False
    )
    op.create_index(
        op.f("ix_data_quality_flags_status"), "data_quality_flags", ["status"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_data_quality_flags_status"), table_name="data_quality_flags")
    op.drop_index(op.f("ix_data_quality_flags_flag_type"), table_name="data_quality_flags")
    op.drop_index(op.f("ix_data_quality_flags_institution_id"), table_name="data_quality_flags")
    op.drop_table("data_quality_flags")
    op.execute("DROP TYPE IF EXISTS flagstatus")
    op.execute("DROP TYPE IF EXISTS flagtype")
