from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional

from lead_harvester.api.dependencies import get_db_session, get_current_user, User
from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.services.institution_service import InstitutionService
from lead_harvester.schemas.institutions import PaginatedInstitutions, InstitutionDetailResponse

router = APIRouter(prefix="/institutions", tags=["Institutions"])

@router.get("", response_model=PaginatedInstitutions)
async def list_institutions(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    city: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """List institutions with pagination and filtering."""
    return await InstitutionService.get_institutions(session, limit, offset, city)

@router.get("/{institution_id}", response_model=InstitutionDetailResponse)
async def get_institution(
    institution_id: str = Path(...),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """Get the full dossier for a specific institution."""
    institution = await InstitutionService.get_institution_detail(session, institution_id)
    if not institution:
        raise ResourceNotFoundError("Institution not found")
    return InstitutionDetailResponse.model_validate(institution)
