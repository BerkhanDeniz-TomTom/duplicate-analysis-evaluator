import subprocess
import argparse
import os
from datetime import datetime
import glob

def run_pipeline(input_file):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    working_dir = f"duplicate_analysis_{timestamp}"
    
    # Create working directory for intermediate files
    os.makedirs(working_dir, exist_ok=True)
    
    print("\n=== Starting Duplicate Analysis Pipeline ===\n")
    
    # Step 1: Query API for each issue
    print("Step 1: Querying API for issues...")
    subprocess.run([
        "python", "api_test_tool.py",
        "--input-file", input_file
    ], check=True)
    
    # Get the most recent results file
    results_files = glob.glob('results_*.json')
    if not results_files:
        raise Exception("No results file found from API query")
    
    latest_results = max(results_files, key=os.path.getctime)
    api_results = os.path.join(working_dir, latest_results)
    
    # Move the file to working directory
    os.rename(latest_results, api_results)
    
    detected_duplicates = os.path.join(working_dir, "duplicates.txt")
    validation_results = os.path.join(working_dir, "validation_results.txt")
    
    # Step 2: Format duplicate detection results
    print("\nStep 2: Processing duplicate detection results...")
    subprocess.run([
        "python", "format_duplicates.py",
        "--input-file", api_results,
        "--output", detected_duplicates
    ], check=True)
    
    # Step 3: Validate against actual duplicates
    print("\nStep 3: Validating results...")
    subprocess.run([
        "python", "validate_duplicates.py",
        "--actual", input_file,
        "--detected", detected_duplicates,
        "--output", validation_results
    ], check=True)
    
    # Copy final results to current directory
    final_output = f"duplicate_analysis_results_{timestamp}.txt"
    with open(validation_results, 'r') as src, open(final_output, 'w') as dst:
        dst.write(src.read())
    
    print(f"\n=== Analysis Complete ===")
    print(f"Final results written to: {final_output}")
    print(f"All intermediate files are in: {working_dir}")

def main():
    parser = argparse.ArgumentParser(description='Duplicate Issue Analysis Pipeline')
    parser.add_argument('--input-file', required=True, 
                       help='Input file containing actual duplicate links')
    args = parser.parse_args()
    
    run_pipeline(args.input_file)

if __name__ == '__main__':
    main()