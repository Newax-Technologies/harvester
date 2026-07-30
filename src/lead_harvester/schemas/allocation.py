from datetime import datetime
from uuid import UUID

from lead_harvester.models.allocation import ReservationStatus
from lead_harvester.schemas.common import BaseSchema


class LeadReservationResponse(BaseSchema):
    id: UUID
    institution_id: UUID
    status: ReservationStatus
    score_at_reservation: int
    batch_label: str
    reserved_at: datetime
    expires_at: datetime
    consumed_at: datetime | None = None
    released_at: datetime | None = None


class LeadReservationListItem(LeadReservationResponse):
    canonical_name: str


class SelectDailyBatchRequest(BaseSchema):
    limit: int | None = None
    ttl_hours: float | None = None
    min_score: int | None = None
    batch_label: str | None = None
