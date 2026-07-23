import enum
import uuid
from datetime import datetime, timezone
from typing import Any, Dict

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lead_harvester.database import Base


class SourceType(str, enum.Enum):
    GOOGLE_PLACES = "google_places"
    WEBSITE = "website"
    TELEGRAM = "telegram"
    LINKEDIN = "linkedin"
    YANDEX = "yandex"
    APPLE_MAPS = "apple_maps"
    MANUAL = "manual"


class RunStatus(str, enum.Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"


class SourceRun(Base):
    __tablename__ = "source_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType), nullable=False)
    run_metadata: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.STARTED, nullable=False)

    records: Mapped[list["RawSourceRecord"]] = relationship("RawSourceRecord", back_populates="run", cascade="all, delete-orphan")


from geoalchemy2 import Geography

class RawSourceRecord(Base):
    """
    An append-only, immutable record representing exactly what was extracted
    from a source before any normalization or merging.
    """
    __tablename__ = "raw_source_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_run_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("source_runs.id"), nullable=False)
    
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType), nullable=False)
    source_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    
    raw_payload: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    
    # Normalized fields for efficient Blocking / Candidate Generation
    normalized_name: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    normalized_phone: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    normalized_domain: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    
    # PostGIS Geography type (Point, SRID 4326)
    location = mapped_column(Geography(geometry_type='POINT', srid=4326), nullable=True)

    
    extracted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    run: Mapped["SourceRun"] = relationship("SourceRun", back_populates="records")
