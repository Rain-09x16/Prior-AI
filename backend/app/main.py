"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.api.v1 import api_router
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting Auto-Prior Art Analyst API...")
    logger.info(f"Initializing database...")
    init_db()
    logger.info("Database initialized successfully")
    yield
    # Shutdown
    logger.info("Shutting down Auto-Prior Art Analyst API...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered patent prior art analysis for Technology Transfer Offices",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Mount static files for reports
app.mount(
    "/reports",
    StaticFiles(directory=str(settings.REPORTS_DIR)),
    name="reports"
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Auto-Prior Art Analyst API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "api": settings.API_V1_PREFIX
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
