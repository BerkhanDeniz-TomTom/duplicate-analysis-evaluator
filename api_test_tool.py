import requests
import json
import argparse
from datetime import datetime

def query_api(issue_key):
    url = "http://10.128.4.180:8201/query/"
    payload = {"issue_key": issue_key}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Create combined result with input key
        result = {
            "input": {
                "processed_description": data.get("input_processed_description", ""),
                "jira_analysis_finding": data.get("input_jira_analysis_finding", "")
            },
            "description_match_results": data.get("description_match_results", []),
            "analysis_finding_match_results": data.get("analysis_finding_match_results", [])
        }
        return result
    except Exception as e:
        return {
            "input": None,
            "error": str(e)
        }

def get_issue_keys_from_file(filename, relationship_text):
    """Extract issue keys from file based on relationship text."""
    issue_keys = set()  # Using set to avoid duplicates
    with open(filename, 'r') as f:
        for line in f:
            if relationship_text in line:
                parts = line.split(relationship_text)
                source = parts[0].strip()
                target = parts[1].strip().rstrip(',')
                issue_keys.add(source)
                issue_keys.add(target)
    return issue_keys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--duplicates', help='File containing known duplicate links')
    parser.add_argument('--non-duplicates', help='File containing known non-duplicate pairs')
    parser.add_argument('--output-file', required=True, help='Output JSON file for results')
    args = parser.parse_args()

    # Collect all unique issue keys from both files
    all_issue_keys = set()

    if args.duplicates:
        duplicate_keys = get_issue_keys_from_file(args.duplicates, 'linked as duplicate of')
        all_issue_keys.update(duplicate_keys)

    if args.non_duplicates:
        non_duplicate_keys = get_issue_keys_from_file(args.non_duplicates, 'confirmed not duplicate of')
        all_issue_keys.update(non_duplicate_keys)

    # Convert set to sorted list for consistent processing
    issue_keys = sorted(all_issue_keys)
    
    if not issue_keys:
        print("No issue keys found in input files!")
        return
    
    # Process each issue key
    results = {}
    for issue_key in issue_keys:
        print(f"Processing {issue_key}")
        result = query_api(issue_key)
        results[issue_key] = result
    
    # Write results to file
    with open(args.output_file, 'w') as f:
        json.dump(results, f, indent=2, sort_keys=True)
    
    print(f"Results written to {args.output_file}")

if __name__ == '__main__':
    main()