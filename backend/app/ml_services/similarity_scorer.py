"""
Similarity Scorer Module

Scores semantic similarity between invention disclosures and patents using watsonx.ai.

Key Features:
- LLM-based semantic comparison
- Fallback to keyword matching if watsonx fails
- Batch scoring for multiple patents
- Identifies overlapping concepts and key differences
"""

from typing import Dict, List
import json
from app.integrations.watsonx_ai import WatsonxAI
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class SimilarityScorer:
    """
    Score similarity between disclosure and patents using watsonx.ai.

    Uses foundation models for semantic similarity analysis that goes beyond
    simple keyword matching to understand technical concepts and relationships.
    """

    def __init__(self):
        """Initialize the similarity scorer with watsonx.ai."""
        self.watsonx_ai = WatsonxAI()
        logger.info("SimilarityScorer initialized")

    def score_similarity(self, claims: dict, patent: dict) -> dict:
        """
        Score similarity between disclosure and single patent.

        Uses watsonx.ai to perform semantic comparison and identify:
        - Overall similarity score (0-100)
        - Specific overlapping technical concepts
        - Key differences that distinguish the disclosure

        Args:
            claims: Extracted claims from disclosure (from ClaimExtractor)
            patent: Patent information (title, abstract, etc.)

        Returns:
            Dictionary with:
                - similarityScore: float (0-100)
                - overlappingConcepts: List[str]
                - keyDifferences: List[str]
        """
        prompt = f"""
Compare invention disclosure with patent. Return JSON:
{{
    "similarity_score": 0-100,
    "overlapping_concepts": ["concept1", "concept2"],
    "key_differences": ["diff1", "diff2"]
}}

Disclosure innovations:
{json.dumps(claims['innovations'])}

Patent:
Title: {patent['title']}
Abstract: {patent['abstract'][:500]}
"""

        try:
            response = self.watsonx_ai.generate(prompt)

            # Clean and parse JSON
            cleaned = response.replace('```json', '').replace('```', '').strip()
            result = json.loads(cleaned)

            return {
                'similarityScore': float(result.get('similarity_score', 50)),
                'overlappingConcepts': result.get('overlapping_concepts', []),
                'keyDifferences': result.get('key_differences', [])
            }

        except Exception as e:
            logger.warning(f"watsonx.ai similarity scoring failed: {str(e)}, using keyword fallback")
            # Fallback: keyword matching
            return self._keyword_matching_fallback(claims, patent)

    def _keyword_matching_fallback(self, claims: dict, patent: dict) -> dict:
        """
        Fallback similarity scoring using keyword matching.

        Used when watsonx.ai is unavailable or fails. Provides basic
        similarity estimation based on keyword overlap.
        """
        innovations_text = ' '.join(claims['innovations']).lower()
        patent_text = f"{patent['title']} {patent['abstract']}".lower()

        # Simple keyword overlap
        common_words = set(innovations_text.split()) & set(patent_text.split())
        score = min(100, len(common_words) * 10)

        return {
            'similarityScore': score,
            'overlappingConcepts': ['Keyword analysis fallback'],
            'keyDifferences': ['Full semantic analysis unavailable']
        }

    def score_multiple_patents(self, claims: dict, patents: list) -> list:
        """
        Score similarity for multiple patents and sort by score.

        Processes each patent in the list and returns them sorted by
        similarity score (highest first) for easy review.

        Args:
            claims: Extracted claims from disclosure
            patents: List of patent dictionaries

        Returns:
            List of patents with similarity scores, sorted by score (descending)
        """
        logger.info(f"Scoring {len(patents)} patents")

        scored = []

        for patent in patents:
            score_data = self.score_similarity(claims, patent)
            scored.append({**patent, **score_data})

        # Sort by similarity (highest first)
        scored.sort(key=lambda x: x['similarityScore'], reverse=True)

        logger.info(f"Scored {len(scored)} patents, top score: {scored[0]['similarityScore']:.1f}" if scored else "No patents scored")
        return scored
