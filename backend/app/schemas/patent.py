"""Patent schemas."""
from typing import Optional, List
from datetime import date
from pydantic import BaseModel


class PatentCreate(BaseModel):
    """Schema for creating a patent record."""

    analysis_id: int
    patent_id: str
    title: str
    abstract: Optional[str] = None
    claims: Optional[str] = None  # JSON array
    publication_date: Optional[date] = None
    assignee: Optional[str] = None
    inventors: Optional[str] = None  # JSON array
    ipc_classifications: Optional[str] = None  # JSON array
    similarity_score: float = 0.0
    overlapping_concepts: Optional[str] = None  # JSON array
    key_differences: Optional[str] = None  # JSON array
    source: str = "google"


class PatentMatch(BaseModel):
    """Patent match schema."""

    id: str
    patentId: str
    title: str
    abstract: Optional[str] = None
    claims: Optional[List[str]] = None
    publicationDate: Optional[str] = None
    assignee: Optional[str] = None
    inventors: Optional[List[str]] = None
    ipcClassifications: Optional[List[str]] = None
    similarityScore: float
    overlappingConcepts: Optional[List[str]] = None
    keyDifferences: Optional[List[str]] = None
    source: str

    class Config:
        from_attributes = True
