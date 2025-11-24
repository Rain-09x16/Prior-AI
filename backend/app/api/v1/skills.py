"""
watsonx Orchestrate Skill Endpoints

These endpoints are called BY watsonx Orchestrate during workflow execution.
Each skill endpoint:
1. Accepts input in Orchestrate format: {'input': {...}}
2. Calls the appropriate service (ML or fullstack)
3. Returns output in Orchestrate format: {'output': {...}}

HACKATHON REQUIREMENT: These skill endpoints must be registered in watsonx
Orchestrate for the workflow to execute. See ORCHESTRATE_SETUP.md for details.

Architecture Flow:
User -> Backend -> Orchestrate API -> Orchestrate Workflow -> These Skills -> Services

Skills:
1. patentability-checker: Assess if disclosure is patentable
2. claim-extractor: Extract claims, keywords, and IPC codes
3. patent-searcher: Search patent databases
4. similarity-scorer: Score similarity between disclosure and patents
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Dict
from pydantic import BaseModel
import traceback

# Import services
from app.ml_services.claim_extractor import ClaimExtractor
from app.ml_services.similarity_scorer import SimilarityScorer
from app.services.patent_searcher import PatentSearcher
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# Create router
router = APIRouter(
    prefix="/skills",
    tags=["Orchestrate Skills"]
)

# Initialize services (shared across all skill endpoints)
claim_extractor = ClaimExtractor()
similarity_scorer = SimilarityScorer()
patent_searcher = PatentSearcher()


# Pydantic models for request/response validation
class SkillInput(BaseModel):
    """Base model for skill input from Orchestrate."""
    input: Dict


class SkillOutput(BaseModel):
    """Base model for skill output to Orchestrate."""
    output: Dict


# ============================================================================
# SKILL 1: Patentability Checker
# ============================================================================

@router.post("/patentability-checker", response_model=SkillOutput)
async def patentability_checker_skill(data: SkillInput = Body(...)):
    """
    Skill: Assess Patentability

    Called by Orchestrate to determine if disclosure is patentable vs publishable.
    This is the FIRST skill in the workflow - if not patentable, workflow stops early.

    Input (from Orchestrate):
    {
        "input": {
            "documentText": "The full disclosure text...",
            "analysisId": 123  # Optional, for logging
        }
    }

    Output (to Orchestrate):
    {
        "output": {
            "isPatentable": true/false,
            "confidence": 0-100,
            "missingElements": ["element1", ...],
            "recommendations": ["recommendation1", ...]
        }
    }
    """
    logger.info("Skill: patentability-checker called by Orchestrate")

    try:
        # Extract input
        input_data = data.input
        document_text = input_data.get('documentText', '')

        if not document_text:
            raise ValueError("documentText is required")

        logger.info(f"Assessing patentability for document (length={len(document_text)})")

        # Call the service
        result = claim_extractor.assess_patentability(document_text)

        # Return in Orchestrate format
        logger.info(f"Patentability assessment complete: {result['isPatentable']} ({result['confidence']}%)")
        return SkillOutput(output=result)

    except Exception as e:
        logger.error(f"Patentability checker skill failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Patentability assessment failed: {str(e)}"
        )


# ============================================================================
# SKILL 2: Claim Extractor
# ============================================================================

@router.post("/claim-extractor", response_model=SkillOutput)
async def claim_extractor_skill(data: SkillInput = Body(...)):
    """
    Skill: Extract Claims

    Called by Orchestrate to extract structured claims from disclosure.
    Extracts keywords, innovations, IPC codes, and background.

    Input (from Orchestrate):
    {
        "input": {
            "documentText": "The full disclosure text...",
            "analysisId": 123  # Optional, for logging
        }
    }

    Output (to Orchestrate):
    {
        "output": {
            "background": "Background section...",
            "innovations": ["Innovation 1", "Innovation 2", ...],
            "keywords": ["keyword1", "keyword2", ...],
            "ipcClassifications": ["H01M10/05", ...]
        }
    }
    """
    logger.info("Skill: claim-extractor called by Orchestrate")

    try:
        # Extract input
        input_data = data.input
        document_text = input_data.get('documentText', '')

        if not document_text:
            raise ValueError("documentText is required")

        logger.info(f"Extracting claims from document (length={len(document_text)})")

        # Call the service
        result = claim_extractor.extract(document_text)

        # Return in Orchestrate format
        logger.info(f"Claim extraction complete: {len(result['keywords'])} keywords, {len(result['innovations'])} innovations")
        return SkillOutput(output=result)

    except Exception as e:
        logger.error(f"Claim extractor skill failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Claim extraction failed: {str(e)}"
        )


# ============================================================================
# SKILL 3: Patent Searcher
# ============================================================================

@router.post("/patent-searcher", response_model=SkillOutput)
async def patent_searcher_skill(data: SkillInput = Body(...)):
    """
    Skill: Search Patents

    Called by Orchestrate to search patent databases for relevant prior art.
    Uses keywords and IPC codes from claim extraction.

    Input (from Orchestrate):
    {
        "input": {
            "keywords": ["keyword1", "keyword2", ...],
            "ipcClassifications": ["H01M10/05", ...],
            "maxResults": 100  # Optional, defaults to 100
        }
    }

    Output (to Orchestrate):
    {
        "output": {
            "patents": [
                {
                    "patentId": "US1234567",
                    "title": "Patent title",
                    "abstract": "Patent abstract...",
                    "publicationDate": "2023-01-01",
                    "assignee": "Company Name",
                    "ipcClassifications": ["H01M10/05"]
                },
                ...
            ],
            "totalFound": 42
        }
    }
    """
    logger.info("Skill: patent-searcher called by Orchestrate")

    try:
        # Extract input
        input_data = data.input
        keywords = input_data.get('keywords', [])
        ipc_codes = input_data.get('ipcClassifications', [])
        max_results = input_data.get('maxResults', 100)

        if not keywords and not ipc_codes:
            raise ValueError("Either keywords or ipcClassifications required")

        logger.info(f"Searching patents: {len(keywords)} keywords, {len(ipc_codes)} IPC codes, max_results={max_results}")

        # Call the service
        patents = patent_searcher.search(keywords, ipc_codes, max_results)

        # Return in Orchestrate format
        result = {
            'patents': patents,
            'totalFound': len(patents)
        }

        logger.info(f"Patent search complete: {len(patents)} patents found")
        return SkillOutput(output=result)

    except Exception as e:
        logger.error(f"Patent searcher skill failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Patent search failed: {str(e)}"
        )


# ============================================================================
# SKILL 4: Similarity Scorer
# ============================================================================

@router.post("/similarity-scorer", response_model=SkillOutput)
async def similarity_scorer_skill(data: SkillInput = Body(...)):
    """
    Skill: Score Similarity

    Called by Orchestrate to score similarity between disclosure and found patents.
    Uses watsonx.ai for semantic comparison.

    Input (from Orchestrate):
    {
        "input": {
            "claims": {
                "innovations": ["Innovation 1", ...],
                "keywords": ["keyword1", ...]
            },
            "patents": [
                {
                    "patentId": "US1234567",
                    "title": "Patent title",
                    "abstract": "Patent abstract..."
                },
                ...
            ]
        }
    }

    Output (to Orchestrate):
    {
        "output": {
            "scoredPatents": [
                {
                    "patentId": "US1234567",
                    "title": "Patent title",
                    "abstract": "Patent abstract...",
                    "similarityScore": 85.5,
                    "overlappingConcepts": ["concept1", "concept2"],
                    "keyDifferences": ["diff1", "diff2"]
                },
                ...
            ],
            "topScore": 85.5,
            "averageScore": 42.3
        }
    }
    """
    logger.info("Skill: similarity-scorer called by Orchestrate")

    try:
        # Extract input
        input_data = data.input
        claims = input_data.get('claims', {})
        patents = input_data.get('patents', [])

        if not claims:
            raise ValueError("claims is required")
        if not patents:
            raise ValueError("patents is required")

        logger.info(f"Scoring similarity for {len(patents)} patents")

        # Call the service
        scored_patents = similarity_scorer.score_multiple_patents(claims, patents)

        # Calculate statistics
        scores = [p.get('similarityScore', 0) for p in scored_patents]
        top_score = max(scores) if scores else 0
        avg_score = sum(scores) / len(scores) if scores else 0

        # Return in Orchestrate format
        result = {
            'scoredPatents': scored_patents,
            'topScore': top_score,
            'averageScore': avg_score
        }

        logger.info(f"Similarity scoring complete: top_score={top_score:.1f}, avg_score={avg_score:.1f}")
        return SkillOutput(output=result)

    except Exception as e:
        logger.error(f"Similarity scorer skill failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Similarity scoring failed: {str(e)}"
        )


# ============================================================================
# Health Check Endpoint
# ============================================================================

@router.get("/health")
async def skills_health():
    """
    Health check for skill endpoints.

    Returns status of all skill endpoints and their dependencies.
    Useful for Orchestrate to verify skills are available.
    """
    return {
        "status": "healthy",
        "skills": [
            "patentability-checker",
            "claim-extractor",
            "patent-searcher",
            "similarity-scorer"
        ],
        "services": {
            "ClaimExtractor": "initialized",
            "SimilarityScorer": "initialized",
            "PatentSearcher": "initialized"
        }
    }
