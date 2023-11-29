#!/usr/bin/env python3

import requests
import os
import sys
from datetime import datetime

# Replace this with your actual Heroku app URL
HEROKU_APP_URL = 'https://tracability-project-c8e1a60af229.herokuapp.com'

def upload_file_to_heroku(file_path):
    upload_url = f'{HEROKU_APP_URL}/upload'

    # Upload the file to the specified endpoint
    files = {'file': open(file_path, 'rb')}
    response = requests.post(upload_url, files=files)

    if response.status_code == 200:
        print(f"File uploaded successfully.{files}")
    else:
        print(f"Error uploading file. Status code: {response.status_code}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    upload_file_to_heroku(file_path)