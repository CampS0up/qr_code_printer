#!/usr/bin/env python3

import os
import sys
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_today_folder():
    today_folder = os.path.join(app.config['UPLOAD_FOLDER'], datetime.today().strftime('%Y-%m-%d'))
    os.makedirs(today_folder, exist_ok=True)
    return today_folder

def upload_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(get_today_folder(), filename)
        file.save(file_path)
        return f"File '{filename}' uploaded successfully"
    else:
        return "Error: Invalid file or file type"

@app.route('/')
def index():
    today_folder = get_today_folder()
    uploaded_files = os.listdir(today_folder)
    return render_template('index.html', uploaded_files=uploaded_files)

@app.route('/upload', methods=['POST'])
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

@app.route('/day/<day>')
def view_day(day):
    day_folder = get_today_folder()
    uploaded_files = os.listdir(day_folder)
    return render_template('day.html', day=day, uploaded_files=uploaded_files)

if __name__ == '__main__':
    # Ensure the 'uploads' folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Run the Flask application on 0.0.0.0 (all available network interfaces) and port 5001
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)