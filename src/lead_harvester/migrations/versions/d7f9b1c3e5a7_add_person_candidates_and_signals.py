"""Add person_candidates and signals

Revision ID: d7f9b1c3e5a7
Revises: c5e7a9b1d3f5
Create Date: 2026-08-01 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d7f9b1c3e5a7"
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
        sa.Column(
            "status",
            sa.Enum("ACTIVE", "MERGED", name="personcandidatestatus"),
            nullable=False,
        ),
        sa.Column("evidence_count", sa.Integer(), nullable=False),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["institution_id"], ["canonical_institutions.id"]),
        sa.PrimaryKeyConstraint("id"),
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
    # One PersonCandidate per (institution, normalized_name) -- defense in
    # depth alongside services/person_candidate_service.py's own
    # SELECT ... FOR UPDATE find-or-create, the same pattern
    # LeadReservation's partial unique index uses for its own claim query.
    op.create_unique_constraint(
        "uq_person_candidates_institution_normalized_name",
        "person_candidates",
        ["institution_id", "normalized_name"],
    )

    op.create_table(
        "signals",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("institution_id", sa.UUID(), nullable=False),
        sa.Column(
            "signal_type",
            sa.Enum("PAIN_POINT", "BUYING_SIGNAL", name="signaltype"),
            nullable=False,
        ),
        sa.Column("signal_text", sa.Text(), nullable=False),
        sa.Column("source_url", sa.String(length=500), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["institution_id"], ["canonical_institutions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_signals_institution_id"), "signals", ["institution_id"], unique=False)
    op.create_index(op.f("ix_signals_signal_type"), "signals", ["signal_type"], unique=False)
    op.create_index(op.f("ix_signals_detected_at"), "signals", ["detected_at"], unique=False)

    op.add_column("contact_points", sa.Column("person_candidate_id", sa.UUID(), nullable=True))
    op.create_index(
        op.f("ix_contact_points_person_candidate_id"),
        "contact_points",
        ["person_candidate_id"],
        unique=False,
    )
    op.create_foreign_key(
        "fk_contact_points_person_candidate_id",
        "contact_points",
        "person_candidates",
        ["person_candidate_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_contact_points_person_candidate_id", "contact_points", type_="foreignkey"
    )
    op.drop_index(op.f("ix_contact_points_person_candidate_id"), table_name="contact_points")
    op.drop_column("contact_points", "person_candidate_id")

    op.drop_index(op.f("ix_signals_detected_at"), table_name="signals")
    op.drop_index(op.f("ix_signals_signal_type"), table_name="signals")
    op.drop_index(op.f("ix_signals_institution_id"), table_name="signals")
    op.drop_table("signals")
    op.execute("DROP TYPE IF EXISTS signaltype")

    op.drop_constraint(
        "uq_person_candidates_institution_normalized_name",
        "person_candidates",
        type_="unique",
    )
    op.drop_index(op.f("ix_person_candidates_normalized_name"), table_name="person_candidates")
    op.drop_index(op.f("ix_person_candidates_institution_id"), table_name="person_candidates")
    op.drop_table("person_candidates")
    op.execute("DROP TYPE IF EXISTS personcandidatestatus")
