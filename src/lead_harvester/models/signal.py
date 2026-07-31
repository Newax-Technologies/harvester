"""
A discrete, individually-queryable opportunity/pain signal detected for
an institution -- see docs/ROADMAP.md module 1 ("Entity Registry") and
module 7 ("Business Intelligence").

intelligence/researcher.py's AI analysis already produces pain_points/
buying_signals lists, but previously only ever stored them as one opaque
JSON blob inside a single ResearchFinding row (finding_key="pain_points"/
"buying_signals") -- unqueryable/unfilterable as individual signals. Each
list item now ALSO becomes its own Signal row here (alongside, not
instead of, that ResearchFinding -- the finding stays the complete,
unedited AI output; Signal is the queryable index over one slice of it),
so ranking/dashboard/export consumers can filter, count, or eventually
expire individual signals rather than parsing a JSON blob.

Known v1 limitation: no freshness/commercial_relevance scoring fields --
the AI prompt this is sourced from doesn't produce a per-signal score
today (only an institution-level lead_score), so no field is added here
that nothing populates. Age can be derived from detected_at by any
consumer that wants a freshness signal.
"""

import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base


class SignalType(str, enum.Enum):
    PAIN_POINT = "pain_point"
    BUYING_SIGNAL = "buying_signal"
    # docs/ROADMAP.md module 20: a detected fact ("has an LMS"), distinct
    # from a pain point or buying signal by itself.
    TECHNOLOGY_PRESENT = "technology_present"


class Signal(Base):
    __tablename__ = "signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("canonical_institutions.id"), nullable=False, index=True
    )

    signal_type: Mapped[SignalType] = mapped_column(Enum(SignalType), nullable=False, index=True)
    signal_text: Mapped[str] = mapped_column(Text, nullable=False)

    # E.g. the LinkedIn profile URL this was detected from.
    source_url: Mapped[str] = mapped_column(String(500), default="", nullable=False)

    confidence_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), index=True
    )

    institution = relationship("CanonicalInstitution")
