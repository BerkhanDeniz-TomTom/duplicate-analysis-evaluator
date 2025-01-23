import json
import argparse
from collections import defaultdict

def parse_actual_duplicates(filename):
    duplicates = []
    with open(filename, 'r') as f:
        for line in f:
            if 'linked as duplicate of' in line:
                source, target = line.strip().split(' linked as duplicate of ')
                duplicates.append((source.strip(), target.strip().rstrip(',')))
    return duplicates

def parse_non_duplicates(filename):
    non_duplicates = []
    with open(filename, 'r') as f:
        for line in f:
            if 'confirmed not duplicate of' in line:
                source, target = line.strip().split(' confirmed not duplicate of ')
                non_duplicates.append((source.strip(), target.strip().rstrip(',')))
    return non_duplicates

def parse_detected_duplicates(filename):
    direct_matches = {}
    scores = {}
    
    with open(filename, 'r') as f:
        for line in f:
            if 'is a possible duplicate of' in line:
                parts = line.strip().split(' is a possible duplicate of ')
                source = parts[0]
                matches = parts[1].split(', ')
                
                direct_matches[source] = []
                for match in matches:
                    target = match.split(' (')[0]
                    score_type = match.split('(')[1].split(':')[0]
                    score = float(match.split(':')[1].rstrip(')'))
                    
                    direct_matches[source].append(target)
                    scores[(source, target)] = (score_type, score)
    
    return direct_matches, scores

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--actual', help='File with actual duplicate links')
    parser.add_argument('--non-duplicates', help='File with confirmed non-duplicate pairs')
    parser.add_argument('--detected', help='File with detected duplicate links')
    parser.add_argument('--output', help='Output file for validation results')
    args = parser.parse_args()

    # Parse files
    actual_duplicates = parse_actual_duplicates(args.actual)
    direct_matches, scores = parse_detected_duplicates(args.detected)
    
    # Initialize results
    results = []
    found_count = 0
    total_count = len(actual_duplicates)
    found_scores = []
    
    # Check positive examples (duplicates)
    results.append("Checking Known Duplicates:\n")
    for source, target in actual_duplicates:
        if source in direct_matches and target in direct_matches[source]:
            found_count += 1
            score_type, score = scores[(source, target)]
            found_scores.append(score)
            results.append(f"{source} -> {target}: FOUND (match type: {score_type}, score: {score:.2f})")
        else:
            results.append(f"{source} -> {target}: NOT FOUND in detected duplicates")

    # Calculate metrics for duplicates
    true_positives = found_count
    false_negatives = total_count - found_count
    
    # Check negative examples if provided
    false_positives = 0
    true_negatives = 0
    if args.non_duplicates:
        non_duplicates = parse_non_duplicates(args.non_duplicates)
        results.append("\nChecking Known Non-Duplicates:\n")
        for source, target in non_duplicates:
            if source in direct_matches and target in direct_matches[source]:
                false_positives += 1
                score_type, score = scores[(source, target)]
                results.append(f"{source} -> {target}: INCORRECTLY DETECTED (match type: {score_type}, score: {score:.2f})")
            else:
                true_negatives += 1
                results.append(f"{source} -> {target}: CORRECTLY NOT DETECTED")

    # Calculate metrics
    success_rate = (found_count / total_count) * 100 if total_count > 0 else 0
    avg_score = sum(found_scores) / len(found_scores) if found_scores else 0
    
    # Write results
    with open(args.output, 'w') as f:
        f.write("Validation Results:\n")
        f.write("=================\n\n")
        for result in results:
            f.write(result + '\n')
        
        f.write(f"\nSummary:\n")
        f.write(f"True Positives (correctly detected duplicates): {true_positives}\n")
        f.write(f"False Negatives (missed duplicates): {false_negatives}\n")
        if args.non_duplicates:
            f.write(f"True Negatives (correctly detected non-duplicates): {true_negatives}\n")
            f.write(f"False Positives (incorrectly flagged as duplicates): {false_positives}\n")
        f.write(f"\nMetrics:\n")
        f.write(f"Success Rate: {success_rate:.1f}%\n")
        if found_scores:
            f.write(f"Average Score of Found Duplicates: {avg_score:.2f}\n")
    
    print(f"Validation results written to {args.output}")

if __name__ == '__main__':
    main()