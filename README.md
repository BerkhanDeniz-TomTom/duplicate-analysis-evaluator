# Duplicate Analysis Evaluator

This tool evaluates the accuracy of a duplicate issue detection API by comparing its results against known duplicate relationships and known non-duplicate pairs.

## Overview

The tool consists of three main components:
1. API querying for potential duplicates
2. Result formatting
3. Accuracy validation

## Input

The tool accepts two types of ground truth data:

1. Known duplicates (required) in the format:

```
HCP3EXT-7121 linked as duplicate of HCP3EXT-6767
HCP3EXT-6767 linked as duplicate of HCP3EXT-7121
```

2. Known non-duplicates (optional) in the format:

```
HCP3EXT-7269 confirmed not duplicate of HCP3EXT-7268
HCP3EXT-7268 confirmed not duplicate of HCP3EXT-7190
```

## Usage

Run the main script with your input file:
```bash
# With only known duplicates
python run_duplicate_analysis.py --duplicates actual_duplicates.txt

# With both duplicates and non-duplicates
python run_duplicate_analysis.py --duplicates actual_duplicates.txt --non-duplicates confirmed_non_duplicates.txt
```

## Output

The tool generates:
1. JSON file with API results
2. Text file with formatted duplicate matches
3. Final validation results showing accuracy scores

Example output:
```
Validation Results:
=================

Checking Known Duplicates:

HCP3EXT-7097 -> HCP3EXT-7039: NOT FOUND in detected duplicates
HCP3EXT-7039 -> HCP3EXT-7097: NOT FOUND in detected duplicates
HCP3EXT-7057 -> HCP3EXT-6938: FOUND (match type: d, score: 0.71)
HCP3EXT-6938 -> HCP3EXT-7057: FOUND (match type: a, score: 0.70)

Checking Known Non-Duplicates:

HCP3EXT-7269 -> HCP3EXT-7268: CORRECTLY NOT DETECTED
HCP3EXT-7268 -> HCP3EXT-7190: CORRECTLY NOT DETECTED
HCP3EXT-7265 -> HCP3EXT-6702: CORRECTLY NOT DETECTED
HCP3EXT-7262 -> HCP3EXT-6795: CORRECTLY NOT DETECTED

Summary:
True Positives (correctly detected duplicates): 6
False Negatives (missed duplicates): 17
True Negatives (correctly detected non-duplicates): 9
False Positives (incorrectly flagged as duplicates): 0

Metrics:
Success Rate: 26.1%
Average Score of Found Duplicates: 0.74
```

Where:
- `d` indicates a description-based match
- `a` indicates an analysis-based match
- Score ranges from 0 to 1, higher is better

## Files
- `run_duplicate_analysis.py`: Main script that orchestrates the analysis
- `api_test_tool.py`: Queries the duplicate detection API
- `format_duplicates.py`: Formats API results
- `validate_duplicates.py`: Validates results against known duplicates