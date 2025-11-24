"""Analysis model."""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Analysis(Base):
    """Analysis database model."""

    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False, default="processing")  # processing, completed, failed
    disclosure_filename = Column(String(255), nullable=False)
    disclosure_path = Column(String(512), nullable=False)
    extracted_claims = Column(Text, nullable=True)  # JSON
    novelty_score = Column(Float, nullable=True)  # 0-100
    recommendation = Column(String(20), nullable=True)  # pursue, reconsider, reject
    reasoning = Column(Text, nullable=True)

    # Patentability assessment fields (NEW in v2.1)
    is_patentable = Column(Boolean, nullable=True)
    patentability_confidence = Column(Float, nullable=True)  # 0-100
    missing_elements = Column(Text, nullable=True)  # JSON array

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    patents = relationship("Patent", back_populates="analysis", cascade="all, delete-orphan")
    orchestrate_logs = relationship("OrchestrateLog", back_populates="analysis", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.uuid,
            "title": self.title,
            "status": self.status,
            "disclosure": {
                "filename": self.disclosure_filename,
                "uploadedAt": self.created_at.isoformat() if self.created_at else None
            },
            "extractedClaims": self.extracted_claims,
            "noveltyScore": self.novelty_score,
            "recommendation": self.recommendation,
            "reasoning": self.reasoning,
            "isPatentable": self.is_patentable,
            "patentabilityConfidence": self.patentability_confidence,
            "missingElements": self.missing_elements,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
            "completedAt": self.completed_at.isoformat() if self.completed_at else None,
        }
