from datetime import datetime
from uuid import UUID

from lead_harvester.models.canonical import OperatingStatus
from lead_harvester.schemas.common import BaseSchema


class BranchSchema(BaseSchema):
    id: UUID
    branch_name: str
    address: str
    city: str
    country_code: str
    provider_ids: dict


class ContactPointSchema(BaseSchema):
    id: UUID
    contact_type: str
    contact_value: str
    person_name: str | None = None
    role: str | None = None


class InstitutionBase(BaseSchema):
    canonical_name: str
    institution_type: str
    domain: str | None = None
    website: str | None = None
    status: OperatingStatus
    confidence_score: float


class InstitutionListResponse(InstitutionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class InstitutionDetailResponse(InstitutionListResponse):
    branches: list[BranchSchema] = []
    contact_points: list[ContactPointSchema] = []


class PaginatedInstitutions(BaseSchema):
    items: list[InstitutionListResponse]
    total: int
    page: int
    size: int
