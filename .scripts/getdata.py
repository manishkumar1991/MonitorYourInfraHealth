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
    headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
    }
    url = "https://management.azure.com/subscriptions/f70efef4-6505-4727-acd8-9d0b3bc0b80e/resourcegroups?api-version=2021-04-01"
    response = requests.get(url, headers=headers)
    print(response.json())
