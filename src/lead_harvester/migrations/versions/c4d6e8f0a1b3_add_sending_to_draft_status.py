"""Add SENDING to draftstatus enum

Revision ID: c4d6e8f0a1b3
Revises: b3c1d9e7f5a2
Create Date: 2026-07-30 00:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c4d6e8f0a1b3"
down_revision: str | Sequence[str] | None = "b3c1d9e7f5a2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """
    New intermediate state OutreachAutomator.run() uses to atomically claim
    a batch of APPROVED drafts (via SELECT ... FOR UPDATE SKIP LOCKED, then
    flip to SENDING in the same transaction) before sending them -- without
    it, two concurrent run() invocations could both read and send the same
    APPROVED drafts.
    """
    op.execute("ALTER TYPE draftstatus ADD VALUE IF NOT EXISTS 'SENDING' BEFORE 'SENT'")


def downgrade() -> None:
    """
    Postgres has no ALTER TYPE ... DROP VALUE -- removing an enum value
    requires rebuilding the type, which isn't safe to do generically without
    knowing whether any row is currently SENDING. No-op; the added value is
    simply unused if this revision is conceptually "reverted".
    """
