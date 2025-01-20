# Duplicate Analysis Evaluator

This tool evaluates the accuracy of the duplicate issue detection service by comparing its results against known duplicates.

## Overview

The tool consists of three main components:
1. API querying for potential duplicates
2. Result formatting
3. Accuracy validation

## Input

The tool takes a text file containing known duplicate relationships in the format:
```
HCP3EXT-7121 linked as duplicate of HCP3EXT-6767
HCP3EXT-6767 linked as duplicate of HCP3EXT-7121
```

## Usage

Run the main script with your input file:
```bash
python run_duplicate_analysis.py --input-file actual_duplicates.txt
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

HCP3EXT-7097 -> HCP3EXT-7039: NOT FOUND in detected duplicates
HCP3EXT-7039 -> HCP3EXT-7097: NOT FOUND in detected duplicates
HCP3EXT-7057 -> HCP3EXT-6938: FOUND (match type: d, score: 0.71)
HCP3EXT-6938 -> HCP3EXT-7057: FOUND (match type: a, score: 0.70)

Summary:
Found: 6 out of 23 duplicates
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