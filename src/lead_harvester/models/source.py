import enum
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
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
    AUTHORIZED_IMPORT = "authorized_import"


class RunStatus(str, enum.Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"


class SourceRun(Base):
    __tablename__ = "source_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType), nullable=False)
    run_metadata: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[RunStatus] = mapped_column(
        Enum(RunStatus), default=RunStatus.STARTED, nullable=False
    )

    records: Mapped[list["RawSourceRecord"]] = relationship(
        "RawSourceRecord", back_populates="run", cascade="all, delete-orphan"
    )


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

    raw_payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    # Normalized fields for efficient Blocking / Candidate Generation
    normalized_name: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    normalized_phone: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    normalized_domain: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    # PostGIS Geography type (Point, SRID 4326)
    location = mapped_column(Geography(geometry_type="POINT", srid=4326), nullable=True)

    extracted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    run: Mapped["SourceRun"] = relationship("SourceRun", back_populates="records")


class RawPageSnapshot(Base):
    """
    An append-only record of one page fetch attempt during a WEBSITE
    crawl -- see docs/ROADMAP.md module 3's raw_snapshot sub-concern.

    RawSourceRecord.raw_payload (above) stores the EXTRACTED lead fields
    for a domain (name/phone/email/etc, aggregated across every page that
    contributed to it) -- it never kept the actual fetched HTML, so there
    was no way to audit what a crawl actually saw, re-run extraction logic
    against historical pages without re-fetching, or distinguish "page had
    no useful data" from "page was skipped/failed and we never really
    looked". This is that raw record: one row per page the crawler
    attempted, success or failure, written by sources/web.py::WebCrawler
    (accumulated on the crawler instance during crawl(), persisted by
    pipeline.py::_run_web_crawler after the run's SourceRun exists).

    Known v1 limitation: html is stored unbounded (up to
    Settings.max_response_bytes, the same cap the crawler already enforces
    at fetch time) -- no separate retention/expiry policy exists yet for
    this table specifically (services/compliance_service.py's
    purge_expired_raw_records only ever targeted RawSourceRecord).

    Correction: a single WEBSITE SourceRun can (and typically does) crawl
    several different seed domains in one crawl() call -- sources/web.py's
    WebCrawler accepts a whole seed list and accumulates every page fetch
    from every domain onto the same `snapshots` list, and pipeline.py's
    `for lead in leads:` loop then creates one RawSourceRecord per DOMAIN,
    not per run. `source_run_id` alone is therefore a "was fetched in the
    same crawl batch" grain, not a "belongs to this institution's website"
    grain -- a query that scoped website-quality snapshots by run
    membership alone (as an earlier version of this table's only consumer,
    services/lead_profile_service.py::_get_website_snapshots, did) could
    silently pull in another institution's pages that happened to be
    crawled in the same run. normalized_domain/raw_source_record_id/
    institution_id below are the exact-grain link that was missing --
    every website-quality query must filter by institution_id (or, before
    resolution has run, normalized_domain), never by source_run_id alone.
    """

    __tablename__ = "raw_page_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("source_runs.id"), nullable=False, index=True
    )

    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    # The URL actually fetched after following redirects -- differs from
    # `url` whenever the page redirected; empty when the fetch never got
    # far enough to know (e.g. robots.txt disallowed it).
    final_url: Mapped[str] = mapped_column(String(2048), default="", nullable=False)

    # The exact-grain link this table was missing -- see the class
    # docstring's "Correction" note. normalized_domain is always
    # computable at fetch time (from final_url, falling back to url) and
    # uses the same normalization resolution/normalize.py::normalize_domain
    # applies to RawSourceRecord.normalized_domain, so the two compare
    # equal for pages that fed the same domain's Lead.
    #
    # raw_source_record_id/institution_id are only knowable once this
    # snapshot's domain has produced a persisted RawSourceRecord and (for
    # institution_id) that record has been resolved -- both stay NULL for
    # a snapshot whose domain never yielded a useful extraction (e.g.
    # every page for that domain failed/was robots-disallowed) or whose
    # record failed resolution. A NULL institution_id must never be
    # treated as "belongs to no institution and is therefore safe to
    # include" -- it means "not yet linked," and a website-quality query
    # must exclude it, not fall back to matching by run.
    normalized_domain: Mapped[str] = mapped_column(
        String(255), default="", nullable=False, index=True
    )
    # CASCADE: see migration e2a4c6f8b0d2 -- purge_expired_raw_records must
    # be able to remove an old, unreferenced RawSourceRecord even when a
    # snapshot still points at it (this table has no retention policy of
    # its own yet).
    raw_source_record_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("raw_source_records.id", ondelete="CASCADE"), nullable=True, index=True
    )
    institution_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("canonical_institutions.id"), nullable=True, index=True
    )

    status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    content_type: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    html: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Empty for a successful fetch -- a short machine-readable reason
    # otherwise (e.g. "robots_disallowed", "http_error: 404",
    # "non_html_content_type", "response_too_large", "decode_error").
    fetch_error: Mapped[str] = mapped_column(String(255), default="", nullable=False)

    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), index=True
    )

    run: Mapped["SourceRun"] = relationship("SourceRun")
