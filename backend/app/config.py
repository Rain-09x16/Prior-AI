"""
Application configuration settings.
"""
import os
from pathlib import Path
from typing import Optional, Union
from pydantic import field_validator, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    model_config = ConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    # App
    APP_NAME: str = "Auto-Prior Art Analyst"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: Union[list[str], str] = ["http://localhost:3000", "http://localhost:3001"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            if not v:
                return ["http://localhost:3000", "http://localhost:3001"]
            return [origin.strip() for origin in v.split(",")]
        return v

    # Database
    DATABASE_URL: str = "sqlite:///./priorai.db"

    # File Storage
    BASE_DIR: Path = Path(__file__).parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    DISCLOSURES_DIR: Path = UPLOAD_DIR / "disclosures"
    REPORTS_DIR: Path = UPLOAD_DIR / "reports"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: Union[list[str], str] = [".pdf", ".docx"]

    @field_validator("ALLOWED_EXTENSIONS", mode="before")
    @classmethod
    def parse_allowed_extensions(cls, v):
        if isinstance(v, str):
            if not v:
                return [".pdf", ".docx"]
            return [ext.strip() for ext in v.split(",")]
        return v

    # watsonx (for AI/ML developer)
    WATSONX_API_KEY: Optional[str] = os.getenv("WATSONX_API_KEY")
    WATSONX_NLU_URL: Optional[str] = os.getenv("WATSONX_NLU_URL")
    WATSONX_URL: Optional[str] = os.getenv("WATSONX_URL")
    WATSONX_PROJECT_ID: Optional[str] = os.getenv("WATSONX_PROJECT_ID")

    # Patent APIs
    GOOGLE_PATENTS_API_KEY: Optional[str] = os.getenv("GOOGLE_PATENTS_API_KEY")

    # Clerk Authentication
    NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: Optional[str] = os.getenv("NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY")
    CLERK_SECRET_KEY: Optional[str] = os.getenv("CLERK_SECRET_KEY")


# Global settings instance
settings = Settings()

# Ensure directories exist
settings.DISCLOSURES_DIR.mkdir(parents=True, exist_ok=True)
settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
