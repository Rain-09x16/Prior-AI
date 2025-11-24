"""Health check endpoints."""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Auto-Prior Art Analyst API",
        "version": "1.0.0"
    }


@router.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Auto-Prior Art Analyst API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
