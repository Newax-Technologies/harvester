"""Add domain/institution linkage to raw_page_snapshots

Revision ID: e2a4c6f8b0d2
Revises: e5a7c9d1f3b5
Create Date: 2026-08-01 00:00:00.000000

"""

from collections.abc import Sequence
from urllib.parse import urlparse

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "e2a4c6f8b0d2"
down_revision: str | Sequence[str] | None = "e5a7c9d1f3b5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _normalize_domain(url: str) -> str:
    """
    Mirrors resolution/normalize.py::normalize_domain -- duplicated here
    rather than imported, since a migration must keep working exactly as
    written even if the application's own normalizer changes shape later.
    """
    if not url:
        return ""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    try:
        domain = urlparse(url).netloc.lower()
    except ValueError:
        return ""
    return domain.removeprefix("www.")


def upgrade() -> None:
    """
    Correction: a single WEBSITE SourceRun crawls every seed domain passed
    to WebCrawler.crawl() in one call, not just one -- RawPageSnapshot rows
    only ever carried source_run_id, so a website-quality query scoped to
    "snapshots from runs that touched this institution" (the only grain
    available) could pull in another institution's pages fetched in the
    same run. This adds the missing exact-grain link -- normalized_domain
    (always computable), raw_source_record_id, and institution_id (both
    nullable: only knowable once a domain's RawSourceRecord exists and,
    for institution_id, has been resolved) -- and backfills every existing
    row using the corrected (source_run_id, domain) pair instead of
    source_run_id alone.

    normalized_domain is staged nullable -> backfill -> not-null (AGENTS.md
    convention for any new required column on a table that may already
    have rows), not added NOT NULL directly.

    See models/source.py::RawPageSnapshot's own "Correction" docstring
    note for the full explanation and pipeline.py::_run_web_crawler for
    where these three fields are populated going forward.
    """
    op.add_column(
        "raw_page_snapshots",
        sa.Column("normalized_domain", sa.String(255), nullable=True),
    )
    op.add_column(
        "raw_page_snapshots",
        sa.Column("raw_source_record_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.add_column(
        "raw_page_snapshots",
        sa.Column("institution_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_raw_page_snapshots_raw_source_record_id",
        "raw_page_snapshots",
        "raw_source_records",
        ["raw_source_record_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_raw_page_snapshots_institution_id",
        "raw_page_snapshots",
        "canonical_institutions",
        ["institution_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "ix_raw_page_snapshots_normalized_domain", "raw_page_snapshots", ["normalized_domain"]
    )
    op.create_index(
        "ix_raw_page_snapshots_raw_source_record_id",
        "raw_page_snapshots",
        ["raw_source_record_id"],
    )
    op.create_index(
        "ix_raw_page_snapshots_institution_id", "raw_page_snapshots", ["institution_id"]
    )

    conn = op.get_bind()

    snapshots = sa.table(
        "raw_page_snapshots",
        sa.column("id", postgresql.UUID),
        sa.column("source_run_id", postgresql.UUID),
        sa.column("url", sa.String),
        sa.column("final_url", sa.String),
        sa.column("normalized_domain", sa.String),
        sa.column("raw_source_record_id", postgresql.UUID),
        sa.column("institution_id", postgresql.UUID),
    )
    raw_source_records = sa.table(
        "raw_source_records",
        sa.column("id", postgresql.UUID),
        sa.column("source_run_id", postgresql.UUID),
        sa.column("normalized_domain", sa.String),
    )
    field_provenance = sa.table(
        "field_provenance",
        sa.column("raw_record_id", postgresql.UUID),
        sa.column("canonical_id", postgresql.UUID),
    )

    record_id_by_run_and_domain: dict[tuple, object] = {}
    for row in conn.execute(
        sa.select(
            raw_source_records.c.id,
            raw_source_records.c.source_run_id,
            raw_source_records.c.normalized_domain,
        )
    ):
        if row.normalized_domain:
            record_id_by_run_and_domain[(row.source_run_id, row.normalized_domain)] = row.id

    canonical_id_by_raw_record: dict[object, object] = {}
    for row in conn.execute(
        sa.select(field_provenance.c.raw_record_id, field_provenance.c.canonical_id)
    ):
        canonical_id_by_raw_record.setdefault(row.raw_record_id, row.canonical_id)

    backfill_batch_size = 5000
    last_id = None
    while True:
        batch_stmt = (
            sa.select(
                snapshots.c.id, snapshots.c.source_run_id, snapshots.c.url, snapshots.c.final_url
            )
            .order_by(snapshots.c.id)
            .limit(backfill_batch_size)
        )
        if last_id is not None:
            batch_stmt = batch_stmt.where(snapshots.c.id > last_id)
        batch = conn.execute(batch_stmt).all()
        if not batch:
            break

        updates = []
        for snap_id, source_run_id, url, final_url in batch:
            domain = _normalize_domain(final_url or url)
            record_id = record_id_by_run_and_domain.get((source_run_id, domain)) if domain else None
            institution_id = canonical_id_by_raw_record.get(record_id) if record_id else None
            updates.append(
                {
                    "_snap_id": snap_id,
                    "_domain": domain,
                    "_record_id": record_id,
                    "_institution_id": institution_id,
                }
            )

        conn.execute(
            snapshots.update()
            .where(snapshots.c.id == sa.bindparam("_snap_id"))
            .values(
                normalized_domain=sa.bindparam("_domain"),
                raw_source_record_id=sa.bindparam("_record_id"),
                institution_id=sa.bindparam("_institution_id"),
            ),
            updates,
        )

        last_id = batch[-1].id
        if len(batch) < backfill_batch_size:
            break

    op.alter_column(
        "raw_page_snapshots", "normalized_domain", existing_type=sa.String(255), nullable=False
    )


def downgrade() -> None:
    op.drop_index("ix_raw_page_snapshots_institution_id", table_name="raw_page_snapshots")
    op.drop_index("ix_raw_page_snapshots_raw_source_record_id", table_name="raw_page_snapshots")
    op.drop_index("ix_raw_page_snapshots_normalized_domain", table_name="raw_page_snapshots")
    op.drop_constraint(
        "fk_raw_page_snapshots_institution_id", "raw_page_snapshots", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_raw_page_snapshots_raw_source_record_id", "raw_page_snapshots", type_="foreignkey"
    )
    op.drop_column("raw_page_snapshots", "institution_id")
    op.drop_column("raw_page_snapshots", "raw_source_record_id")
    op.drop_column("raw_page_snapshots", "normalized_domain")
