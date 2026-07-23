from datetime import datetime
from uuid import UUID
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class AuditEventSchema(BaseSchema):
    id: UUID
    action: str
    actor: str
    entity_type: str
    entity_id: UUID
    timestamp: datetime
    feedback: Optional[str] = None
