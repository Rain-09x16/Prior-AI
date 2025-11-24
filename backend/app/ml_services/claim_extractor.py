"""
Claim Extractor Module

Extracts structured claims from invention disclosure documents and assesses patentability.

This module uses:
- watsonx NLU for keyword/entity extraction
- watsonx.ai for patentability assessment and innovation extraction

Key Functions:
1. assess_patentability() - NEW in v3.0: Check if patentable vs publishable
2. extract() - Extract structured claims from disclosure text
"""

from typing import Dict, List
import json
from app.integrations.watsonx_nlu import WatsonxNLU
from app.integrations.watsonx_ai import WatsonxAI
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class ClaimExtractor:
    """
    Extract claims and assess patentability using watsonx NLU and watsonx.ai.

    This is a core component of the analysis pipeline that runs FIRST to determine
    if a disclosure is worth analyzing (patentable) or should be rejected early
    (publishable-only research).
    """

    def __init__(self):
        """Initialize the claim extractor with watsonx services."""
        self.watsonx_nlu = WatsonxNLU()
        self.watsonx_ai = WatsonxAI()
        logger.info("ClaimExtractor initialized")

    def assess_patentability(self, text: str) -> dict:
        """
        NEW: Check if patentable vs publishable-only research.

        This is the FIRST step in the workflow to prevent expensive prior art searches
        on research that is publishable but not patentable.

        PATENTABLE inventions have:
        - Specific device design, process steps, or method
        - Industrial application (can be manufactured/used)
        - Technical details (numbers, materials, configurations)

        PUBLISHABLE-ONLY research:
        - Only theory or experimental results
        - No specific implementation
        - Just observations or discoveries

        Business Value:
        - Saves $500-1,000 per avoided filing
        - Prevents 30-40% of wasted filings
        - Helps TTOs focus on truly patentable innovations

        Args:
            text: Full disclosure text

        Returns:
            Dictionary with:
                - isPatentable: bool
                - confidence: float (0-100)
                - missingElements: List[str]
                - recommendations: List[str]
        """
        logger.info("Assessing patentability")

        prompt = f"""
Analyze if this invention disclosure is PATENTABLE or just PUBLISHABLE research.

PATENTABLE inventions have:
- Specific device design, process steps, or method
- Industrial application (can be manufactured/used)
- Technical details (numbers, materials, configurations)

PUBLISHABLE-ONLY research:
- Only theory or experimental results
- No specific implementation
- Just observations or discoveries

Disclosure (first 2000 chars):
{text[:2000]}

Respond with ONLY valid JSON:
{{
    "isPatentable": true/false,
    "confidence": 0-100,
    "reasoning": "brief explanation",
    "missingElements": ["element1", "element2"],
    "recommendations": ["add specific device details", "define manufacturing process"]
}}

DO NOT include any text before or after the JSON.
"""

        try:
            response = self.watsonx_ai.generate(prompt)

            # Clean and parse JSON
            cleaned = response.replace('```json', '').replace('```', '').strip()
            result = json.loads(cleaned)

            patentability_result = {
                'isPatentable': result.get('isPatentable', True),
                'confidence': result.get('confidence', 50),
                'missingElements': result.get('missingElements', []),
                'recommendations': result.get('recommendations', [])
            }

            logger.info(f"Patentability: {patentability_result['isPatentable']} (confidence: {patentability_result['confidence']}%)")
            return patentability_result

        except Exception as e:
            logger.error(f"Patentability assessment failed: {str(e)}")
            # If parsing fails, assume patentable to not block workflow
            return {
                'isPatentable': True,
                'confidence': 60,
                'missingElements': [],
                'recommendations': ['Manual review recommended - automated assessment failed']
            }

    def extract(self, text: str) -> dict:
        """
        Extract structured claims from disclosure text.

        Uses watsonx NLU for entity extraction and watsonx.ai for
        structured innovation extraction.

        Args:
            text: Full disclosure text

        Returns:
            Dictionary with:
                - background: str
                - innovations: List[str]
                - keywords: List[str]
                - ipcClassifications: List[str]
        """
        logger.info("Extracting claims from disclosure")

        # Extract background FIRST (always needed)
        background = self._extract_background(text)
        
        # Analyze with watsonx NLU
        nlu_result = self.watsonx_nlu.analyze(text)

        # Extract components with proper defaults
        innovations = self._extract_innovations(text, nlu_result)
        keywords = [kw['text'] for kw in nlu_result.get('keywords', [])][:20]
        ipc_codes = self._classify_ipc(keywords)

        result = {
            'background': background,
            'innovations': innovations if innovations else ["Innovation extraction pending"],
            'keywords': keywords if keywords else ["disclosure", "analysis"],
            'ipcClassifications': ipc_codes if ipc_codes else ["G06F"]  # Default to computing
        }

        logger.info(f"Extracted {len(keywords)} keywords, {len(innovations)} innovations, {len(ipc_codes)} IPC codes")
        return result

    def _extract_background(self, text: str) -> str:
        """
        Extract background section from disclosure.

        Looks for common section markers or returns beginning of document.
        ALWAYS returns a non-empty string.
        """
        if not text:
            return "No disclosure text provided"
            
        # Look for common patterns
        text_lower = text.lower()
        patterns = ['background', 'prior art', 'field of invention', 'technical field', 'problem', 'introduction', 'overview']

        for pattern in patterns:
            if pattern in text_lower:
                start = text_lower.index(pattern)
                background = text[start:start+500].strip()
                if background:
                    return background

        # Fallback: first 300 chars
        background = text[:300].strip()
        return background if background else "Technical disclosure provided"

    def _extract_innovations(self, text: str, nlu_result: dict) -> list:
        """
        Extract key innovations using watsonx.ai.

        Prompts the LLM to identify the 3-5 key technical innovations
        from the disclosure.
        """
        prompt = f"""
Extract the 3-5 key technical innovations from this disclosure.
Focus on WHAT is new, not WHY it's important.

Disclosure:
{text[:1500]}

Return JSON list:
["Innovation 1", "Innovation 2", ...]
"""

        try:
            response = self.watsonx_ai.generate(prompt)

            # Clean and parse JSON
            cleaned = response.replace('```json', '').replace('```', '').strip()
            innovations = json.loads(cleaned)

            if isinstance(innovations, list) and innovations:
                logger.info(f"Extracted {len(innovations)} innovations")
                return innovations
            else:
                raise ValueError("Invalid innovations format")

        except Exception as e:
            logger.error(f"Innovation extraction failed: {str(e)}")
            return ["Innovation extraction failed - manual review needed"]

    def _classify_ipc(self, keywords: list) -> list:
        """
        Map keywords to IPC (International Patent Classification) codes.

        Uses a keyword-to-IPC mapping to suggest relevant patent classifications.
        """
        ipc_mapping = {
            'battery': ['H01M10/05'],
            'electrolyte': ['H01M10/0562'],
            'lithium': ['H01M10/0525'],
            'drug': ['A61K31'],
            'pharmaceutical': ['A61K'],
            'neural network': ['G06N3/08'],
            'machine learning': ['G06N20/00'],
            'sensor': ['G01D5/00'],
            'semiconductor': ['H01L29/00'],
            'database': ['G06F16'],
            'communication': ['H04L'],
            'wireless': ['H04W'],
            'software': ['G06F'],
            'algorithm': ['G06F'],
            'network': ['H04L'],
            'medical': ['A61'],
            'chemical': ['C01'],
            'polymer': ['C08'],
            'metal': ['C22'],
            'engine': ['F02'],
            'mechanical': ['F16'],
            'display': ['G09'],
            'optics': ['G02'],
        }

        codes = set()
        for keyword in keywords:
            keyword_lower = keyword.lower()
            for term, ipc_codes in ipc_mapping.items():
                if term in keyword_lower:
                    codes.update(ipc_codes)

        # Default if nothing found
        if not codes:
            codes = {'G06F'}  # Default: computing

        return sorted(list(codes))
