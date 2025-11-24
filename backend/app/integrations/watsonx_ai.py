"""
watsonx.ai Integration Wrapper

This module provides integration with IBM watsonx.ai for:
- Patentability assessment (distinguishing patentable vs publishable research)
- Similarity scoring (comparing disclosures with patents)
- IDF generation from patents (for training data)
- Natural language generation for recommendations

IMPLEMENTATION STATUS: STUB/TODO
This is a stub implementation that needs to be completed by the AI/ML developer
with actual watsonx.ai API integration.

Required Environment Variables:
    WATSONX_API_KEY: Your IBM Cloud API key
    WATSONX_URL: watsonx.ai service endpoint
    WATSONX_PROJECT_ID: watsonx project ID

Usage:
    from app.integrations.watsonx_ai import WatsonxAI

    ai = WatsonxAI()
    response = ai.generate(prompt, max_tokens=500)
"""

import os
import json
from typing import Dict, Optional
from app.utils.logger import setup_logger

try:
    from ibm_watsonx_ai.foundation_models import ModelInference
    from ibm_watsonx_ai import Credentials
    WATSONX_AVAILABLE = True
except ImportError:
    WATSONX_AVAILABLE = False

logger = setup_logger(__name__)


class WatsonxAI:
    """
    Wrapper for IBM watsonx.ai Foundation Models API.

    Used for:
    - Patentability assessment using LLM reasoning
    - Semantic similarity scoring between disclosures and patents
    - Generating structured JSON responses for analysis
    - Creating synthetic training data (IDF generation)

    TODO: AI/ML Developer - Implement actual watsonx.ai integration
    """

    def __init__(self, model_id: str = "ibm/granite-3-8b-instruct"):
        """
        Initialize watsonx.ai client.

        Args:
            model_id: Foundation model to use. Options:
                - "ibm/granite-3-8b-instruct" (default, recommended for reasoning)
                - "meta-llama/llama-3-3-70b-instruct" (more powerful)
                - "ibm/granite-3-2-8b-instruct"
        """
        self.api_key = os.getenv('WATSONX_API_KEY')
        self.watsonx_url = os.getenv('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')
        self.project_id = os.getenv('WATSONX_PROJECT_ID')
        self.model_id = model_id
        self.model = None
        self.use_stub = False

        if not self.api_key or not self.project_id or not WATSONX_AVAILABLE:
            logger.warning("WATSONX_API_KEY or PROJECT_ID not set, or SDK not installed - using stub implementation")
            self.use_stub = True
        else:
            try:
                # Initialize IBM watsonx.ai credentials
                credentials = Credentials(
                    url=self.watsonx_url,
                    api_key=self.api_key
                )

                # Initialize the model
                self.model = ModelInference(
                    model_id=self.model_id,
                    credentials=credentials,
                    project_id=self.project_id,
                    params={
                        "decoding_method": "greedy",
                        "max_new_tokens": 500,
                        "min_new_tokens": 1,
                        "temperature": 0.3,
                        "top_k": 50,
                        "top_p": 0.9
                    }
                )

                logger.info(f"WatsonxAI initialized with model {self.model_id} - REAL API mode")
            except Exception as e:
                logger.error(f"Failed to initialize watsonx.ai client: {e}")
                logger.warning("Falling back to stub implementation")
                self.use_stub = True

    def generate(self, prompt: str, max_tokens: int = 500, temperature: float = 0.3) -> str:
        """
        Generate text using watsonx.ai foundation model.

        Args:
            prompt: Input prompt for the model
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative)
                        Lower values (0.1-0.3) recommended for structured JSON outputs

        Returns:
            Generated text from the model
        """
        if self.use_stub or not self.model:
            logger.info(f"Generating text with prompt length: {len(prompt)} chars (STUB)")
            return self._stub_generate(prompt)

        try:
            logger.info(f"Generating text with watsonx.ai, prompt length: {len(prompt)} chars")

            # Update model parameters for this generation
            self.model.params["max_new_tokens"] = max_tokens
            self.model.params["temperature"] = temperature

            # Call watsonx.ai API
            response = self.model.generate_text(prompt=prompt)

            logger.info(f"Successfully generated {len(response)} chars from watsonx.ai")
            return response

        except Exception as e:
            logger.error(f"Error generating text from watsonx.ai: {e}")
            logger.warning("Falling back to stub implementation")
            return self._stub_generate(prompt)

    def generate_json(self, prompt: str, max_tokens: int = 500) -> Dict:
        """
        Generate structured JSON response using watsonx.ai.

        This method is specifically designed for prompts that request JSON output.
        It uses lower temperature for more deterministic, structured responses.

        Args:
            prompt: Input prompt (should instruct model to output JSON)
            max_tokens: Maximum tokens to generate

        Returns:
            Parsed JSON dictionary

        Raises:
            json.JSONDecodeError: If model output is not valid JSON
        """
        # Use low temperature for structured output
        response = self.generate(prompt, max_tokens=max_tokens, temperature=0.1)

        # Clean response (remove markdown code blocks if present)
        cleaned = response.replace('```json', '').replace('```', '').strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from model output: {cleaned[:200]}...")
            raise

    def _stub_generate(self, prompt: str) -> str:
        """
        STUB implementation - returns mock responses based on prompt.

        This allows the system to work in development mode without actual
        watsonx credentials. Remove when implementing real integration.
        """
        prompt_lower = prompt.lower()

        # Check what type of analysis is being requested
        if 'patentability' in prompt_lower or 'patentable' in prompt_lower:
            # Patentability assessment stub
            is_patentable = 'device' in prompt_lower or 'method' in prompt_lower or 'system' in prompt_lower
            return json.dumps({
                "isPatentable": is_patentable,
                "confidence": 75 if is_patentable else 60,
                "reasoning": "STUB: Basic keyword analysis",
                "missingElements": [] if is_patentable else ["Specific technical details", "Manufacturing process"],
                "recommendations": ["STUB: Implement actual watsonx.ai analysis"]
            })

        elif 'similarity' in prompt_lower or 'compare' in prompt_lower:
            # Similarity scoring stub
            return json.dumps({
                "similarity_score": 65,
                "overlapping_concepts": ["Common technical domain", "Similar approach"],
                "key_differences": ["Different implementation", "Novel combination"]
            })

        elif 'innovation' in prompt_lower or 'extract' in prompt_lower:
            # Innovation extraction stub
            return json.dumps([
                "STUB: Innovation 1 - needs actual extraction",
                "STUB: Innovation 2 - needs actual extraction",
                "STUB: Innovation 3 - needs actual extraction"
            ])

        elif 'invention disclosure' in prompt_lower and 'convert' in prompt_lower:
            # IDF generation stub (for training data)
            return """
Title: STUB Generated Invention Disclosure

Background:
This is a stub-generated disclosure. The actual implementation should use
watsonx.ai to convert patent language into researcher-friendly disclosure format.

Key Innovations:
1. STUB innovation point 1
2. STUB innovation point 2
3. STUB innovation point 3

Technical Details:
- STUB measurement 1
- STUB measurement 2

Advantages:
- STUB advantage 1
- STUB advantage 2
"""

        else:
            # Generic response
            return "STUB response - implement actual watsonx.ai integration"

    def assess_patentability(self, text: str) -> Dict:
        """
        Assess if disclosure is patentable vs publishable-only.

        Convenience method that constructs the patentability prompt and
        returns parsed JSON response.

        Args:
            text: Disclosure text to assess

        Returns:
            Dictionary with patentability assessment:
            {
                'isPatentable': bool,
                'confidence': float (0-100),
                'missingElements': List[str],
                'recommendations': List[str]
            }
        """
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

        return self.generate_json(prompt)

    def score_similarity(self, disclosure_innovations: list, patent_title: str, patent_abstract: str) -> Dict:
        """
        Score similarity between disclosure and patent.

        Convenience method for semantic similarity scoring.

        Args:
            disclosure_innovations: List of innovation points from disclosure
            patent_title: Patent title
            patent_abstract: Patent abstract

        Returns:
            Dictionary with similarity assessment:
            {
                'similarity_score': float (0-100),
                'overlapping_concepts': List[str],
                'key_differences': List[str]
            }
        """
        prompt = f"""
Compare invention disclosure with patent. Return JSON:
{{
    "similarity_score": 0-100,
    "overlapping_concepts": ["concept1", "concept2"],
    "key_differences": ["diff1", "diff2"]
}}

Disclosure innovations:
{json.dumps(disclosure_innovations)}

Patent:
Title: {patent_title}
Abstract: {patent_abstract[:500]}
"""

        return self.generate_json(prompt)


# TODO: AI/ML Developer - Complete Implementation Checklist
#
# [ ] Install required dependencies:
#     pip install ibm-watson-machine-learning
#
# [ ] Set up watsonx.ai credentials in .env:
#     WATSONX_API_KEY=your_actual_key
#     WATSONX_URL=https://us-south.ml.cloud.ibm.com
#     WATSONX_PROJECT_ID=your_project_id
#
# [ ] Replace __init__() with actual watsonx.ai client initialization
#
# [ ] Replace generate() stub with actual foundation model API calls
#
# [ ] Test JSON parsing with various prompts
#
# [ ] Implement error handling for malformed JSON responses
#
# [ ] Add retry logic for API failures
#
# [ ] Optimize temperature and token settings for each use case
#
# [ ] Consider prompt engineering improvements for better accuracy
#
# [ ] Test with different foundation models to find best performance
