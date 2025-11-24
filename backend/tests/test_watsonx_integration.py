"""
Test script to verify watsonx integrations are working correctly.

This script tests:
1. WatsonxAI initialization and generate() method
2. WatsonxNLU initialization and analyze() method
3. ClaimExtractor with patentability assessment
4. SimilarityScorer for comparing disclosures
5. RecommendationGenerator for final recommendations
"""

import os
import sys
import json

# Fix Unicode encoding on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.integrations.watsonx_ai import WatsonxAI
from app.integrations.watsonx_nlu import WatsonxNLU
from app.ml_services.claim_extractor import ClaimExtractor
from app.ml_services.similarity_scorer import SimilarityScorer
from app.ml_services.recommender import RecommendationGenerator
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def test_watsonx_ai():
    """Test WatsonxAI initialization and basic generation."""
    print("\n" + "="*60)
    print("TEST 1: WatsonxAI Integration")
    print("="*60)
    
    try:
        ai = WatsonxAI()
        print(f"✓ WatsonxAI initialized successfully")
        print(f"  Model: {ai.model_id}")
        print(f"  API Mode: {'REAL' if not ai.use_stub else 'STUB'}")
        
        # Test basic generation
        test_prompt = "What is a patent? Answer in 1 sentence."
        response = ai.generate(test_prompt, max_tokens=100)
        print(f"✓ Generated text: {response[:100]}...")
        
        return True
    except Exception as e:
        print(f"✗ WatsonxAI test failed: {str(e)}")
        return False


def test_watsonx_nlu():
    """Test WatsonxNLU initialization and analysis."""
    print("\n" + "="*60)
    print("TEST 2: WatsonxNLU Integration")
    print("="*60)
    
    try:
        nlu = WatsonxNLU()
        print(f"✓ WatsonxNLU initialized successfully")
        print(f"  API Mode: {'REAL' if not nlu.use_stub else 'STUB'}")
        
        # Test with sample text
        sample_text = """
        This invention relates to a novel lithium-ion battery with improved
        energy density. The battery includes a specialized electrolyte formulation
        that increases charge capacity by 40% compared to existing designs.
        The cathode is made of layered oxide material with custom doping.
        """
        
        result = nlu.analyze(sample_text, features=['keywords', 'entities'])
        print(f"✓ Analyzed text successfully")
        print(f"  Keywords found: {len(result.get('keywords', []))}")
        print(f"  Entities found: {len(result.get('entities', []))}")
        
        if result.get('keywords'):
            print(f"  Top keywords: {[kw['text'] for kw in result['keywords'][:3]]}")
        
        return True
    except Exception as e:
        print(f"✗ WatsonxNLU test failed: {str(e)}")
        return False


def test_claim_extractor():
    """Test ClaimExtractor with patentability assessment."""
    print("\n" + "="*60)
    print("TEST 3: ClaimExtractor (Patentability + Extraction)")
    print("="*60)
    
    try:
        extractor = ClaimExtractor()
        print(f"✓ ClaimExtractor initialized successfully")
        
        # Test patentability assessment
        sample_disclosure = """
        INVENTION DISCLOSURE

        BACKGROUND:
        Current lithium-ion batteries suffer from low energy density and expensive
        manufacturing processes.

        INNOVATION:
        We have developed a novel electrochemistry approach using a proprietary
        electrolyte formulation that significantly increases energy density.

        TECHNICAL DETAILS:
        - Electrolyte: 1M LiPF6 in EC:DMC (1:1) with 5% additives
        - Cathode material: LiNi0.8Co0.1Mn0.1O2 with Mg-doping
        - Anode: Graphite with SEI protection layer
        - Operating voltage: 3.0-4.3V
        - Capacity increase: 40% vs baseline
        - Cost reduction: 15% due to simplified manufacturing

        CLAIMS:
        1. A battery system comprising the novel electrolyte formulation
        2. The manufacturing process for the Mg-doped cathode
        3. The complete battery assembly with improved thermal management
        """
        
        # Test patentability assessment
        patentability = extractor.assess_patentability(sample_disclosure)
        print(f"✓ Patentability assessment completed")
        print(f"  Is Patentable: {patentability['isPatentable']}")
        print(f"  Confidence: {patentability['confidence']}%")
        
        # Test claim extraction
        claims = extractor.extract(sample_disclosure)
        print(f"✓ Claims extraction completed")
        print(f"  Background: {claims['background'][:100]}...")
        print(f"  Innovations found: {len(claims['innovations'])}")
        print(f"  Keywords found: {len(claims['keywords'])}")
        print(f"  IPC codes found: {claims['ipcClassifications']}")
        
        return True
    except Exception as e:
        print(f"✗ ClaimExtractor test failed: {str(e)}")
        return False


