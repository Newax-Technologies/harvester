from datetime import datetime
from typing import Any
from uuid import UUID

from lead_harvester.models.resolution import MatchDecision
from lead_harvester.schemas.common import BaseSchema


class MatchAssessmentSchema(BaseSchema):
    id: UUID
    name_similarity: float
    distance_meters: float | None = None
    phone_match: bool
    domain_match: bool
    total_score: float
    decision: MatchDecision
    assessed_at: datetime


class ResolutionCandidateSchema(BaseSchema):
    id: UUID
    raw_record_id: UUID
    target_canonical_id: UUID | None = None
    target_raw_record_id: UUID | None = None
    blocking_strategy: str
    version: int
    created_at: datetime
    assessments: list[MatchAssessmentSchema] = []
    # Derived, not direct ORM columns -- assembled by ResolutionService from
    # the candidate's best MatchAssessment and the source RawSourceRecord's
    # raw_payload (see canonical/merger.py::display_fields), since neither
    # lives on ResolutionCandidate itself.
    confidence_score: float = 0.0
    incoming_data: dict[str, Any] = {}


class ResolutionSummarySchema(BaseSchema):
    """Shape expected by frontend/src/pages/ResolutionQueue.tsx."""

    id: UUID
    candidateName: str
    targetName: str
    strategy: str
    score: float


class ResolutionDecisionRequest(BaseSchema):
    # One of "merge" (same branch -- enrich in place), "branch" (a distinct
    # physical location of the same institution), or "separate" (confidently
    # distinct entities) -- matches the buttons in
    # frontend/src/pages/ResolutionDetail.tsx ("Merge Entities", "Shared
    # Parent (Branches)", "Keep Separate").
    decision: str
    feedback: str
    expected_version: int
