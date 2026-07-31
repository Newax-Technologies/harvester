import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.api.dependencies import User, get_current_user, get_db_session
from lead_harvester.models.signal import SignalType
from lead_harvester.schemas.entities import PersonCandidateResponse, SignalResponse
from lead_harvester.services.person_candidate_service import list_person_candidates
from lead_harvester.services.signal_service import list_signals

router = APIRouter(prefix="/entities", tags=["Entity Registry"])


@router.get("/person-candidates", response_model=list[PersonCandidateResponse])
async def list_person_candidates_route(
    institution_id: uuid.UUID | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    candidates = await list_person_candidates(session, institution_id=institution_id, limit=limit)
    return [PersonCandidateResponse.model_validate(c) for c in candidates]


@router.get("/signals", response_model=list[SignalResponse])
async def list_signals_route(
    institution_id: uuid.UUID | None = Query(None),
    signal_type: SignalType | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    signals = await list_signals(
        session, institution_id=institution_id, signal_type=signal_type, limit=limit
    )
    return [SignalResponse.model_validate(s) for s in signals]
