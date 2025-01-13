import requests
import json
import argparse
from datetime import datetime

def query_api(issue_key):
    url = "http://10.128.4.180:8200/query/"
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', help='File containing issue keys')
    args = parser.parse_args()

    # Read issue keys from file
    with open(args.input_file, 'r') as f:
        issue_keys = [line.strip() for line in f if line.strip()]
    
    # Process each issue key
    results = {}
    for issue_key in issue_keys:
        print(f"Processing {issue_key}")
        result = query_api(issue_key)
        results[issue_key] = result
    
    # Write results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"results_{timestamp}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, sort_keys=True)
    
    print(f"Results written to {output_file}")

if __name__ == '__main__':
    main()