"""
Orchestration Conductor - watsonx Orchestrate Integration (v3.1)

MAJOR CHANGE: This conductor now calls watsonx Orchestrate API instead of
calling ML functions directly.

NEW FLOW:
1. Backend calls watsonx Orchestrate API (via WatsonxOrchestrateClient)
2. Orchestrate executes the patent-analysis-workflow
3. Orchestrate calls our skill endpoints (/skills/*)
4. Our skills call watsonx NLU/AI services
5. Orchestrate aggregates and returns results
6. Backend saves results to database

This architecture demonstrates watsonx Orchestrate workflow orchestration
for the hackathon judges.
"""
from typing import Dict
import json
from datetime import datetime
from sqlalchemy.orm import Session

# Import Orchestrate client
from app.integrations.watsonx_orchestrate import WatsonxOrchestrateClient

# Import database models
from app.models import Analysis, OrchestrateLog

# Import logger
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class OrchestrateConductor:
    """
    Orchestrate the full prior art analysis workflow via watsonx Orchestrate.

    This class is the main integration point with watsonx Orchestrate.
    Instead of directly calling ML services, it delegates to Orchestrate
    which coordinates the workflow execution.
    """

    def __init__(self, db_session: Session):
        """
        Initialize the orchestration conductor.

        Args:
            db_session: Database session for logging and storing results
        """
        self.db = db_session
        self.orchestrate_client = WatsonxOrchestrateClient()

        # Check if Orchestrate is configured
        if self.orchestrate_client.is_configured():
            logger.info("Orchestration Conductor initialized with watsonx Orchestrate integration")
        else:
            logger.warning("Orchestration Conductor initialized WITHOUT watsonx Orchestrate (not configured)")
            logger.warning("Set WATSONX_ORCHESTRATE_API_KEY and WATSONX_ORCHESTRATE_TEAM_ID to enable Orchestrate")
