# Backend Scripts

This directory contains utility scripts for the Auto-Prior Art Analyst backend.

## Scripts

### generate_training_data.py

Generates synthetic training data by reverse-engineering real patents into Invention Disclosure Forms (IDFs).

**Purpose:**
- Create realistic test data with known ground truth
- Validate the entire analysis pipeline
- Ensure 80%+ accuracy before demo/production

**How it works:**
1. Reads patent data from `../training_data/patents/source_patents.json`
2. Uses watsonx.ai to convert formal patent language → researcher-friendly disclosure
3. Creates 2 examples per patent:
   - **Positive (Novel)**: Search date before priority → expects no matches
   - **Negative (Not Novel)**: Search date after publication → expects to find source patent
4. Saves pairs to `../training_data/pairs/`

**Usage:**

```bash
# From backend directory
python scripts/generate_training_data.py
```

**Requirements:**
- watsonx.ai credentials in `.env` (WATSONX_API_KEY, WATSONX_URL, WATSONX_PROJECT_ID)
- Source patent data in `training_data/patents/source_patents.json`

**Output:**
- `training_data/pairs/pair_001_positive.json`
- `training_data/pairs/pair_001_negative.json`
- `training_data/pairs/pair_002_positive.json`
- ...

**Recommended Workflow:**

1. **Collect 10 Diverse Patents** from Google Patents:
   - 3 battery/energy (H01M)
   - 3 pharma/biotech (A61K)
   - 2 software/ML (G06N)
   - 2 mechanical/device (F16, G01)

2. **Create source_patents.json**:
```json
[
  {
    "id": "battery_001",
    "patent_number": "US10234567B2",
    "title": "Lithium-ion battery with improved electrolyte",
    "abstract": "A lithium-ion battery comprising...",
    "claims": [
      "1. A lithium-ion battery comprising...",
      "2. The battery of claim 1, wherein..."
    ],
    "priority_date": "2019-03-15",
    "publication_date": "2020-04-20",
    "ipc_codes": ["H01M10/05"]
  }
]
```

3. **Run the script**:
```bash
python scripts/generate_training_data.py
```

4. **Validate output**:
   - Read 2-3 generated IDFs manually
   - Check they sound like researcher disclosures (not patent legalese)
   - Verify dates: positive < priority, negative > publication

5. **Test the pipeline**:
```bash
# Use generated data to test analysis workflow
pytest tests/ --training-data
```

**Expected Results:**
- 10 source patents → 20 training examples (10 positive + 10 negative)
- Positive examples: novelty > 70%, recommendation = "pursue"
- Negative examples: novelty < 40%, recommendation = "reject", source patent found

**Troubleshooting:**

**Error: "Patents file not found"**
- Create `training_data/patents/source_patents.json`
- See `training_data/README.md` for format

**Error: "WATSONX_API_KEY not set"**
- Add credentials to `.env` file
- Or use stub mode (will generate basic templates)

**Generated IDFs don't look good**
- Check watsonx.ai model settings (try different models)
- Adjust temperature in script (currently 0.5)
- Improve prompt engineering in `reverse_engineer_to_idf()`

**Patent dates invalid**
- Ensure dates are in YYYY-MM-DD format
- Check that publication_date > priority_date
- Script will use fallback dates if parsing fails

## Future Scripts

Other scripts that could be added:

- `validate_training_data.py` - Test analysis accuracy on training pairs
- `analyze_batch.py` - Batch process multiple disclosures
- `export_results.py` - Export analysis results to CSV/Excel
- `benchmark_performance.py` - Measure analysis speed and accuracy

## Development

To add a new script:

1. Create the script in this directory
2. Add documentation to this README
3. Use the app modules via `sys.path` (see generate_training_data.py)
4. Include proper logging and error handling
5. Provide usage examples and troubleshooting

## Notes

- All scripts should be runnable from the `backend/` directory
- Use absolute paths or Path objects for file operations
- Include comprehensive error handling
- Log progress and results for debugging
- Make scripts idempotent when possible (safe to re-run)
