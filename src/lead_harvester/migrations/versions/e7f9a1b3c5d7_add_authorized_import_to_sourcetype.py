"""Add AUTHORIZED_IMPORT to sourcetype enum

Revision ID: e7f9a1b3c5d7
Revises: d5e7f9a1b3c5
Create Date: 2026-07-30 00:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e7f9a1b3c5d7"
down_revision: str | Sequence[str] | None = "d5e7f9a1b3c5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """
    New SourceType member for the authorized-imports connector (CSV/bulk
    ingestion of licensed or manually-sourced institution/contact data --
    docs/ROADMAP.md's Module #2 "accepted pattern" alternative to
    unauthorized scraping/account automation).
    """
    op.execute("ALTER TYPE sourcetype ADD VALUE IF NOT EXISTS 'AUTHORIZED_IMPORT'")


def downgrade() -> None:
    """
    Postgres has no ALTER TYPE ... DROP VALUE -- removing an enum value
    requires rebuilding the type, which isn't safe to do generically without
    knowing whether any row currently uses it. No-op; the added value is
    simply unused if this revision is conceptually "reverted".
    """
