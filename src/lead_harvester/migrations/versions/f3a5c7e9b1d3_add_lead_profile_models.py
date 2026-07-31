"""Add lead profile models

Revision ID: f3a5c7e9b1d3
Revises: e7f9a1b3c5d7
Create Date: 2026-07-30 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f3a5c7e9b1d3"
down_revision: str | Sequence[str] | None = "e7f9a1b3c5d7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "lead_profiles",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("institution_id", sa.UUID(), nullable=False),
        sa.Column("overall_score", sa.Integer(), nullable=False),
        sa.Column("score_breakdown", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("has_phone", sa.Boolean(), nullable=False),
        sa.Column("has_email", sa.Boolean(), nullable=False),
        sa.Column("has_named_contact", sa.Boolean(), nullable=False),
        sa.Column(
            "qualification_status",
            # Reuses the qualificationstatus enum type already created by
            # 44e94c2881ad_add_qualification_models.py -- create_type=False
            # so this doesn't attempt (and fail on) CREATE TYPE again.
            postgresql.ENUM(
                "PENDING",
                "QUALIFIED",
                "DISQUALIFIED",
                "NEEDS_REVIEW",
                name="qualificationstatus",
                create_type=False,
            ),
            nullable=True,
        ),
        sa.Column("organization_summary", sa.Text(), nullable=False),
        sa.Column("evidence_count", sa.Integer(), nullable=False),
        sa.Column("computed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["institution_id"],
            ["canonical_institutions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_lead_profiles_institution_id"), "lead_profiles", ["institution_id"], unique=True
    )

    op.create_table(
        "lead_score_history",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("institution_id", sa.UUID(), nullable=False),
        sa.Column("overall_score", sa.Integer(), nullable=False),
        sa.Column("score_breakdown", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("computed_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["institution_id"],
            ["canonical_institutions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_lead_score_history_institution_id"),
        "lead_score_history",
        ["institution_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_lead_score_history_institution_id"), table_name="lead_score_history")
    op.drop_table("lead_score_history")

    op.drop_index(op.f("ix_lead_profiles_institution_id"), table_name="lead_profiles")
    op.drop_table("lead_profiles")
