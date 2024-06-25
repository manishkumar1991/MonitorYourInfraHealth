import sys
import requests
from azure.identity import DefaultAzureCredential
import os

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    print(f"Content of {file_path}:\n{content}")
    
def get_access_token():
    credential = DefaultAzureCredential()
    token = credential.get_token('https://management.azure.com/.default')
    return token.token    

if __name__ == "__main__":
    file_path = sys.argv[1]
    read_file(file_path)
    access_token = get_access_token()
    print(access_token)
