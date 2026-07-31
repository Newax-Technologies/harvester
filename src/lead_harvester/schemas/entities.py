from datetime import datetime
from uuid import UUID

from lead_harvester.models.person import PersonCandidateStatus
from lead_harvester.models.signal import SignalType
from lead_harvester.schemas.common import BaseSchema


class PersonCandidateResponse(BaseSchema):
    id: UUID
    institution_id: UUID
    display_name: str
    normalized_name: str
    status: PersonCandidateStatus
    evidence_count: int
    first_seen_at: datetime
    last_seen_at: datetime


class SignalResponse(BaseSchema):
    id: UUID
    institution_id: UUID
    signal_type: SignalType
    signal_text: str
    source_url: str
    confidence_score: float
    detected_at: datetime
