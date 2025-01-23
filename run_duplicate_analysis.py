import subprocess
import argparse
import os
from datetime import datetime
import glob

def run_pipeline(duplicates_file, non_duplicates_file=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    working_dir = f"duplicate_analysis_{timestamp}"
    
    # Create working directory for intermediate files
    os.makedirs(working_dir, exist_ok=True)
    
    print("\n=== Starting Duplicate Analysis Pipeline ===\n")
    
    # Define intermediate file paths
    api_results = os.path.join(working_dir, f"results_{timestamp}.json")
    detected_duplicates = os.path.join(working_dir, "duplicates.txt")
    validation_results = os.path.join(working_dir, "validation_results.txt")
    
    # Step 1: Query API for issues
    print("Step 1: Querying API for issues...")
    cmd = ["python", "api_test_tool.py", "--output-file", api_results]
    if duplicates_file:
        cmd.extend(["--duplicates", duplicates_file])
    if non_duplicates_file:
        cmd.extend(["--non-duplicates", non_duplicates_file])
    subprocess.run(cmd, check=True)
    
    # Step 2: Format duplicate detection results
    print("\nStep 2: Processing duplicate detection results...")
    subprocess.run([
        "python", "format_duplicates.py",
        "--input-file", api_results,
        "--output", detected_duplicates
    ], check=True)
    
    # Step 3: Validate against both actual duplicates and non-duplicates
    print("\nStep 3: Validating results...")
    cmd = [
        "python", "validate_duplicates.py",
        "--detected", detected_duplicates,
        "--output", validation_results
    ]
    if duplicates_file:
        cmd.extend(["--actual", duplicates_file])
    if non_duplicates_file:
        cmd.extend(["--non-duplicates", non_duplicates_file])
    
    subprocess.run(cmd, check=True)
    
    # Copy final results to current directory
    final_output = f"duplicate_analysis_results_{timestamp}.txt"
    with open(validation_results, 'r') as src, open(final_output, 'w') as dst:
        dst.write(src.read())
    
    print(f"\n=== Analysis Complete ===")
    print(f"Final results written to: {final_output}")
    print(f"All intermediate files are in: {working_dir}")

def main():
    parser = argparse.ArgumentParser(description='Duplicate Issue Analysis Pipeline')
    parser.add_argument('--duplicates', required=True, 
                       help='Input file containing known duplicate links')
    parser.add_argument('--non-duplicates', 
                       help='Input file containing known non-duplicate pairs')
    args = parser.parse_args()
    
    run_pipeline(args.duplicates, args.non_duplicates)

if __name__ == '__main__':
    main()