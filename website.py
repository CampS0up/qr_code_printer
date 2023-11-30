#!/usr/bin/env python3

import os
import sys
from flask import Flask, render_template, request, send_from_directory, send_file
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'day'
ALLOWED_EXTENSIONS = {'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_today_folder():
    today_folder = os.path.join(app.config['UPLOAD_FOLDER'], datetime.today().strftime('%Y-%m-%d'))
    os.makedirs(today_folder, exist_ok=True)
    return today_folder

def upload_file(file):
    if allowed_file(file.name):  # Use file.name instead of file.filename
        original_filename = secure_filename(file.name)

        # Remove the prefix "excel_data_" if it exists
        prefix = "excel_data_"
        if original_filename.startswith(prefix):
            original_filename = original_filename[len(prefix):]

        filename, file_extension = os.path.splitext(original_filename)
        filename = f"{filename}{file_extension}"
        file_path = os.path.join(get_today_folder(), filename)
        with open(file_path, 'wb') as f:
            f.write(file.read())
        return f"File '{filename}' uploaded successfully"
    else:
        return "Error: Invalid file or file type"

def process_command_line_argument():
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    result = upload_file(file)
                    print(result)
            else:
                print("Error: Provided path is a directory, not a file.")
        else:
            print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("Usage: ./website.py <file.xlsx>")
        sys.exit(1)

@app.route('/')
def index():
    today_folder = get_today_folder()
    uploaded_files = os.listdir(today_folder)
    return render_template('index.html', uploaded_files=uploaded_files)

@app.route('/uploads', methods=['POST'])
def upload_file_web():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    # If the user does not select a file, browser submits an empty part without filename
    if file.filename == '':
        return render_template('index.html', error='No selected file')

    result = upload_file(file)
    return render_template('index.html', message=result)

@app.route('/download/<filename>')
def download_file(filename):
    today_folder = get_today_folder()
    file_path = os.path.join(today_folder, filename)
    return send_from_directory(today_folder, filename, as_attachment=True)

@app.route('/days')
def list_days():
    all_days = sorted([d for d in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], d))], reverse=True)
    return render_template('days.html', all_days=all_days)

@app.route('/day/<day>', methods=['GET', 'POST'])
def view_day(day):
    if request.method == 'GET':
        # Handle GET requests (display page, list files, etc.)
        day_folder = os.path.join(app.config['UPLOAD_FOLDER'], day)
        uploaded_files = os.listdir(day_folder)
        return render_template('day.html', day=day, uploaded_files=uploaded_files)
    elif request.method == 'POST':
        # Handle POST requests (file upload)
        return handle_day(day)

def handle_day(day):
    day_folder = os.path.join(app.config['UPLOAD_FOLDER'], day)

    if not os.path.exists(day_folder) or not os.path.isdir(day_folder):
        return f"Error: Day folder '{day}' does not exist."

    if request.method == 'GET':
        # Handle GET requests (display page, list files, etc.)
        uploaded_files = os.listdir(day_folder)
        return render_template('day.html', day=day, uploaded_files=uploaded_files)
    elif request.method == 'POST':
        # Handle POST requests (file upload)
        if 'file' not in request.files:
            return "No file part"

        file = request.files['file']

        if file.filename == '':
            return "No selected file"

        # Save the file to the day folder
        file.save(os.path.join(day_folder, secure_filename(file.filename)))

        # Optionally, you can list the files after the upload
        uploaded_files = os.listdir(day_folder)

        return f"File uploaded successfully to {day}"

if __name__ == '__main__':
    # Ensure the 'uploads' folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Process command line argument if provided
    process_command_line_argument()

    # Run the Flask application on 0.0.0.0 (all available network interfaces) and port 5001
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)