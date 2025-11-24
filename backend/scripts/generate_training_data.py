"""
Training Data Generation Script

This script reverse-engineers real patents into synthetic Invention Disclosure Forms (IDFs)
to create training/validation data for the prior art analysis pipeline.

Strategy:
- For each patent, create 2 synthetic IDFs:
  1. POSITIVE (Novel): Search date BEFORE priority → should find nothing
  2. NEGATIVE (Not Novel): Search date AFTER publication → should find source patent

This validates the entire pipeline with known ground truth.

Usage:
    cd backend
    python scripts/generate_training_data.py

Requirements:
    - watsonx.ai credentials configured in .env
    - Source patents in training_data/patents/source_patents.json

Output:
    - training_data/pairs/pair_XXX_positive.json
    - training_data/pairs/pair_XXX_negative.json
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.integrations.watsonx_ai import WatsonxAI
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class PatentToIDFGenerator:
    """
    Convert real patents into synthetic Invention Disclosure Forms.

    Uses watsonx.ai to transform patent language into researcher-friendly
    disclosure format for realistic testing data.
    """

    def __init__(self):
        """Initialize the generator with watsonx.ai client."""
        self.watsonx_ai = WatsonxAI()
        logger.info("PatentToIDFGenerator initialized")

    def reverse_engineer_to_idf(self, patent: Dict) -> str:
        """
        Convert patent → IDF using watsonx.ai.

        Takes formal patent language and converts it to how a researcher
        would naturally describe their invention in a disclosure form.

        Args:
            patent: Dictionary with patent data (title, abstract, claims, etc.)

        Returns:
            IDF text in researcher-friendly format
        """
        logger.info(f"Reverse-engineering patent {patent.get('id')} to IDF format")

        prompt = f"""
Convert this patent into an Invention Disclosure Form as a researcher would write it.

Patent Title: {patent.get('title')}
Abstract: {patent.get('abstract')}
Claims: {patent.get('claims', [])[:2]}

Create an IDF with these sections:

1. TITLE: A descriptive title (not the patent title - make it sound like a research project)

2. BACKGROUND: Describe the problem being solved in 2-3 sentences.
   - What's the current limitation?
   - Why is this important?
   - What gap does this fill?

3. KEY INNOVATIONS: List 3-5 bullet points of what's new.
   - Focus on WHAT is new, not patent claim language
   - Use natural researcher language, not legal terminology
   - Be specific about technical features

4. TECHNICAL DETAILS: Provide specific measurements, materials, process steps.
   - Include numbers, ranges, or specifications mentioned in the patent
   - Describe the device/system/method components
   - Explain how it works

5. ADVANTAGES: List 2-4 benefits over existing solutions.
   - Performance improvements
   - Cost reductions
   - Efficiency gains
   - Novel capabilities

Write in the first person ("we developed", "our approach") as a researcher would.
Use technical language but NOT patent legalese (avoid "comprising", "wherein", "said").
"""

        try:
            idf_text = self.watsonx_ai.generate(prompt, max_tokens=800, temperature=0.5)
            logger.info(f"Generated IDF ({len(idf_text)} chars) for patent {patent.get('id')}")
            return idf_text
        except Exception as e:
            logger.error(f"Failed to generate IDF: {str(e)}")
            # Fallback to simple template
            return self._create_fallback_idf(patent)

    def _create_fallback_idf(self, patent: Dict) -> str:
        """
        Create a simple IDF if watsonx.ai fails.

        This ensures the script works even without watsonx credentials.
        """
        return f"""
TITLE: {patent.get('title', 'Research Project')}

BACKGROUND:
{patent.get('abstract', 'Innovation in technical field.')[:300]}

KEY INNOVATIONS:
- Novel approach based on patent {patent.get('id')}
- Technical advancement in the field
- Improved performance and efficiency

TECHNICAL DETAILS:
See patent abstract for detailed specifications.

