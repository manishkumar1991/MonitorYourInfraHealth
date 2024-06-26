import sys
import requests
from azure.identity import DefaultAzureCredential
import os

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    print(f"Content of {file_path}:\n{content}") 

if __name__ == "__main__":
    file_path = sys.argv[1]
    if "Schema" in file_path:
        print(f"Schema file found at {file_path}")
