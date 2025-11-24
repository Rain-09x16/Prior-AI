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

TO USE THIS VERSION:
1. Complete Orchestrate setup (see ORCHESTRATE_SETUP.md)
2. Rename this file to orchestrate.py (backup current one first)
3. Restart backend server

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

    async def run_analysis(self, analysis_id: int, document_text: str) -> Dict:
        """
        Run the complete analysis workflow via watsonx Orchestrate.

        NEW WORKFLOW (v3.1 with Orchestrate):
        1. Call watsonx Orchestrate API with document text and analysis ID
        2. Orchestrate executes the patent-analysis-workflow which:
           a. Calls /skills/patentability-checker
           b. If patentable, calls /skills/claim-extractor
           c. Calls /skills/patent-searcher
           d. Calls /skills/similarity-scorer
           e. Aggregates and returns results
        3. Log execution to orchestrate_logs with execution ID
        4. Save results to database
        5. Return results

        FALLBACK: If Orchestrate is not configured, falls back to direct
        service calls (for development/testing).

        Args:
            analysis_id: Database ID of the analysis
            document_text: Parsed document text

        Returns:
            Dictionary with analysis results
        """
        logger.info(f"Starting analysis workflow for analysis_id={analysis_id}")

        # Check if Orchestrate is configured
        if not self.orchestrate_client.is_configured():
            logger.warning("watsonx Orchestrate not configured - falling back to direct service calls")
            return await self._run_analysis_fallback(analysis_id, document_text)

        try:
            # Prepare input data for Orchestrate workflow
            input_data = {
                "documentText": document_text,
                "analysisId": analysis_id,
                "options": {
                    "maxPatents": 100,
                    "minSimilarity": 0.7
                }
            }

            # Log workflow start
            workflow_log = OrchestrateLog(
                analysis_id=analysis_id,
                skill_name="orchestrate_workflow",
                status="started",
                workflow_name="patent-analysis-workflow",
                input_data=json.dumps({"documentLength": len(document_text)}),
                started_at=datetime.utcnow()
            )
            self.db.add(workflow_log)
            self.db.commit()

            logger.info("Calling watsonx Orchestrate API to execute workflow")

            # Execute workflow via Orchestrate
            start_time = datetime.utcnow()
            orchestrate_response = self.orchestrate_client.execute_workflow(input_data)
            end_time = datetime.utcnow()

            # Extract execution ID and results
            execution_id = orchestrate_response.get("executionId")
            status = orchestrate_response.get("status", "unknown")
            results = orchestrate_response.get("results", {})

            logger.info(f"Orchestrate workflow execution_id={execution_id}, status={status}")

            # Update workflow log with execution ID and status
            workflow_log.orchestrate_execution_id = execution_id
            workflow_log.status = "completed" if status == "completed" else "running"
            workflow_log.completed_at = end_time if status == "completed" else None
            workflow_log.output_data = json.dumps({
                "executionId": execution_id,
                "status": status,
                "duration_seconds": (end_time - start_time).total_seconds()
            })
            self.db.commit()

            # Update analysis record with results
            analysis = self.db.query(Analysis).filter(Analysis.id == analysis_id).first()
            if analysis and results:
                self._update_analysis_from_results(analysis, results, execution_id)
                self.db.commit()

            # Return results with execution ID
            return {
                **results,
                "orchestrateExecutionId": execution_id,
                "workflowStatus": status
            }

        except Exception as e:
            logger.error(f"Orchestrate workflow failed: {str(e)}")
            self._log_error(analysis_id, str(e))

            # Try fallback to direct service calls
            logger.warning("Falling back to direct service calls after Orchestrate failure")
            return await self._run_analysis_fallback(analysis_id, document_text)

    def _update_analysis_from_results(self, analysis: Analysis, results: Dict, execution_id: str):
        """
        Update Analysis record from Orchestrate workflow results.

        Args:
            analysis: Analysis database record
            results: Results from Orchestrate workflow
            execution_id: Orchestrate execution ID
        """
        # Extract patentability assessment
        patentability = results.get("patentabilityAssessment", {})
        analysis.is_patentable = patentability.get("isPatentable", True)
        analysis.patentability_confidence = patentability.get("confidence", 50)
        analysis.missing_elements = json.dumps(patentability.get("missingElements", []))

        # If not patentable, mark as rejected
        if not analysis.is_patentable:
            analysis.status = "completed"
            analysis.recommendation = "reject"
            analysis.reasoning = "Disclosure appears to be publishable research but not patentable. See patentability assessment for details."
            analysis.novelty_score = 0.0
            analysis.completed_at = datetime.utcnow()
            logger.info(f"Analysis {analysis.id} marked as not patentable")
            return

        # Extract recommendation
        analysis.novelty_score = results.get("noveltyScore", 0)
        analysis.recommendation = results.get("recommendation", "pending")
        analysis.reasoning = results.get("reasoning", "")
        analysis.status = "completed"
        analysis.completed_at = datetime.utcnow()

        logger.info(f"Analysis {analysis.id} updated: {analysis.recommendation} (novelty={analysis.novelty_score})")

    async def _run_analysis_fallback(self, analysis_id: int, document_text: str) -> Dict:
        """
        Fallback: Run analysis using direct service calls (no Orchestrate).

        This is used when Orchestrate is not configured or fails. It directly
        calls the ML services instead of going through Orchestrate.

        NOTE: This is for development/testing only. Production should use Orchestrate.
        """
        logger.info("Running analysis with fallback method (direct service calls)")

        # Import services for fallback
        from app.ml_services.claim_extractor import ClaimExtractor
        from app.ml_services.similarity_scorer import SimilarityScorer
        from app.services.patent_searcher import PatentSearcher
        from app.ml_services.recommender import RecommendationGenerator

        claim_extractor = ClaimExtractor()
        similarity_scorer = SimilarityScorer()
        patent_searcher = PatentSearcher()
        recommender = RecommendationGenerator()

        try:
            # Step 0: Assess Patentability
            logger.info("Fallback: Assessing patentability")
            patentability = await self._run_skill(
                analysis_id,
                "assess_patentability",
                lambda: claim_extractor.assess_patentability(document_text)
            )

            # Save patentability to database
            analysis = self.db.query(Analysis).filter(Analysis.id == analysis_id).first()
            if analysis:
                analysis.is_patentable = patentability.get("isPatentable")
                analysis.patentability_confidence = patentability.get("confidence")
                analysis.missing_elements = json.dumps(patentability.get("missingElements", []))
                self.db.commit()

            # If not patentable, stop here
            if not patentability.get("isPatentable"):
                logger.warning("Fallback: Not patentable - stopping analysis")
                if analysis:
                    analysis.status = "completed"
                    analysis.recommendation = "reject"
                    analysis.reasoning = "Disclosure appears to be publishable research but not patentable."
                    analysis.novelty_score = 0.0
                    analysis.completed_at = datetime.utcnow()
                    self.db.commit()

                return {
                    "patentabilityAssessment": patentability,
                    "warning": "Disclosure appears to be publishable but not patentable",
                    "skipPriorArt": True,
                    "recommendation": "reject"
                }

            # Step 1: Extract Claims
            logger.info("Fallback: Extracting claims")
            claims = await self._run_skill(
                analysis_id,
                "extract_claims",
                lambda: claim_extractor.extract(document_text)
            )

            # Step 2: Search Patents
            logger.info("Fallback: Searching patents")
            patents = await self._run_skill(
                analysis_id,
                "search_patents",
                lambda: patent_searcher.search(
                    keywords=claims.get("keywords", []),
                    ipc_codes=claims.get("ipcClassifications", []),
                    max_results=100
                )
            )

            # Step 3: Score Similarity
            logger.info("Fallback: Scoring similarity")
            scored_patents = await self._run_skill(
                analysis_id,
                "score_similarity",
                lambda: similarity_scorer.score_multiple_patents(claims, patents)
            )

            # Step 4: Generate Recommendation
            logger.info("Fallback: Generating recommendation")
            recommendation = await self._run_skill(
                analysis_id,
                "generate_recommendation",
                lambda: recommender.generate(claims, scored_patents)
            )

            # Return results
            return {
                "patentabilityAssessment": patentability,
                "extractedClaims": claims,
                "patents": scored_patents[:20],
                "noveltyScore": recommendation.get("noveltyScore"),
                "recommendation": recommendation.get("recommendation"),
                "reasoning": recommendation.get("reasoning"),
                "suggestedClaimFocus": recommendation.get("suggestedClaimFocus", [])
            }

        except Exception as e:
            logger.error(f"Fallback analysis failed: {str(e)}")
            self._log_error(analysis_id, str(e))
            raise

    async def _run_skill(self, analysis_id: int, skill_name: str, skill_function):
        """
        Execute a skill and log to orchestrate_logs table.

        Used by fallback method to track individual skill executions.

        Args:
            analysis_id: Database ID of the analysis
            skill_name: Name of the skill being executed
            skill_function: Lambda/function to execute

        Returns:
            Result from skill_function
        """
        logger.info(f"Executing skill: {skill_name}")

        # Create orchestration log entry
        log = OrchestrateLog(
            analysis_id=analysis_id,
            skill_name=skill_name,
            status="started",
            started_at=datetime.utcnow()
        )
        self.db.add(log)
        self.db.commit()

        try:
            # Execute the skill
            start_time = datetime.utcnow()
            result = skill_function()
            end_time = datetime.utcnow()

            # Update log with success
            log.status = "completed"
            log.completed_at = end_time
            log.output_data = json.dumps(
                {"status": "success", "duration_seconds": (end_time - start_time).total_seconds()},
                default=str
            )
            self.db.commit()

            logger.info(f"Skill {skill_name} completed successfully")
            return result

        except Exception as e:
            # Update log with failure
            log.status = "failed"
            log.completed_at = datetime.utcnow()
            log.error_message = str(e)
            self.db.commit()

            logger.error(f"Skill {skill_name} failed: {str(e)}")
            raise

    def _log_error(self, analysis_id: int, error_message: str):
        """Log error to orchestrate_logs."""
        try:
            log = OrchestrateLog(
                analysis_id=analysis_id,
                skill_name="workflow_error",
                status="failed",
                error_message=error_message,
                started_at=datetime.utcnow(),
                completed_at=datetime.utcnow()
            )
            self.db.add(log)
            self.db.commit()
        except Exception as e:
            logger.error(f"Failed to log error: {str(e)}")
