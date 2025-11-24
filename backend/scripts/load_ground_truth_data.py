"""
Ground Truth Dataset Loader

This script loads the ground truth patent IDF dataset and:
1. Extracts individual IDF disclosure pairs
2. Extracts source patents for reference
3. Creates test cases for ML pipeline validation
4. Generates statistics and validation reports

Usage:
    python scripts/load_ground_truth_data.py
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Fix Windows encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


class GroundTruthDataLoader:
    """Loader for ground truth patent IDF dataset"""

    def __init__(self, dataset_path: str = None):
        """Initialize the loader with dataset path"""
        if dataset_path is None:
            # Default to training_data directory
            base_dir = Path(__file__).parent.parent
            dataset_path = base_dir / "training_data" / "ground_truth_dataset.json"

        self.dataset_path = Path(dataset_path)
        self.base_dir = self.dataset_path.parent
        self.pairs_dir = self.base_dir / "pairs"
        self.patents_dir = self.base_dir / "patents"

        # Create directories if they don't exist
        self.pairs_dir.mkdir(exist_ok=True)
        self.patents_dir.mkdir(exist_ok=True)

        self.dataset = None
        self.statistics = {}

    def load_dataset(self) -> Dict:
        """Load the ground truth dataset from JSON"""
        print(f"Loading dataset from: {self.dataset_path}")

        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            self.dataset = json.load(f)

        print(f"✓ Dataset loaded successfully")
        print(f"  Version: {self.dataset['metadata']['version']}")
        print(f"  Domains: {self.dataset['metadata']['domains_covered']}")
        print(f"  Total Disclosures: {self.dataset['metadata']['total_disclosures']}")
        print(f"  Total Prior Art: {self.dataset['metadata']['total_prior_art_references']}")

        return self.dataset

    def extract_idf_pairs(self):
        """Extract individual IDF disclosure pairs into separate files"""
        print("\n🔄 Extracting IDF disclosure pairs...")

        if not self.dataset:
            self.load_dataset()

        pair_count = 0
        novel_count = 0
        not_novel_count = 0

        for entry in self.dataset['dataset_entries']:
            domain = entry['domain']
            domain_slug = domain.lower().replace(' - ', '_').replace(' ', '_')

            # Extract reference patent
            ref_patent = entry['reference_patent']
            ref_patent_file = self.patents_dir / f"{domain_slug}_reference_patent.json"

            with open(ref_patent_file, 'w', encoding='utf-8') as f:
                json.dump(ref_patent, f, indent=2, ensure_ascii=False)

            print(f"  ✓ Saved reference patent: {ref_patent_file.name}")

            # Extract each disclosure pair
            for disclosure in entry['disclosures']:
                case_type = disclosure['case_type']
                label = disclosure['ground_truth_label']

                # Create filename
                filename = f"{domain_slug}_{case_type.lower()}.json"
                filepath = self.pairs_dir / filename

                # Save disclosure pair
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(disclosure, f, indent=2, ensure_ascii=False)

                pair_count += 1
                if case_type == "NOVEL":
                    novel_count += 1
                elif case_type == "NOT_NOVEL":
                    not_novel_count += 1

                print(f"  ✓ Saved {case_type} pair: {filename} (Label: {label})")

        self.statistics['total_pairs'] = pair_count
        self.statistics['novel_pairs'] = novel_count
        self.statistics['not_novel_pairs'] = not_novel_count

        print(f"\n✓ Extracted {pair_count} IDF pairs")
        print(f"  - NOVEL (PATENTABLE): {novel_count}")
        print(f"  - NOT_NOVEL (REJECT): {not_novel_count}")

    def extract_prior_art_patents(self):
        """Extract all prior art patents into a consolidated file"""
        print("\n🔄 Extracting prior art patents...")

        if not self.dataset:
            self.load_dataset()

        all_prior_art = []
        similarity_distribution = {
            'Very High (90-100%)': 0,
            'High (60-85%)': 0,
            'Medium (30-60%)': 0,
            'Low (10-30%)': 0
        }

        for entry in self.dataset['dataset_entries']:
            domain = entry['domain']

            for disclosure in entry['disclosures']:
                # Use correct key name from dataset
                prior_art_list = disclosure.get('relevant_prior_art', [])
                for prior_art in prior_art_list:
                    # Add domain and case type for context
                    prior_art_with_context = {
                        'domain': domain,
                        'related_to_case': disclosure['case_type'],
                        **prior_art
                    }
                    all_prior_art.append(prior_art_with_context)

                    # Count similarity distribution
                    similarity_tier = prior_art.get('similarity_tier', 'Unknown')
                    if similarity_tier in similarity_distribution:
                        similarity_distribution[similarity_tier] += 1

        # Save consolidated prior art file
        prior_art_file = self.patents_dir / "all_prior_art_patents.json"
        with open(prior_art_file, 'w', encoding='utf-8') as f:
            json.dump({
                'total_patents': len(all_prior_art),
                'similarity_distribution': similarity_distribution,
                'patents': all_prior_art
            }, f, indent=2, ensure_ascii=False)

        print(f"  ✓ Saved {len(all_prior_art)} prior art patents to: {prior_art_file.name}")
        print("\n  Similarity Distribution:")
        for tier, count in similarity_distribution.items():
            print(f"    - {tier}: {count} patents")

        self.statistics['total_prior_art'] = len(all_prior_art)
        self.statistics['similarity_distribution'] = similarity_distribution

    def generate_test_cases(self):
        """Generate test cases for ML pipeline validation"""
        print("\n🔄 Generating test cases...")

        if not self.dataset:
            self.load_dataset()

        test_cases = []

        for entry in self.dataset['dataset_entries']:
            domain = entry['domain']

            for disclosure in entry['disclosures']:
                # Extract key information for testing
                idf_content = disclosure.get('idf_content', {})
                test_case = {
                    'test_id': f"{domain}_{disclosure['case_type']}",
                    'domain': domain,
                    'case_type': disclosure['case_type'],
                    'expected_label': disclosure['ground_truth_label'],
                    'idf_data': {
                        'title': idf_content.get('TITLE_OF_INVENTION', ''),
                        'technical_description': idf_content.get('TECHNICAL_DESCRIPTION', ''),
                        'search_terms': idf_content.get('SEARCH_TERMS', [])
                    },
                    'validation_data': disclosure.get('validation_data', {}),
                    'prior_art_count': len(disclosure.get('relevant_prior_art', [])),
                    'expected_similarity_range': self._get_similarity_range(disclosure)
                }
                test_cases.append(test_case)

        # Save test cases
        test_cases_file = self.base_dir / "test_cases.json"
        with open(test_cases_file, 'w', encoding='utf-8') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'total_test_cases': len(test_cases),
                'test_cases': test_cases
            }, f, indent=2, ensure_ascii=False)

        print(f"  ✓ Generated {len(test_cases)} test cases: {test_cases_file.name}")

        self.statistics['total_test_cases'] = len(test_cases)

    def _get_similarity_range(self, disclosure: Dict) -> Dict:
        """Calculate expected similarity score range from prior art"""
        if disclosure['case_type'] == 'NOVEL':
            # Novel cases should have lower similarity scores
            return {
                'min': 0.0,
                'max': 0.70,  # Some similarity but novel
                'expected': 'low_to_medium'
            }
        else:  # NOT_NOVEL
            # Not novel cases should have high similarity scores
            return {
                'min': 0.70,
                'max': 1.0,  # High similarity
                'expected': 'high_to_very_high'
            }

    def generate_statistics_report(self):
        """Generate comprehensive statistics report"""
        print("\n📊 Generating statistics report...")

        report = {
            'generated_at': datetime.now().isoformat(),
            'dataset_info': {
                'version': self.dataset['metadata']['version'],
                'domains_covered': self.dataset['metadata']['domains_covered'],
                'total_disclosures': self.dataset['metadata']['total_disclosures'],
                'total_prior_art_references': self.dataset['metadata']['total_prior_art_references']
            },
            'extraction_statistics': self.statistics,
            'file_locations': {
                'idf_pairs': str(self.pairs_dir),
                'prior_art_patents': str(self.patents_dir),
                'test_cases': str(self.base_dir / "test_cases.json")
            }
        }

        # Save report
        report_file = self.base_dir / "dataset_statistics.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"  ✓ Statistics report saved: {report_file.name}")

        # Print summary
        print("\n" + "="*60)
        print("DATASET PROCESSING SUMMARY")
        print("="*60)
        print(f"Dataset Version: {report['dataset_info']['version']}")
        print(f"Domains Covered: {report['dataset_info']['domains_covered']}")
        print(f"Total Disclosures: {report['dataset_info']['total_disclosures']}")
        print(f"Total Prior Art References: {report['dataset_info']['total_prior_art_references']}")
        print(f"\nIDF Pairs Extracted: {self.statistics.get('total_pairs', 0)}")
        print(f"  - NOVEL (PATENTABLE): {self.statistics.get('novel_pairs', 0)}")
        print(f"  - NOT_NOVEL (REJECT): {self.statistics.get('not_novel_pairs', 0)}")
        print(f"\nTotal Prior Art Patents: {self.statistics.get('total_prior_art', 0)}")
        print(f"Test Cases Generated: {self.statistics.get('total_test_cases', 0)}")
        print("="*60)

    def run_full_extraction(self):
        """Run complete extraction pipeline"""
        print("="*60)
        print("GROUND TRUTH DATASET EXTRACTION")
        print("="*60)

        self.load_dataset()
        self.extract_idf_pairs()
        self.extract_prior_art_patents()
        self.generate_test_cases()
        self.generate_statistics_report()

        print("\n✅ Dataset extraction completed successfully!")
        print(f"\nFiles are organized in: {self.base_dir}")
        print(f"  - IDF pairs: {self.pairs_dir}")
        print(f"  - Prior art patents: {self.patents_dir}")
        print(f"  - Test cases: test_cases.json")
        print(f"  - Statistics: dataset_statistics.json")


def main():
    """Main entry point"""
    loader = GroundTruthDataLoader()
    loader.run_full_extraction()


if __name__ == "__main__":
    main()
