import sys
import os
import subprocess

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    GetModifiedFiles = f'git diff --name-only origin/main "{current_directory}/../../../Sample Data/ASIM/"'
    try:
        modified_files = subprocess.run(GetModifiedFiles, shell=True, text=True, capture_output=True, check=True)
        print(modified_files.stdout.splitlines())
    except subprocess.CalledProcessError as e:
        print(f"::error::An error occurred while executing the command: {e}")
        sys.stdout.flush()  # Explicitly flush stdout
    
