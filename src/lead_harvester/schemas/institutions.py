from datetime import datetime
from uuid import UUID
from typing import Any, List, Optional
from pydantic import Field
from lead_harvester.models.canonical import OperatingStatus
from lead_harvester.schemas.common import BaseSchema

class BranchSchema(BaseSchema):
    id: UUID
    branch_name: str
    address: str
    provider_ids: dict

class ContactPointSchema(BaseSchema):
    id: UUID
    contact_type: str
    contact_value: str
    person_name: Optional[str] = None
    role: Optional[str] = None

class InstitutionBase(BaseSchema):
    canonical_name: str
    institution_type: str
    domain: Optional[str] = None
    website: Optional[str] = None
    status: OperatingStatus
    confidence_score: float

class InstitutionListResponse(InstitutionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

class InstitutionDetailResponse(InstitutionListResponse):
    branches: List[BranchSchema] = []
    contact_points: List[ContactPointSchema] = []

class PaginatedInstitutions(BaseSchema):
    items: List[InstitutionListResponse]
    total: int
    page: int
    size: int
