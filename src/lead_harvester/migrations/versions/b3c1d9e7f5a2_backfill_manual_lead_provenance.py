"""Backfill branch_membership provenance for pre-existing manual leads

Revision ID: b3c1d9e7f5a2
Revises: a4b6c8d0e2f4
Create Date: 2026-07-30 00:00:00.000000

"""

import uuid
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b3c1d9e7f5a2"
down_revision: str | Sequence[str] | None = "a4b6c8d0e2f4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """
    Every manual lead created before api/routes/manual_leads.py started
    writing a "branch_membership" FieldProvenance row (the fix this
    revision follows) has a RawSourceRecord with no link back to the
    CanonicalInstitution it produced. canonical/merger.py::
    find_canonical_for_raw_record relies entirely on that row, so without
    this backfill, a later scraped record matching one of these historical
    manual leads would create a second, duplicate institution instead of
    attaching to the existing one -- silently, with no error to signal it.

    The only historical Branch.provider_ids shape those old submissions
    ever wrote was a bare scalar under the "manual_record_id" key (fixed in
    this same PR to the {"manual": [source_id, ...]} list shape every other
    source_type now uses); match on that legacy shape specifically to find
    each orphaned record's institution. Idempotent and safe to re-run: only
    touches RawSourceRecord rows that still lack the provenance row, and is
    a pure no-op if none exist (e.g. a database that never had the old,
    unfixed manual_leads.py deployed against it).
    """
    conn = op.get_bind()

    raw_source_records = sa.table(
        "raw_source_records",
        sa.column("id", postgresql.UUID),
        sa.column("source_type", sa.String),
        sa.column("source_id", sa.String),
    )
    field_provenance = sa.table(
        "field_provenance",
        sa.column("id", postgresql.UUID),
        sa.column("canonical_id", postgresql.UUID),
        sa.column("raw_record_id", postgresql.UUID),
        sa.column("field_name", sa.String),
        sa.column("asserted_value", postgresql.JSONB),
        sa.column("assertion_trust", sa.Float),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    branches = sa.table(
        "branches",
        sa.column("institution_id", postgresql.UUID),
        sa.column("provider_ids", postgresql.JSONB),
    )

    already_provenanced = sa.select(field_provenance.c.raw_record_id).where(
        field_provenance.c.field_name == "branch_membership"
    )
    orphaned = conn.execute(
        sa.select(raw_source_records.c.id, raw_source_records.c.source_id).where(
            # source_type is a native Postgres enum column storing each
            # member's NAME, not its .value (SQLAlchemy's Enum() type
            # defaults to that; models/source.py's SourceType.MANUAL = "manual"
            # is stored as the label "MANUAL") -- confirmed against a live
            # DB (`SELECT enumlabel FROM pg_enum WHERE enumtypid =
            # 'sourcetype'::regtype`) rather than assumed. A bound parameter
            # (unlike a literal) also doesn't get an implicit cast against
            # an enum column, so the column itself must be cast to compare
            # against a plain string.
            sa.cast(raw_source_records.c.source_type, sa.String) == "MANUAL",
            raw_source_records.c.id.not_in(already_provenanced),
        )
    ).all()

    for record_id, source_id in orphaned:
        branch_row = conn.execute(
            sa.select(branches.c.institution_id)
            .where(branches.c.provider_ids["manual_record_id"].astext == source_id)
            .limit(1)
        ).first()
        if branch_row is None:
            # No branch was ever written with this legacy shape for this
            # record -- nothing to link it to; leave it for manual
            # investigation rather than guessing.
            continue

        conn.execute(
            field_provenance.insert().values(
                id=uuid.uuid4(),
                canonical_id=branch_row.institution_id,
                raw_record_id=record_id,
                field_name="branch_membership",
                asserted_value=source_id,
                assertion_trust=1.0,
                created_at=sa.func.now(),
            )
        )


def downgrade() -> None:
    """
    Irreversible by design: a backfilled branch_membership row is
    indistinguishable from one written normally at submission time, and
    removing them would just reopen the duplicate-institution bug for
    these specific records. No-op.
    """
