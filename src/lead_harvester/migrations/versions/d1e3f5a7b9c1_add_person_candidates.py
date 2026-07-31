"""Add person_candidates and link contact_points to them

Revision ID: d1e3f5a7b9c1
Revises: c5e7a9b1d3f5
Create Date: 2026-07-31 03:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d1e3f5a7b9c1"
down_revision: str | Sequence[str] | None = "c5e7a9b1d3f5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "person_candidates",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("institution_id", sa.UUID(), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("normalized_name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["institution_id"], ["canonical_institutions.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "institution_id",
            "normalized_name",
            name="uq_person_candidates_institution_normalized_name",
        ),
    )
    op.create_index(
        op.f("ix_person_candidates_institution_id"),
        "person_candidates",
        ["institution_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_person_candidates_normalized_name"),
        "person_candidates",
        ["normalized_name"],
        unique=False,
    )

    op.add_column(
        "contact_points", sa.Column("person_candidate_id", sa.UUID(), nullable=True)
    )
    op.create_foreign_key(
        "fk_contact_points_person_candidate_id",
        "contact_points",
        "person_candidates",
        ["person_candidate_id"],
        ["id"],
    )
    op.create_index(
        op.f("ix_contact_points_person_candidate_id"),
        "contact_points",
        ["person_candidate_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_contact_points_person_candidate_id"), table_name="contact_points")
    op.drop_constraint(
        "fk_contact_points_person_candidate_id", "contact_points", type_="foreignkey"
    )
    op.drop_column("contact_points", "person_candidate_id")

    op.drop_index(op.f("ix_person_candidates_normalized_name"), table_name="person_candidates")
    op.drop_index(op.f("ix_person_candidates_institution_id"), table_name="person_candidates")
    op.drop_table("person_candidates")
