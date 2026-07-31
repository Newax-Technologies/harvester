import enum
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Float, ForeignKey, String, Text, DateTime, Enum, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geography

from lead_harvester.database import Base
from lead_harvester.models.verification import ContactVerification, VerificationStatus
from lead_harvester.models.compliance import ConsentBasis


class OperatingStatus(str, enum.Enum):
    OPERATIONAL = "operational"
    CLOSED_TEMPORARILY = "closed_temporarily"
    CLOSED_PERMANENTLY = "closed_permanently"
    UNKNOWN = "unknown"


class CanonicalInstitution(Base):
    """
    The pristine, resolved entity representing a single educational institution.
    Constructed by merging one or more RawSourceRecords.
    """
    __tablename__ = "canonical_institutions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Core Fields
    canonical_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    institution_type: Mapped[str] = mapped_column(String(100), default="", nullable=False)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    status: Mapped[OperatingStatus] = mapped_column(Enum(OperatingStatus), default=OperatingStatus.OPERATIONAL, nullable=False)
    
    # Trust score based on the number and quality of sources that confirm this entity
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    branches: Mapped[list["Branch"]] = relationship("Branch", back_populates="institution", cascade="all, delete-orphan")
    contact_points: Mapped[list["ContactPoint"]] = relationship("ContactPoint", back_populates="institution", cascade="all, delete-orphan")


class Branch(Base):
    """
    A specific physical location of a CanonicalInstitution.
    """
    __tablename__ = "branches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("canonical_institutions.id"), nullable=False)
    
    branch_name: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    address: Mapped[str] = mapped_column(Text, default="", nullable=False)
    
    location = mapped_column(Geography(geometry_type='POINT', srid=4326), nullable=True)
    
    # Store provider-specific IDs mapping to this exact physical location (e.g. Google Place IDs)
    provider_ids: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)

    institution: Mapped["CanonicalInstitution"] = relationship("CanonicalInstitution", back_populates="branches")


class ContactPoint(Base):
    """
    A unified contact method (e.g., a phone number or email) associated with an institution.
    If multiple branches share a phone number, it is stored here once to link them.
    """
    __tablename__ = "contact_points"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("canonical_institutions.id"), nullable=False)
    
    contact_type: Mapped[str] = mapped_column(String(50), nullable=False) # e.g. "phone", "email", "whatsapp", "telegram"
    contact_value: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    
    person_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    is_publicly_listed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Latest verification result (see models/verification.py for full history)
    verification_status: Mapped[VerificationStatus] = mapped_column(Enum(VerificationStatus), default=VerificationStatus.PENDING, nullable=False)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Lawful basis for holding/using this contact (see models/compliance.py)
    consent_basis: Mapped[ConsentBasis] = mapped_column(Enum(ConsentBasis), default=ConsentBasis.UNKNOWN, nullable=False)
    consent_note: Mapped[str] = mapped_column(Text, default="", nullable=False)

    institution: Mapped["CanonicalInstitution"] = relationship("CanonicalInstitution", back_populates="contact_points")
    verifications: Mapped[list["ContactVerification"]] = relationship("ContactVerification", back_populates="contact_point", cascade="all, delete-orphan")
