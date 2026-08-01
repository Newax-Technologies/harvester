"""Add domain/institution linkage to raw_page_snapshots

Revision ID: e2a4c6f8b0d2
Revises: d3f5a7c9e1b3
Create Date: 2026-08-01 00:00:00.000000

"""

from collections.abc import Sequence
from urllib.parse import urlparse

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "e2a4c6f8b0d2"
down_revision: str | Sequence[str] | None = "d3f5a7c9e1b3"
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

    See models/source.py::RawPageSnapshot's own "Correction" docstring
    note for the full explanation and pipeline.py::_run_web_crawler for
    where these three fields are populated going forward.
    """
    op.add_column(
        "raw_page_snapshots",
        sa.Column("normalized_domain", sa.String(255), nullable=False, server_default=""),
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
    )
    op.create_foreign_key(
        "fk_raw_page_snapshots_institution_id",
        "raw_page_snapshots",
        "canonical_institutions",
        ["institution_id"],
        ["id"],
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

    rows = conn.execute(
        sa.select(snapshots.c.id, snapshots.c.source_run_id, snapshots.c.url, snapshots.c.final_url)
    ).all()

    for snap_id, source_run_id, url, final_url in rows:
        domain = _normalize_domain(final_url or url)
        record_row = None
        if domain:
            # Scoped to (this snapshot's run, this snapshot's domain) --
            # the composite key that was missing -- not source_run_id
            # alone, which is exactly the bug this migration fixes.
            record_row = conn.execute(
                sa.select(raw_source_records.c.id)
                .where(
                    raw_source_records.c.source_run_id == source_run_id,
                    raw_source_records.c.normalized_domain == domain,
                )
                .limit(1)
            ).first()

        institution_id = None
        if record_row is not None:
            fp_row = conn.execute(
                sa.select(field_provenance.c.canonical_id)
                .where(field_provenance.c.raw_record_id == record_row.id)
                .limit(1)
            ).first()
            if fp_row is not None:
                institution_id = fp_row.canonical_id

        conn.execute(
            snapshots.update()
            .where(snapshots.c.id == snap_id)
            .values(
                normalized_domain=domain,
                raw_source_record_id=(record_row.id if record_row is not None else None),
                institution_id=institution_id,
            )
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
