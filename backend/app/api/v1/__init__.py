"""API v1 package."""
from fastapi import APIRouter
from app.api.v1 import analyses, health, skills

api_router = APIRouter()

# Include routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(analyses.router, prefix="/analyses", tags=["analyses"])
api_router.include_router(skills.router, tags=["Orchestrate Skills"])
