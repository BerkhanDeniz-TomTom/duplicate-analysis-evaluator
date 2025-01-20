import json
import argparse
from datetime import datetime

def format_duplicates(results_data):
    output_lines = []
    
    for issue_key, data in results_data.items():
        # Collect all matches with their scores and types
        matches = []
        
        # Add description matches
        for match in data.get('description_match_results', []):
            matches.append((match['issue_key'], match['score'], 'd'))
            
        # Add analysis matches
        for match in data.get('analysis_finding_match_results', []):
            matches.append((match['issue_key'], match['score'], 'a'))
        
        # Sort by score in descending order
        matches.sort(key=lambda x: x[1], reverse=True)
        
        # Format the matches
        if matches:
            matches_str = ', '.join([f"{m[0]} ({m[2]}:{m[1]:.2f})" for m in matches])
            line = f"{issue_key} is a possible duplicate of {matches_str}"
            output_lines.append(line)
    
    return output_lines

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', help='Input JSON file with results')
    parser.add_argument('--output-file', help='Output text file for formatted results')
    args = parser.parse_args()

    # Read JSON file
    with open(args.input_file, 'r') as f:
        results = json.load(f)
    
    # Format the results
    output_lines = format_duplicates(results)
    
    # Write to output file
    with open(args.output_file, 'w') as f:
        for line in output_lines:
            f.write(line + '\n')
    
    print(f"Results written to {args.output_file}")

if __name__ == '__main__':
    main()