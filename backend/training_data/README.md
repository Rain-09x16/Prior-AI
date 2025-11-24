# Training Data Directory

This directory contains synthetic training data generated from real patents to validate the prior art analysis pipeline.

## Strategy: Reverse-Engineer Patents to IDFs

Instead of manually creating invention disclosure forms, we reverse-engineer real patents into disclosure-style documents using watsonx.ai. This provides realistic test data with known ground truth.

## Directory Structure

```
training_data/
├── README.md                  # This file
├── patents/                   # Source patent data
│   └── source_patents.json    # Patent metadata (title, abstract, claims, dates)
└── pairs/                     # Generated positive/negative training pairs
    ├── pair_001_positive.json # Novel example (search before priority date)
    ├── pair_001_negative.json # Not novel (search after publication)
    ├── pair_002_positive.json
    ├── pair_002_negative.json
    └── ...
```

## Training Pair Format

Each training pair consists of:

### Positive Example (Novel)
- **IDF Text**: Reverse-engineered disclosure from patent
- **Search Date**: BEFORE patent priority date (e.g., priority - 60 days)
- **Expected Result**: No blocking patents found
- **Label**: `isNovel: true`, `expectedMatches: 0`

### Negative Example (Not Novel)
- **IDF Text**: Same reverse-engineered disclosure
- **Search Date**: AFTER patent publication (e.g., publication + 90 days)
- **Expected Result**: Source patent should be found
- **Label**: `isNovel: false`, `expectedMatches: 1`, `blockingPatent: [patent_id]`

## Example Training Pair

**pair_001_positive.json:**
```json
{
  "text": "Novel lithium-ion battery electrolyte system...",
  "search_date": "2019-01-15",
  "label": {
    "isNovel": true,
    "expectedMatches": 0,
    "reasoning": "Disclosure predates all prior art"
  }
}
```

**pair_001_negative.json:**
```json
{
  "text": "Novel lithium-ion battery electrolyte system...",
  "search_date": "2020-06-20",
  "label": {
    "isNovel": false,
    "expectedMatches": 1,
    "blockingPatent": "US10234567B2",
    "reasoning": "Source patent should be found"
  }
}
```

## Generating Training Data

Use the script to generate training pairs:

```bash
cd backend
python scripts/generate_training_data.py
```

This will:
1. Load patent data from `patents/source_patents.json`
2. Use watsonx.ai to reverse-engineer each patent into an IDF
3. Create positive (novel) and negative (not novel) pairs
4. Save to `pairs/` directory

## Recommended Patent Diversity

For comprehensive testing, include patents from different technical domains:

- **3 Battery/Energy Patents** (H01M classification)
  - Test technical specifications and measurements
  - Materials and chemical compositions
  - Process parameters

- **3 Pharma/Biotech Patents** (A61K classification)
  - Medical devices and drug compositions
  - Biological processes
  - Clinical applications

- **2 Software/ML Patents** (G06N classification)
  - Algorithms and data structures
  - Neural network architectures
  - System implementations

- **2 Mechanical/Device Patents** (F16, G01 classifications)
  - Physical devices and mechanisms
  - Measurement instruments
  - Manufacturing processes

## Validation Metrics

When testing with this data, measure:

1. **Patentability Assessment Accuracy**: Does the system correctly identify all examples as patentable?
2. **Similarity Scoring Accuracy**:
   - Positive examples: Should have low similarity scores (no blocking patents)
   - Negative examples: Should find source patent with high similarity (70%+)
3. **Recommendation Accuracy**:
   - Positive: Recommend "pursue" (novelty > 70%)
   - Negative: Recommend "reject" or "reconsider" (novelty < 40%)

## Quick Start

1. **Collect 10 Diverse Patents**:
   - Search Google Patents for recent patents (2019-2023)
   - Select from different technical fields
   - Record: patent ID, title, abstract, claims (first 2), priority date, publication date

2. **Create source_patents.json**:
```bash
# See patents/source_patents.json for format
```

3. **Generate Training Pairs**:
```bash
python scripts/generate_training_data.py
```

4. **Validate**:
```bash
# Read 2-3 generated IDFs manually
# Ensure they sound like researcher disclosures, not patent language
# Check dates are correct (positive before priority, negative after publication)
```

## Notes

- Each patent yields 2 training examples (1 positive + 1 negative)
- 10 source patents = 20 training examples
- Aim for 80%+ accuracy on this dataset before demo
- This data validates the ENTIRE pipeline from claim extraction to recommendation
