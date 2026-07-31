import uuid

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from lead_harvester.api.dependencies import get_current_user
from lead_harvester.api.errors import BaseAPIException
from lead_harvester.api.routes import (
    compliance,
    daily_selection,
    dashboard,
    drafts,
    entities,
    exports,
    institutions,
    lead_profiles,
    manual_leads,
    operations,
    outbox,
    resolution_reviews,
    verification,
)

app = FastAPI(
    title="Lead Harvester API",
    description="Backend API for the Lead Harvester Dashboard",
    version="1.0.0",
)

from fastapi.responses import RedirectResponse


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(BaseAPIException)
async def custom_api_exception_handler(request: Request, exc: BaseAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
                "request_id": exc.request_id,
            }
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_error",
                "message": "An unexpected error occurred.",
                "details": {},
                "request_id": f"req_{uuid.uuid4().hex[:12]}",
            }
        },
    )


@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}


# Global router for all /api/v1 endpoints requiring authentication
api_router = APIRouter(
    prefix="/api/v1",
    dependencies=[Depends(get_current_user)],
)

api_router.include_router(dashboard.router)
api_router.include_router(institutions.router)
api_router.include_router(drafts.router)
api_router.include_router(resolution_reviews.router)
api_router.include_router(manual_leads.router)
api_router.include_router(lead_profiles.router)
api_router.include_router(daily_selection.router)
api_router.include_router(verification.router)
api_router.include_router(compliance.router)
api_router.include_router(outbox.router)
api_router.include_router(exports.router)
api_router.include_router(operations.router)
api_router.include_router(entities.router)

app.include_router(api_router)
