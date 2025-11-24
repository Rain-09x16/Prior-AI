"""
Recommendation Generator Module

Generates patent filing recommendations based on prior art analysis.

Key Features:
- Calculates novelty score using PRD-specified formula
- Determines recommendation (pursue/reconsider/reject)
- Generates human-readable reasoning
- Suggests claim focus areas
"""

from typing import Dict, List
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class RecommendationGenerator:
    """
    Generate overall recommendation from patent similarity scores.

    Uses the novelty calculation formula from PRD v3.0:
    novelty = 100 - (top_score * 0.7) - (high_sim_count * 5)
    """

    def __init__(self):
        """Initialize the recommendation generator."""
        logger.info("RecommendationGenerator initialized")

    def generate(self, claims: dict, scored_patents: list) -> dict:
        """
        Generate recommendation based on claims and scored patents.

        Uses PRD v3.0 novelty calculation formula:
        - Top patent similarity has 70% weight
        - Each high-similarity patent (>70%) reduces novelty by 5%

        Args:
            claims: Extracted claims from disclosure
            scored_patents: List of patents with similarity scores (sorted by score)

        Returns:
            Dictionary with:
                - noveltyScore: float (0-100)
                - recommendation: str (pursue, reconsider, reject)
                - reasoning: str
        """
        logger.info("Generating recommendation")

        if not scored_patents:
            return {
                'noveltyScore': 100.0,
                'recommendation': 'pursue',
                'reasoning': 'No similar prior art found. Proceed with patent application.'
            }

        # Calculate novelty score using PRD formula
        top_score = scored_patents[0]['similarityScore']
        high_sim_count = sum(1 for p in scored_patents if p['similarityScore'] > 70)

        # PRD v3.0 Formula: novelty = 100 - (top_score * 0.7) - (high_sim_count * 5)
        novelty = 100 - (top_score * 0.7) - (high_sim_count * 5)
        novelty = max(0, min(100, novelty))

        # Determine recommendation based on novelty thresholds
        if novelty >= 70:
            rec = 'pursue'
            reasoning = f"High novelty ({novelty:.0f}%). Top match only {top_score:.0f}% similar. Strong patent potential."
        elif novelty >= 40:
            rec = 'reconsider'
            reasoning = f"Medium novelty ({novelty:.0f}%). {high_sim_count} highly similar patents found. Consider narrow claims."
        else:
            rec = 'reject'
            reasoning = f"Low novelty ({novelty:.0f}%). Very similar prior art exists (top: {top_score:.0f}%). Consider publication instead."

        result = {
            'noveltyScore': round(novelty, 1),
            'recommendation': rec,
            'reasoning': reasoning
        }

        logger.info(f"Recommendation: {rec} (novelty: {novelty:.1f}%)")
        return result
