#!/usr/bin/env python3

import requests
import os
import sys
from datetime import datetime

# Replace this with your actual Heroku app URL
HEROKU_APP_URL = 'https://tracability-project-c8e1a60af229.herokuapp.com'

def upload_file_to_heroku(file_path):
    # Use the current date as the folder name
    current_date_folder = datetime.today().strftime('%Y-%m-%d')

    # Ensure the folder structure exists on Heroku
    upload_url = f'{HEROKU_APP_URL}/day/{current_date_folder}'
    response = requests.get(upload_url)

    # Upload the file to the specified folder on Heroku
    files = {'file': open(file_path, 'rb')}
    response = requests.post(upload_url, files=files)

    if response.status_code == 200:
        print(f"File uploaded successfully to Heroku.")

    else:
        print(f"Error uploading file to Heroku. Status code: {response.status_code}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    upload_file_to_heroku(file_path)