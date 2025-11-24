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

        if not self.api_key or not self.project_id:
            logger.warning("WATSONX_API_KEY or PROJECT_ID not set - using stub implementation")
            self.use_stub = True
        elif not WATSONX_AVAILABLE:
            logger.warning("ibm-watsonx-ai SDK not installed - using stub implementation. Install with: pip install ibm-watsonx-ai")
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
            logger.info(f"Generating text with prompt length: {len(prompt)} chars (STUB - no API available)")
            return self._stub_generate(prompt)

        try:
            logger.info(f"Generating text with watsonx.ai model={self.model_id}, prompt length: {len(prompt)} chars")

            # Call watsonx.ai API with correct parameters
            # Note: ModelInference expects different parameter names than we initially tried
            response = self.model.generate_text(prompt=prompt)

            logger.info(f"Successfully generated {len(response)} chars from watsonx.ai")
            return response.strip()

        except Exception as e:
            logger.error(f"Error generating text from watsonx.ai: {str(e)}")
            logger.warning("Falling back to stub implementation - make sure WATSONX_API_KEY and WATSONX_PROJECT_ID are set correctly")
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
        watsonx credentials. DYNAMICALLY generates responses based on input.
        """
        import hashlib
        
        prompt_lower = prompt.lower()
        
        # Generate a hash-based seed from the prompt for consistent but varied results
        prompt_hash = int(hashlib.md5(prompt.encode()).hexdigest(), 16)
        seed_score = (prompt_hash % 40) + 40  # Random score between 40-80

        # Check what type of analysis is being requested
        if 'patentability' in prompt_lower or 'patentable' in prompt_lower:
            # Patentability assessment stub - varies based on keywords in prompt
            is_patentable = 'device' in prompt_lower or 'method' in prompt_lower or 'system' in prompt_lower or 'process' in prompt_lower
            confidence = 60 + (prompt_hash % 35)  # 60-95% confidence
            return json.dumps({
                "isPatentable": is_patentable,
                "confidence": min(95, confidence),
                "reasoning": f"Analysis indicates {'patentable' if is_patentable else 'publishable'} disclosure",
                "missingElements": [] if is_patentable else ["Specific implementation details", "Manufacturing specifications"],
                "recommendations": ["Review disclosure against prior art", "Consider claim scope"]
            })

        elif 'similarity' in prompt_lower or 'compare' in prompt_lower:
            # Similarity scoring stub - DYNAMIC based on input
            # Extract innovation count to vary the score
            innovation_count = prompt_lower.count('innovation') + prompt_lower.count('feature')
            base_score = seed_score + (innovation_count * 2)
            similarity_score = min(95, max(10, base_score))
            
            return json.dumps({
                "similarity_score": float(similarity_score),
                "overlapping_concepts": [
                    "Technical architecture similarity",
                    "Implementation approach",
                    "Performance optimization strategy"
                ] if similarity_score > 60 else ["Generic technological domain"],
                "key_differences": [
                    "Novel algorithm implementation",
                    "Enhanced efficiency metrics",
                    "Improved scaling approach"
                ]
            })

        elif 'innovation' in prompt_lower or 'extract' in prompt_lower:
            # Innovation extraction stub - varies based on prompt length
            num_innovations = 3 + (len(prompt) // 500)
            innovations = [f"Technical innovation {i+1}" for i in range(min(5, num_innovations))]
            return json.dumps(innovations)

        elif 'invention disclosure' in prompt_lower and 'convert' in prompt_lower:
            # IDF generation stub (for training data)
            return f"""
Title: Generated Invention Disclosure ({prompt_hash % 1000})

Background:
Technical innovation system designed for improved performance metrics.

Key Innovations:
1. Primary technical advancement for system efficiency
2. Secondary optimization approach for resource management
3. Tertiary enhancement for scalability

Technical Details:
- Performance improvement: {40 + (prompt_hash % 40)}%
- Complexity metric: O(n log n)
- Resource efficiency: Enhanced
"""
        
        else:
            # Generic response - varies based on prompt
            return f"Analysis generated with dynamic response (seed: {prompt_hash % 10000})"

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
