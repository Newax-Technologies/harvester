from datetime import datetime
from uuid import UUID

from lead_harvester.models.outreach import BriefStatus, DraftStatus
from lead_harvester.schemas.common import BaseSchema


class AccountBriefSchema(BaseSchema):
    id: UUID
    institution_id: UUID
    status: BriefStatus
    value_hypotheses: list[str]
    stakeholder_ranking: list[dict]
    executive_summary: str
    created_at: datetime
    updated_at: datetime


class OutreachDraftSchema(BaseSchema):
    id: UUID
    brief_id: UUID
    status: DraftStatus
    target_name: str
    target_role: str
    target_contact_value: str
    subject_line: str
    body: str
    human_feedback: str
    version: int
    created_at: datetime
    updated_at: datetime


class DraftEditRequest(BaseSchema):
    message: str
    expected_version: int


class DraftDecisionRequest(BaseSchema):
    decision: str  # e.g., 'approved', 'rejected'
    feedback: str
    expected_version: int
