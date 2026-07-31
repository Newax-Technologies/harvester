import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from lead_harvester.database import Base


class Sector(Base):
    """
    A business vertical (education, healthcare, retail, ...) -- see
    docs/ROADMAP.md module 16. Deliberately a DB table, not a Python enum:
    a new sector is a row insert, not a migration. `institution_types` is
    the membership list `services/sector_service.py::resolve_sector_for_institution_type`
    matches a `CanonicalInstitution.institution_type` value against;
    `icp_criteria`/`qualification_rules` are per-sector targeting config
    consumed by later modules (17: Sector-Aware ICP & Qualification) --
    both start empty here and are filled in by an operator, not guessed.
    """

    __tablename__ = "sectors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    institution_types: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    icp_criteria: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    qualification_rules: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
