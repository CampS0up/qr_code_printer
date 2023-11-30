#!/usr/bin/env python3

import os
from flask import Flask, render_template, send_from_directory
from datetime import datetime

app = Flask(__name__)

# Set the upload folder
UPLOAD_FOLDER = 'day'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_today_folder():
    today_folder = os.path.join(app.config['UPLOAD_FOLDER'], datetime.today().strftime('%Y-%m-%d'))
    os.makedirs(today_folder, exist_ok=True)
    return today_folder

@app.route('/')
def index():
    today_folder = get_today_folder()
    uploaded_files = os.listdir(today_folder)
    return render_template('index.html', uploaded_files=uploaded_files)

@app.route('/days')
def list_days():
    all_days = sorted([d for d in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], d))], reverse=True)
    return render_template('days.html', all_days=all_days)

@app.route('/day/<day>')
def view_day(day):
    day_folder = os.path.join(app.config['UPLOAD_FOLDER'], day)

    if not os.path.exists(day_folder) or not os.path.isdir(day_folder):
        return f"Error: Day folder '{day}' does not exist."

    # Optionally, you can list the files for the day
    uploaded_files = os.listdir(day_folder)

    return render_template('day.html', day=day, uploaded_files=uploaded_files)

@app.route('/download/<day>/<filename>')
def download_file(day, filename):
    day_folder = os.path.join(app.config['UPLOAD_FOLDER'], day)
    file_path = os.path.join(day_folder, filename)
    return send_from_directory(day_folder, filename, as_attachment=True)

if __name__ == '__main__':
    # Ensure the 'uploads' folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Run the Flask application on 0.0.0.0 (all available network interfaces) and port 5001
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)