ADVANTAGES:
- Improved over prior art
- Cost effective solution
- Scalable implementation
"""

    def create_training_pair(self, patent: Dict) -> Dict:
        """
        Create positive (novel) + negative (not novel) training pair.

        Args:
            patent: Dictionary with patent data including dates

        Returns:
            Dictionary with 'positive' and 'negative' training examples
        """
        logger.info(f"Creating training pair for patent {patent.get('id')}")

        # Generate IDF text
        idf_text = self.reverse_engineer_to_idf(patent)

        # Parse dates
        try:
            priority_date = datetime.strptime(patent.get('priority_date'), '%Y-%m-%d')
            publication_date = datetime.strptime(patent.get('publication_date'), '%Y-%m-%d')
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid date format in patent {patent.get('id')}: {e}")
            # Use fallback dates
            priority_date = datetime.now() - timedelta(days=365)
            publication_date = datetime.now()

        # POSITIVE: Search date BEFORE priority (should find nothing)
        positive = {
            'text': idf_text,
            'search_date': (priority_date - timedelta(days=60)).strftime('%Y-%m-%d'),
            'label': {
                'isNovel': True,
                'expectedMatches': 0,
                'reasoning': 'Disclosure predates all prior art - no patents should be found'
            },
            'metadata': {
                'source_patent': patent.get('id'),
                'patent_number': patent.get('patent_number'),
                'priority_date': patent.get('priority_date'),
                'publication_date': patent.get('publication_date'),
                'type': 'positive'
            }
        }

        # NEGATIVE: Search date AFTER publication (should find source patent)
        negative = {
            'text': idf_text,
            'search_date': (publication_date + timedelta(days=90)).strftime('%Y-%m-%d'),
            'label': {
                'isNovel': False,
                'expectedMatches': 1,
                'blockingPatent': patent.get('patent_number'),
                'reasoning': 'Source patent should be found as blocking prior art'
            },
            'metadata': {
                'source_patent': patent.get('id'),
                'patent_number': patent.get('patent_number'),
                'priority_date': patent.get('priority_date'),
                'publication_date': patent.get('publication_date'),
                'type': 'negative'
            }
        }

        return {'positive': positive, 'negative': negative}

    def generate_all_pairs(self, patents: List[Dict], output_dir: Path) -> int:
        """
        Generate training pairs for all patents.

        Args:
            patents: List of patent dictionaries
            output_dir: Directory to save training pairs

        Returns:
            Number of pairs generated
        """
        logger.info(f"Generating training pairs for {len(patents)} patents")

        pairs_generated = 0

        for i, patent in enumerate(patents, start=1):
            try:
                # Create training pair
                pair = self.create_training_pair(patent)

                # Save positive example
                positive_path = output_dir / f"pair_{i:03d}_positive.json"
                with open(positive_path, 'w') as f:
                    json.dump(pair['positive'], f, indent=2)
                logger.info(f"Saved positive example: {positive_path}")

                # Save negative example
                negative_path = output_dir / f"pair_{i:03d}_negative.json"
                with open(negative_path, 'w') as f:
                    json.dump(pair['negative'], f, indent=2)
                logger.info(f"Saved negative example: {negative_path}")

                pairs_generated += 1

            except Exception as e:
                logger.error(f"Failed to generate pair for patent {patent.get('id')}: {str(e)}")
                continue

        return pairs_generated


def main():
    """Main execution function."""
    print("=" * 60)
    print("Training Data Generation Script")
    print("=" * 60)
    print()

    # Set up paths
    script_dir = Path(__file__).parent
    backend_dir = script_dir.parent
    training_data_dir = backend_dir / 'training_data'
    patents_file = training_data_dir / 'patents' / 'source_patents.json'
    pairs_dir = training_data_dir / 'pairs'

    # Load source patents
    print(f"Loading patents from: {patents_file}")
    if not patents_file.exists():
        print(f"ERROR: Patents file not found: {patents_file}")
        print("Please create training_data/patents/source_patents.json with patent data")
        print("See training_data/README.md for format")
        return 1

    with open(patents_file) as f:
        patents = json.load(f)

    print(f"Loaded {len(patents)} patents")
    print()

    # Validate patents
    valid_patents = []
    for patent in patents:
        required_fields = ['id', 'title', 'abstract', 'priority_date', 'publication_date']
        missing = [f for f in required_fields if not patent.get(f)]
        if missing:
            print(f"WARNING: Patent {patent.get('id', 'unknown')} missing fields: {missing}")
            continue
        valid_patents.append(patent)

    if not valid_patents:
        print("ERROR: No valid patents found")
        return 1

    print(f"Valid patents: {len(valid_patents)}")
    print()

    # Generate training pairs
    print("Generating training pairs...")
    print("This will use watsonx.ai to reverse-engineer patents into IDFs")
    print()

    generator = PatentToIDFGenerator()
    pairs_generated = generator.generate_all_pairs(valid_patents, pairs_dir)

    # Summary
    print()
    print("=" * 60)
    print("Generation Complete")
    print("=" * 60)
    print(f"Pairs generated: {pairs_generated}")
    print(f"Total examples: {pairs_generated * 2} ({pairs_generated} positive + {pairs_generated} negative)")
    print(f"Output directory: {pairs_dir}")
    print()

    # Next steps
    print("Next steps:")
    print("1. Review 2-3 generated IDFs in training_data/pairs/")
    print("2. Ensure they sound like researcher disclosures, not patent language")
    print("3. Check that dates are correct:")
    print("   - Positive: search_date < priority_date")
    print("   - Negative: search_date > publication_date")
    print("4. Use these for testing the analysis pipeline")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
