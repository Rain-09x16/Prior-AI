"""Patent model."""
from sqlalchemy import Column, Integer, String, Text, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Patent(Base):
    """Patent database model."""

    __tablename__ = "patents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False, index=True)
    patent_id = Column(String(50), nullable=False)  # US10234567B2
    title = Column(String(512), nullable=False)
    abstract = Column(Text, nullable=True)
    claims = Column(Text, nullable=True)  # JSON array
    publication_date = Column(Date, nullable=True)
    assignee = Column(String(255), nullable=True)
    inventors = Column(Text, nullable=True)  # JSON array
    ipc_classifications = Column(Text, nullable=True)  # JSON array
    similarity_score = Column(Float, nullable=False, default=0.0)  # 0-100
    overlapping_concepts = Column(Text, nullable=True)  # JSON array
    key_differences = Column(Text, nullable=True)  # JSON array
    source = Column(String(20), nullable=False, default="google")  # google, espacenet

    # Relationships
    analysis = relationship("Analysis", back_populates="patents")

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "patentId": self.patent_id,
            "title": self.title,
            "abstract": self.abstract,
            "claims": self.claims,
            "publicationDate": self.publication_date.isoformat() if self.publication_date else None,
            "assignee": self.assignee,
            "inventors": self.inventors,
            "ipcClassifications": self.ipc_classifications,
            "similarityScore": self.similarity_score,
            "overlappingConcepts": self.overlapping_concepts,
            "keyDifferences": self.key_differences,
            "source": self.source,
        }
