"""
Orchestration Conductor - Main workflow coordinator.

This is the INTEGRATION POINT between fullstack and AI/ML code.
It orchestrates the complete analysis workflow by calling:
1. Document Parser (fullstack)
2. Claim Extractor (AI/ML)
3. Patent Searcher (fullstack)
4. Similarity Scorer (AI/ML)
5. Recommendation Generator (AI/ML)

HACKATHON MODE: Now supports watsonx Orchestrate for multi-agent coordination!
"""
from typing import Dict
import json
import os
from datetime import datetime
from sqlalchemy.orm import Session

# Import fullstack services
from app.services.patent_searcher import PatentSearcher
from app.models import Analysis, Patent, OrchestrateLog

# Import AI/ML services (stubs for now, AI/ML dev will implement)
from app.ml_services.claim_extractor import ClaimExtractor
from app.ml_services.similarity_scorer import SimilarityScorer
from app.ml_services.recommender import RecommendationGenerator

# Import watsonx Orchestrate client for multi-agent coordination
from app.integrations.watsonx_orchestrate import WatsonxOrchestrateClient

from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class OrchestrateConductor:
    """
    Orchestrate the full prior art analysis workflow.

    This class coordinates between fullstack and AI/ML components.
    """

    def __init__(self, db_session: Session):
        """
        Initialize the orchestration conductor.

        Args:
            db_session: Database session for logging and storing results
        """
        self.db = db_session

        # Initialize watsonx Orchestrate client (HACKATHON REQUIREMENT!)
        logger.info("Initializing watsonx Orchestrate client...")
        self.orchestrate_client = WatsonxOrchestrateClient()

        # Check if Orchestrate is enabled (use environment variable to toggle)
        self.use_orchestrate = os.getenv('USE_WATSONX_ORCHESTRATE', 'true').lower() == 'true'
        if self.use_orchestrate and self.orchestrate_client.is_configured():
            logger.info("watsonx Orchestrate ENABLED - will use multi-agent orchestration")
        else:
            logger.info("watsonx Orchestrate disabled - using direct service calls")

        # Initialize AI/ML services (AI/ML developer implements these)
        logger.info("Initializing AI/ML services...")
        self.claim_extractor = ClaimExtractor()
        self.similarity_scorer = SimilarityScorer()
        self.recommender = RecommendationGenerator()

        # Initialize fullstack services
        logger.info("Initializing fullstack services...")
        self.patent_searcher = PatentSearcher()

        logger.info("Orchestration Conductor initialized")

    async def run_analysis(self, analysis_id: int, document_text: str) -> Dict:
        """
        Run the complete analysis workflow.

        HACKATHON MODE: If watsonx Orchestrate is enabled, use multi-agent orchestration!
        Otherwise, use direct service calls.

        ORCHESTRATE WORKFLOW (v3.0 - HACKATHON):
        - watsonx Orchestrate coordinates all 4 agents:
          1. Claim Extractor agent
          2. Patent Searcher agent
          3. Novelty Scorer agent
          4. Compliance Validator agent

        CLASSIC WORKFLOW (v2.1):
        0. Assess Patentability (AI/ML) - NEW STEP
           - If NOT patentable: Return early with recommendations, skip expensive search
           - If patentable: Continue with normal flow
        1. Extract claims from document (AI/ML)
        2. Search for patents (Fullstack)
        3. Score patent similarity (AI/ML)
        4. Generate recommendation (AI/ML)
        5. Return results

        Args:
            analysis_id: Database ID of the analysis
            document_text: Parsed document text

        Returns:
            Dictionary with analysis results
        """
        logger.info(f"Starting analysis workflow for analysis_id={analysis_id}")

        # HACKATHON MODE: Use watsonx Orchestrate if enabled
        if self.use_orchestrate and self.orchestrate_client.is_configured():
            logger.info("🚀 HACKATHON MODE: Using watsonx Orchestrate multi-agent workflow!")
            return await self._run_orchestrate_workflow(analysis_id, document_text)

        # CLASSIC MODE: Direct service calls
        logger.info("Using classic direct service calls workflow")

        try:
            # NEW STEP 0: Assess Patentability (v2.1)
            logger.info("Step 0 (NEW): Assessing patentability...")
            patentability = await self._run_skill(
                analysis_id,
                "assess_patentability",
                lambda: self.claim_extractor.assess_patentability(document_text)
            )
            logger.info(f"Patentability: {patentability.get('isPatentable')} (confidence: {patentability.get('confidence')}%)")

            # Save patentability results to database
            analysis = self.db.query(Analysis).filter(Analysis.id == analysis_id).first()
            if analysis:
                analysis.is_patentable = patentability.get('isPatentable')
                analysis.patentability_confidence = patentability.get('confidence')
                analysis.missing_elements = json.dumps(patentability.get('missingElements', []))
                self.db.commit()
                logger.info("Saved patentability assessment to database")

            # If NOT patentable, stop here and return warning (save costs!)
            if not patentability.get('isPatentable'):
                logger.warning("Disclosure is NOT patentable - stopping analysis to save costs")

                if analysis:
                    analysis.status = 'completed'
                    analysis.reasoning = "Disclosure appears to be publishable research but not patentable. See patentability assessment for details."
                    analysis.recommendation = 'reject'
                    analysis.novelty_score = 0.0
                    analysis.completed_at = datetime.utcnow()
                    self.db.commit()

                return {
                    'patentabilityAssessment': patentability,
                    'warning': 'Disclosure appears to be publishable but not patentable',
                    'skipPriorArt': True,
                    'recommendation': 'reject',
                    'reasoning': 'Based on patentability assessment, this disclosure lacks key elements required for a patent. Consider revising the disclosure or publishing as research instead.'
                }

            # PATENTABLE - Continue with normal workflow
            logger.info("Disclosure is patentable - proceeding with prior art search")

            # Step 1: Extract Claims (AI/ML)
            logger.info("Step 1: Extracting claims from disclosure...")
            claims = await self._run_skill(
                analysis_id,
                "extract_claims",
                lambda: self.claim_extractor.extract(document_text)
            )
            logger.info(f"Extracted {len(claims.get('keywords', []))} keywords and {len(claims.get('innovations', []))} innovations")

            # Step 2: Search Patents (Fullstack)
            logger.info("Step 2: Searching patent database...")
            patents = await self._run_skill(
                analysis_id,
                "search_patents",
                lambda: self.patent_searcher.search(
                    keywords=claims.get('keywords', []),
                    ipc_codes=claims.get('ipcClassifications', []),
                    max_results=100
                )
            )
            logger.info(f"Found {len(patents)} patents")

            # Step 3: Score Similarity (AI/ML)
            logger.info("Step 3: Scoring patent similarity...")
            scored_patents = await self._run_skill(
                analysis_id,
                "score_similarity",
                lambda: self.similarity_scorer.score_multiple_patents(claims, patents)
            )
            logger.info(f"Scored {len(scored_patents)} patents")

            # Step 4: Generate Recommendation (AI/ML)
            logger.info("Step 4: Generating recommendation...")
            recommendation = await self._run_skill(
                analysis_id,
                "generate_recommendation",
                lambda: self.recommender.generate(claims, scored_patents)
            )
            logger.info(f"Recommendation: {recommendation.get('recommendation')} (novelty: {recommendation.get('noveltyScore')})")

            # Compile final results (including patentability assessment)
            results = {
                'patentabilityAssessment': patentability,
                'extractedClaims': claims,
                'patents': scored_patents[:20],  # Return top 20 patents
                'noveltyScore': recommendation.get('noveltyScore'),
                'recommendation': recommendation.get('recommendation'),
                'reasoning': recommendation.get('reasoning'),
                'suggestedClaimFocus': recommendation.get('suggestedClaimFocus', [])
            }

            logger.info(f"Analysis workflow completed for analysis_id={analysis_id}")
            return results

        except Exception as e:
            logger.error(f"Analysis workflow failed: {str(e)}")
            self._log_error(analysis_id, str(e))
            raise

    async def _run_skill(self, analysis_id: int, skill_name: str, skill_function):
        """
        Execute a skill and log to orchestrate_logs table.

        This method wraps each step of the workflow for tracking and debugging.

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

    async def _run_orchestrate_workflow(self, analysis_id: int, document_text: str) -> Dict:
        """
        Run analysis using watsonx Orchestrate multi-agent coordination.

        This is the HACKATHON MODE implementation that demonstrates
        watsonx Orchestrate orchestrating multiple AI agents.

        Args:
            analysis_id: Database ID of the analysis
            document_text: Parsed document text

        Returns:
            Dictionary with orchestrated analysis results
        """
        logger.info("=" * 80)
        logger.info("WATSONX ORCHESTRATE MULTI-AGENT WORKFLOW")
        logger.info("=" * 80)

        try:
            # Get analysis record
            analysis = self.db.query(Analysis).filter(Analysis.id == analysis_id).first()

            # Execute orchestration workflow
            logger.info("Invoking watsonx Orchestrate workflow...")
            orchestrate_result = self.orchestrate_client.execute_workflow(
                disclosure_text=document_text,
                disclosure_id=analysis_id,
                user_id=str(analysis.id) if analysis else None
            )

            logger.info(f"Orchestration completed with status: {orchestrate_result.get('status')}")
            logger.info(f"Agents executed: {orchestrate_result.get('agents_executed', [])}")

            # Extract results from orchestration
            claim_extraction = orchestrate_result.get('claim_extraction', {})
            patent_search = orchestrate_result.get('patent_search', {})
            novelty_scoring = orchestrate_result.get('novelty_scoring', {})
            compliance_validation = orchestrate_result.get('compliance_validation', {})

            # Update database with orchestration results
            if analysis:
                # Save patentability from compliance validation
                patentability_assessment = compliance_validation.get('patentability_assessment', {})
                analysis.is_patentable = patentability_assessment.get('is_patentable', True)
                analysis.patentability_confidence = patentability_assessment.get('confidence', 0)

                # Save claims
                analysis.extracted_claims = json.dumps(claim_extraction.get('claims', []))

                # Save novelty score
                analysis.novelty_score = novelty_scoring.get('overall_novelty_score', 0) / 100.0

                # Save recommendation
                is_patentable = patentability_assessment.get('is_patentable', True)
                novelty_score = novelty_scoring.get('overall_novelty_score', 0)

                if not is_patentable:
                    analysis.recommendation = 'reject'
                    analysis.reasoning = "Disclosure lacks patentable elements per USPTO requirements"
                elif novelty_score >= 70:
                    analysis.recommendation = 'proceed'
                    analysis.reasoning = "High novelty score indicates strong patentability"
                elif novelty_score >= 50:
                    analysis.recommendation = 'revise'
                    analysis.reasoning = "Moderate novelty - revision recommended to strengthen claims"
                else:
                    analysis.recommendation = 'reject'
                    analysis.reasoning = "Low novelty score due to significant prior art overlap"

                # Save status
                analysis.status = 'completed'
                analysis.completed_at = datetime.utcnow()

                self.db.commit()
                logger.info("Saved orchestration results to database")

            # Format response for frontend
            results = {
                'patentabilityAssessment': compliance_validation.get('patentability_assessment', {}),
                'extractedClaims': {
                    'keywords': claim_extraction.get('claims', [])[:5],  # Use first 5 claims as keywords
                    'innovations': claim_extraction.get('claims', []),
                    'technicalDetails': claim_extraction.get('technical_details', []),
                    'ipcClassifications': []
                },
                'patents': [
                    {
                        'patentNumber': p.get('patent_number'),
                        'title': p.get('title'),
                        'abstract': p.get('abstract', ''),
                        'similarity': p.get('similarity', 0),
                        'filingDate': p.get('filing_date'),
                        'assignee': p.get('assignee', ''),
                        'url': f"https://patents.google.com/patent/{p.get('patent_number')}"
                    }
                    for p in patent_search.get('top_patents', [])
                ],
                'noveltyScore': novelty_scoring.get('overall_novelty_score', 0) / 100.0,
                'recommendation': analysis.recommendation if analysis else 'proceed',
                'reasoning': analysis.reasoning if analysis else '',
                'suggestedClaimFocus': novelty_scoring.get('key_differentiators', []),
                'orchestration': {
                    'mode': 'watsonx_orchestrate',
                    'orchestration_id': orchestrate_result.get('orchestration_id'),
                    'agent_id': orchestrate_result.get('agent_id'),
                    'agents_executed': orchestrate_result.get('agents_executed', []),
                    'total_execution_time_ms': orchestrate_result.get('total_execution_time_ms', 0),
                    'is_stub': orchestrate_result.get('is_stub', False)
                }
            }

            logger.info("=" * 80)
            logger.info(f"✅ ORCHESTRATE WORKFLOW COMPLETED")
            logger.info(f"Recommendation: {results['recommendation']}")
            logger.info(f"Novelty Score: {results['noveltyScore'] * 100:.1f}%")
            logger.info("=" * 80)

            return results

        except Exception as e:
            logger.error(f"Orchestrate workflow failed: {str(e)}")
            self._log_error(analysis_id, f"Orchestrate workflow error: {str(e)}")
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
