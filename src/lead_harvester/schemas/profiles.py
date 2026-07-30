from datetime import datetime
from uuid import UUID

from lead_harvester.models.qualification import QualificationStatus
from lead_harvester.schemas.common import BaseSchema


class LeadProfileResponse(BaseSchema):
    id: UUID
    institution_id: UUID
    overall_score: int
    score_breakdown: dict[str, int]
    has_phone: bool
    has_email: bool
    has_named_contact: bool
    qualification_status: QualificationStatus | None = None
    organization_summary: str
    evidence_count: int
    computed_at: datetime


class LeadProfileListItem(LeadProfileResponse):
    canonical_name: str


class PaginatedLeadProfiles(BaseSchema):
    items: list[LeadProfileListItem]
    total: int
    page: int
    size: int


class LeadScoreHistoryPoint(BaseSchema):
    overall_score: int
    score_breakdown: dict[str, int]
    computed_at: datetime