def test_similarity_scorer():
    """Test SimilarityScorer for patent comparison."""
    print("\n" + "="*60)
    print("TEST 4: SimilarityScorer (Patent Matching)")
    print("="*60)
    
    try:
        scorer = SimilarityScorer()
        print(f"✓ SimilarityScorer initialized successfully")
        
        # Sample claims from disclosure
        claims = {
            'innovations': [
                'Novel electrolyte formulation with improved energy density',
                'Mg-doped cathode material with enhanced stability',
                'Simplified manufacturing process reducing costs'
            ],
            'keywords': ['battery', 'lithium-ion', 'electrolyte', 'cathode']
        }
        
        # Sample prior art patent
        patent = {
            'title': 'High Energy Density Lithium-Ion Battery',
            'abstract': 'A lithium-ion battery with improved energy density using a novel electrolyte formulation. The battery achieves 40% higher capacity than conventional designs with LiNi0.8Co0.1Mn0.1O2 cathode material.',
            'id': 'US12345678A'
        }
        
        score_result = scorer.score_similarity(claims, patent)
        print(f"✓ Similarity scoring completed")
        print(f"  Similarity Score: {score_result['similarityScore']:.1f}%")
        print(f"  Overlapping Concepts: {score_result['overlappingConcepts'][:2] if score_result['overlappingConcepts'] else 'None'}")
        print(f"  Key Differences: {score_result['keyDifferences'][:2] if score_result['keyDifferences'] else 'None'}")
        
        return True
    except Exception as e:
        print(f"✗ SimilarityScorer test failed: {str(e)}")
        return False


def test_recommendation_generator():
    """Test RecommendationGenerator for final analysis."""
    print("\n" + "="*60)
    print("TEST 5: RecommendationGenerator (Analysis Result)")
    print("="*60)
    
    try:
        gen = RecommendationGenerator()
        print(f"✓ RecommendationGenerator initialized successfully")
        
        claims = {'innovations': ['Novel technology']}
        
        # Test with various patent similarity scores
        scored_patents = [
            {'title': 'Patent 1', 'similarityScore': 45.0},
            {'title': 'Patent 2', 'similarityScore': 55.0},
            {'title': 'Patent 3', 'similarityScore': 65.0}
        ]
        
        recommendation = gen.generate(claims, scored_patents)
        print(f"✓ Recommendation generated")
        print(f"  Novelty Score: {recommendation['noveltyScore']}")
        print(f"  Recommendation: {recommendation['recommendation'].upper()}")
        print(f"  Reasoning: {recommendation['reasoning']}")
        
        return True
    except Exception as e:
        print(f"✗ RecommendationGenerator test failed: {str(e)}")
        return False


def main():
    """Run all integration tests."""
    print("\n" + "="*60)
    print("WATSONX INTEGRATION TEST SUITE")
    print("="*60)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    print(f"\nEnvironment:")
    print(f"  WATSONX_API_KEY: {'SET' if os.getenv('WATSONX_API_KEY') else 'NOT SET'}")
    print(f"  WATSONX_PROJECT_ID: {'SET' if os.getenv('WATSONX_PROJECT_ID') else 'NOT SET'}")
    print(f"  WATSONX_URL: {os.getenv('WATSONX_URL', 'DEFAULT')}")
    
    results = []
    
    # Run all tests
    results.append(("WatsonxAI", test_watsonx_ai()))
    results.append(("WatsonxNLU", test_watsonx_nlu()))
    results.append(("ClaimExtractor", test_claim_extractor()))
    results.append(("SimilarityScorer", test_similarity_scorer()))
    results.append(("RecommendationGenerator", test_recommendation_generator()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All watsonx integrations are working correctly!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
