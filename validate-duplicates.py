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

def parse_detected_duplicates(filename):
    graph = defaultdict(list)
    scores = {}
    
    with open(filename, 'r') as f:
        for line in f:
            if 'is a possible duplicate of' in line:
                parts = line.strip().split(' is a possible duplicate of ')
                source = parts[0]
                matches = parts[1].split(', ')
                
                for match in matches:
                    # Extract issue key and score from format: HCP3EXT-XXXX (d:0.77)
                    target = match.split(' (')[0]
                    score_type = match.split('(')[1].split(':')[0]
                    score = float(match.split(':')[1].rstrip(')'))
                    
                    graph[source].append(target)
                    scores[(source, target)] = (score_type, score)
    
    return graph, scores

def find_path(graph, start, end, path=None, visited=None):
    if path is None:
        path = []
    if visited is None:
        visited = set()
        
    path = path + [start]
    visited.add(start)
    
    if start == end:
        return path
    
    for next_node in graph[start]:
        if next_node not in visited:
            new_path = find_path(graph, next_node, end, path, visited)
            if new_path:
                return new_path
    
    return None

def format_path_with_scores(path, scores):
    if len(path) < 2:
        return ""
        
    result = []
    for i in range(len(path)-1):
        score_type, score = scores.get((path[i], path[i+1]), ('?', 0.0))
        result.append(f"{path[i]}->{path[i+1]}({score_type}:{score:.2f})")
    
    return " -> ".join(result)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--actual', help='File with actual duplicate links')
    parser.add_argument('--detected', help='File with detected duplicate links')
    parser.add_argument('--output', help='Output file for validation results')
    args = parser.parse_args()

    # Parse both files
    actual_duplicates = parse_actual_duplicates(args.actual)
    graph, scores = parse_detected_duplicates(args.detected)
    
    # Validate each actual duplicate
    results = []
    found_count = 0
    total_count = len(actual_duplicates)
    
    for source, target in actual_duplicates:
        path = find_path(graph, source, target)
        
        if path:
            found_count += 1
            chain = format_path_with_scores(path, scores)
            results.append(f"{source} -> {target}: FOUND via chain: {chain}")
        else:
            results.append(f"{source} -> {target}: NOT FOUND in detected duplicates")
    
    # Calculate percentage
    success_rate = (found_count / total_count) * 100 if total_count > 0 else 0
    
    # Write results
    with open(args.output, 'w') as f:
        f.write("Validation Results:\n")
        f.write("=================\n\n")
        for result in results:
            f.write(result + '\n')
        
        f.write(f"\nSummary:\n")
        f.write(f"Found: {found_count} out of {total_count} duplicates\n")
        f.write(f"Success Rate: {success_rate:.1f}%\n")
    
    print(f"Validation results written to {args.output}")

if __name__ == '__main__':
    main()