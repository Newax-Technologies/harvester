from datetime import datetime
from uuid import UUID
from typing import Any, List, Optional
from pydantic import Field
from lead_harvester.models.resolution import MatchDecision
from lead_harvester.schemas.common import BaseSchema

class MatchAssessmentSchema(BaseSchema):
    id: UUID
    name_similarity: float
    distance_meters: Optional[float] = None
    phone_match: bool
    domain_match: bool
    total_score: float
    decision: MatchDecision
    assessed_at: datetime

class ResolutionCandidateSchema(BaseSchema):
    id: UUID
    raw_record_id: UUID
    target_canonical_id: Optional[UUID] = None
    target_raw_record_id: Optional[UUID] = None
    blocking_strategy: str
    version: int
    created_at: datetime
    assessments: List[MatchAssessmentSchema] = []

class ResolutionDecisionRequest(BaseSchema):
    decision: str  # e.g., 'same_business', 'same_branch', 'keep_separate'
    feedback: str
    expected_version: int
