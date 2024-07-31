import requests
import yaml
import re
import os
import subprocess
import csv

def get_modified_files(current_directory):

    # Add upstream remote if not already present
    git_remote_command = "git remote"
    remote_result = subprocess.run(git_remote_command, shell=True, text=True, capture_output=True, check=True)
    if 'upstream' not in remote_result.stdout.split():
        git_add_upstream_command = f"git remote add upstream '{SentinelRepoUrl}'"
        subprocess.run(git_add_upstream_command, shell=True, text=True, capture_output=True, check=True)
    # Fetch from upstream
    git_fetch_upstream_command = "git fetch upstream"
    subprocess.run(git_fetch_upstream_command, shell=True, text=True, capture_output=True, check=True)
    cmd = f"git diff --name-only upstream/master {current_directory}/../../../Parsers/"
    try:
        return subprocess.check_output(cmd, shell=True).decode().split("\n")
    except subprocess.CalledProcessError as e:
        print(f"::error::Error occurred while executing the command: {e}")
        return []

def get_current_commit_number():
    cmd = "git rev-parse HEAD"
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except subprocess.CalledProcessError as e:
        print(f"::error::Error occurred while executing the command: {e}")
        return None

def filter_yaml_files(modified_files):
    # Take only the YAML files
    return [line for line in modified_files if line.endswith('.yaml')]


SentinelRepoUrl = "https://github.com/Azure/Azure-Sentinel.git"
current_directory = os.path.dirname(os.path.abspath(__file__))
modified_files = get_modified_files(current_directory)
commit_number = get_current_commit_number()
parser_yaml_files = filter_yaml_files(modified_files)
print("Following files were found to be modified:")
for file in parser_yaml_files:
    print(f"{file}")
