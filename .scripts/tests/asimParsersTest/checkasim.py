import requests
import yaml
import re
import os
import subprocess
import csv
from datetime import datetime
from urllib.parse import urlparse
from tabulate import tabulate

# Constants
SENTINEL_REPO_RAW_URL = f'https://raw.githubusercontent.com/manishkumar1991/MonitorYourInfraHealth'
SAMPLE_DATA_PATH = '/Sample%20Data/ASIM/'

def get_current_commit_number():
    cmd = "git rev-parse HEAD"
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except subprocess.CalledProcessError as e:
        print(f"::error::Error occurred while executing the command: {e}")
        return None

commit_number = get_current_commit_number()
sample_data_url = f'{SENTINEL_REPO_RAW_URL}/{commit_number}/{SAMPLE_DATA_PATH}'
SampleDataFile = 'Crowd_falcon_asimnetwork_IngestedLogs.csv'
SampleDataUrl = sample_data_url+SampleDataFile
response = requests.get(SampleDataUrl)
if response.status_code == 200:
  print(f"file found at {SampleDataUrl}")
else:
  print(f"No file found at {SampleDataUrl}")
