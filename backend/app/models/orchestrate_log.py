"""Orchestrate log model."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class OrchestrateLog(Base):
    """Orchestrate log database model."""

    __tablename__ = "orchestrate_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default="started")  # started, completed, failed
    input_data = Column(Text, nullable=True)  # JSON
    output_data = Column(Text, nullable=True)  # JSON
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # watsonx Orchestrate integration fields (v3.1)
    orchestrate_execution_id = Column(String(255), nullable=True, index=True)  # Orchestrate workflow execution ID
    workflow_name = Column(String(100), nullable=True, default='patent-analysis-workflow')  # Workflow identifier

    # Relationships
    analysis = relationship("Analysis", back_populates="orchestrate_logs")

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "analysisId": self.analysis_id,
            "skillName": self.skill_name,
            "status": self.status,
            "inputData": self.input_data,
            "outputData": self.output_data,
            "errorMessage": self.error_message,
            "startedAt": self.started_at.isoformat() if self.started_at else None,
            "completedAt": self.completed_at.isoformat() if self.completed_at else None,
            "orchestrateExecutionId": self.orchestrate_execution_id,
            "workflowName": self.workflow_name,
        }
