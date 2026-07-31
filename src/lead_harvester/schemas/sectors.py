from uuid import UUID

from pydantic import Field

from lead_harvester.schemas.common import BaseSchema


class SectorResponse(BaseSchema):
    id: UUID
    code: str
    display_name: str
    institution_types: list[str]
    icp_criteria: dict
    qualification_rules: dict


class CreateSectorRequest(BaseSchema):
    code: str = Field(..., min_length=1, max_length=50)
    display_name: str = Field(..., min_length=1, max_length=100)
    institution_types: list[str] = Field(default_factory=list)
    icp_criteria: dict = Field(default_factory=dict)
    qualification_rules: dict = Field(default_factory=dict)


class UpdateSectorRequest(BaseSchema):
    display_name: str | None = Field(default=None, min_length=1, max_length=100)
    institution_types: list[str] | None = None
    icp_criteria: dict | None = None
    qualification_rules: dict | None = None
