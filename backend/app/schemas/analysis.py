"""Analysis schemas."""
from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.patent import PatentMatch


class ExtractedClaims(BaseModel):
    """Extracted claims schema."""

    background: str = Field(default="Technical disclosure provided")
    innovations: List[str] = Field(default_factory=list)
    technicalSpecs: Dict[str, str] = Field(default_factory=dict)
    keywords: List[str] = Field(default_factory=list)
    ipcClassifications: List[str] = Field(default_factory=list)


class DisclosureInfo(BaseModel):
    """Disclosure information schema."""

    filename: str
    uploadedAt: datetime


class PatentabilityAssessment(BaseModel):
    """Patentability assessment schema (NEW in v2.1)."""

    isPatentable: bool
    confidence: float  # 0-100
    missingElements: List[str]
    recommendations: List[str]


class AnalysisCreate(BaseModel):
    """Schema for creating an analysis."""

    title: Optional[str] = None


class AnalysisResponse(BaseModel):
    """Analysis response schema."""

    id: str  # UUID
    title: str
    status: str  # processing, completed, failed
    disclosure: DisclosureInfo
    extractedClaims: Optional[ExtractedClaims] = None
    patents: Optional[List[PatentMatch]] = None
    noveltyScore: Optional[float] = None
    recommendation: Optional[str] = None  # pursue, reconsider, reject
    reasoning: Optional[str] = None

    # Patentability assessment (NEW in v2.1)
    patentabilityAssessment: Optional[PatentabilityAssessment] = None

    createdAt: datetime
    updatedAt: Optional[datetime] = None
    completedAt: Optional[datetime] = None

    class Config:
        from_attributes = True


class AnalysisListResponse(BaseModel):
    """List of analyses with pagination."""

    data: List[AnalysisResponse]
    total: int
    page: int
    limit: int
    pages: int
