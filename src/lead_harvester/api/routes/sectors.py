import uuid

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import get_db_session
from lead_harvester.api.errors import ResourceNotFoundError
from lead_harvester.api.permissions import Permission, require_permission
from lead_harvester.schemas.sectors import CreateSectorRequest, SectorResponse, UpdateSectorRequest
from lead_harvester.services.sector_service import (
    create_sector,
    get_sector,
    list_sectors,
    update_sector,
)

router = APIRouter(
    prefix="/sectors",
    tags=["Sectors"],
    dependencies=[Depends(require_permission(Permission.SECTORS_MANAGE))],
)


@router.get("", response_model=list[SectorResponse])
async def list_sectors_route(
    session: AsyncSession = Depends(get_db_session),
):
    sectors = await list_sectors(session)
    return [SectorResponse.model_validate(s) for s in sectors]


@router.get("/{sector_id}", response_model=SectorResponse)
async def get_sector_route(
    sector_id: uuid.UUID = Path(...),
    session: AsyncSession = Depends(get_db_session),
):
    sector = await get_sector(session, sector_id)
    if sector is None:
        raise ResourceNotFoundError(str(sector_id))
    return SectorResponse.model_validate(sector)


@router.post("", response_model=SectorResponse, status_code=201)
async def create_sector_route(
    payload: CreateSectorRequest,
    session: AsyncSession = Depends(get_db_session),
):
    try:
        sector = await create_sector(
            session,
            code=payload.code,
            display_name=payload.display_name,
            institution_types=payload.institution_types,
            icp_criteria=payload.icp_criteria,
            qualification_rules=payload.qualification_rules,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    await session.commit()
    return SectorResponse.model_validate(sector)


@router.patch("/{sector_id}", response_model=SectorResponse)
async def update_sector_route(
    payload: UpdateSectorRequest,
    sector_id: uuid.UUID = Path(...),
    session: AsyncSession = Depends(get_db_session),
):
    sector = await update_sector(
        session,
        sector_id,
        display_name=payload.display_name,
        institution_types=payload.institution_types,
        icp_criteria=payload.icp_criteria,
        qualification_rules=payload.qualification_rules,
    )
    await session.commit()
    return SectorResponse.model_validate(sector)
