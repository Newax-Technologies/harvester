"""Add deletion graph cascades and deletion_requests.manifest

Revision ID: a5c7e9f1b3d5
Revises: f4b6d8e0a2c4
Create Date: 2026-08-01 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a5c7e9f1b3d5"
down_revision: str | Sequence[str] | None = "f4b6d8e0a2c4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (constraint_name, table, column, foreign_table, ondelete) -- every FK
# reachable from canonical_institutions.id or raw_source_records.id, made
# CASCADE so a single DELETE against either root removes its entire owned
# subtree in one statement/transaction instead of requiring an
# application-level ordered delete per table. See
# services/compliance_service.py::erase_institution for the explicit
# deletion graph this backs, and models/*.py's individual FK declarations
# (now carrying the matching ondelete=) for per-table rationale.
#
# raw_page_snapshots.raw_source_record_id -> raw_source_records and
# raw_page_snapshots.institution_id -> canonical_institutions are
# deliberately NOT listed here: migration e2a4c6f8b0d2 already made both
# ondelete=CASCADE (for purge_expired_raw_records' sake and for
# fulfill_deletion's sake respectively -- separate reasons that happen to
# want the same behavior) -- redeclaring either here would make this
# migration's downgrade() incorrectly reset it to NO ACTION, undoing that
# earlier fix, for no benefit (both are already correct).
_CASCADE_FKS: list[tuple[str, str, str, str]] = [
    (
        "account_briefs_institution_id_fkey",
        "account_briefs",
        "institution_id",
        "canonical_institutions",
    ),
    ("branches_institution_id_fkey", "branches", "institution_id", "canonical_institutions"),
    (
        "contact_points_institution_id_fkey",
        "contact_points",
        "institution_id",
        "canonical_institutions",
    ),
    (
        "data_quality_flags_institution_id_fkey",
        "data_quality_flags",
        "institution_id",
        "canonical_institutions",
    ),
    (
        "event_outbox_institution_id_fkey",
        "event_outbox",
        "institution_id",
        "canonical_institutions",
    ),
    (
        "field_provenance_canonical_id_fkey",
        "field_provenance",
        "canonical_id",
        "canonical_institutions",
    ),
    (
        "field_provenance_raw_record_id_fkey",
        "field_provenance",
        "raw_record_id",
        "raw_source_records",
    ),
    (
        "lead_profiles_institution_id_fkey",
        "lead_profiles",
        "institution_id",
        "canonical_institutions",
    ),
    (
        "lead_reservations_institution_id_fkey",
        "lead_reservations",
        "institution_id",
        "canonical_institutions",
    ),
    (
        "lead_score_history_institution_id_fkey",
        "lead_score_history",
        "institution_id",
        "canonical_institutions",
    ),
    (
        "match_assessments_candidate_id_fkey",
        "match_assessments",
        "candidate_id",
        "resolution_candidates",
    ),
    ("outreach_drafts_brief_id_fkey", "outreach_drafts", "brief_id", "account_briefs"),
    ("outreach_outcomes_draft_id_fkey", "outreach_outcomes", "draft_id", "outreach_drafts"),
    (
        "person_candidates_institution_id_fkey",
        "person_candidates",
        "institution_id",
        "canonical_institutions",
    ),
    (
        "qualification_assessments_institution_id_fkey",
        "qualification_assessments",
        "institution_id",
        "canonical_institutions",
    ),
    (
        "research_findings_institution_id_fkey",
        "research_findings",
        "institution_id",
        "canonical_institutions",
    ),
    ("research_findings_job_id_fkey", "research_findings", "job_id", "research_jobs"),
    (
        "research_jobs_institution_id_fkey",
        "research_jobs",
        "institution_id",
        "canonical_institutions",
    ),
    (
        "resolution_candidates_raw_record_id_fkey",
        "resolution_candidates",
        "raw_record_id",
        "raw_source_records",
    ),
    (
        "resolution_candidates_target_canonical_id_fkey",
        "resolution_candidates",
        "target_canonical_id",
        "canonical_institutions",
    ),
    (
        "resolution_candidates_target_raw_record_id_fkey",
        "resolution_candidates",
        "target_raw_record_id",
        "raw_source_records",
    ),
    ("signals_institution_id_fkey", "signals", "institution_id", "canonical_institutions"),
]

# ContactPoint.person_candidate_id is a soft classification link, not
# ownership -- a ContactPoint must survive its PersonCandidate being
# removed independently of an institution-wide erasure, so this one gets
# SET NULL instead of CASCADE.
_SET_NULL_FKS: list[tuple[str, str, str, str]] = [
    (
        "fk_contact_points_person_candidate_id",
        "contact_points",
        "person_candidate_id",
        "person_candidates",
    ),
]


def upgrade() -> None:
    for name, table, column, foreign_table in _CASCADE_FKS:
        op.drop_constraint(name, table, type_="foreignkey")
        op.create_foreign_key(name, table, foreign_table, [column], ["id"], ondelete="CASCADE")

    for name, table, column, foreign_table in _SET_NULL_FKS:
        op.drop_constraint(name, table, type_="foreignkey")
        op.create_foreign_key(name, table, foreign_table, [column], ["id"], ondelete="SET NULL")

    # Staged nullable -> backfill -> not-null (AGENTS.md convention for any
    # new required column on a table that may already have rows), not
    # added NOT NULL directly -- a constant server_default alone still
    # bypasses the convention even though it happens to avoid a null
    # error.
    op.add_column(
        "deletion_requests",
        sa.Column("manifest", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.execute("UPDATE deletion_requests SET manifest = '{}'::jsonb WHERE manifest IS NULL")
    op.alter_column(
        "deletion_requests",
        "manifest",
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        nullable=False,
        server_default="{}",
    )

    # Correction: services/compliance_service.py::_erase_institution's own
    # "institution.deleted" tombstone event must survive the institution
    # row it's about being deleted in the same transaction -- see
    # models/outbox.py's institution_id comment. Every other EventOutbox
    # row still sets it; only this one deliberately doesn't.
    op.alter_column(
        "event_outbox",
        "institution_id",
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=True,
    )


def downgrade() -> None:
    # Correction: a surviving "institution.deleted" tombstone row (see this
    # migration's own upgrade() comment) has institution_id=NULL by design
    # once this feature has been used -- SET NOT NULL below would otherwise
    # be rejected by Postgres while any such row exists, making downgrade
    # unusable after normal feature usage. A tombstone has no institution
    # left to attribute it to (the whole point is that the institution is
    # gone), so it cannot be repaired into a valid pre-migration row; drop
    # it rather than block the downgrade indefinitely.
    op.execute("DELETE FROM event_outbox WHERE institution_id IS NULL")

    op.alter_column(
        "event_outbox",
        "institution_id",
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=False,
    )

    op.drop_column("deletion_requests", "manifest")

    for name, table, column, foreign_table in _SET_NULL_FKS:
        op.drop_constraint(name, table, type_="foreignkey")
        op.create_foreign_key(name, table, foreign_table, [column], ["id"])

    for name, table, column, foreign_table in _CASCADE_FKS:
        op.drop_constraint(name, table, type_="foreignkey")
        op.create_foreign_key(name, table, foreign_table, [column], ["id"])
