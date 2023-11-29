#!/usr/bin/env python3

import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    # If the user does not select a file, browser submits an empty part without filename
    if file.filename == '':
        return render_template('index.html', error='No selected file')

    # If the file is allowed and is successfully uploaded
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return render_template('index.html', success='File uploaded successfully', filename=filename)

    return render_template('index.html', error='Invalid file type')

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    # Ensure the 'uploads' folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)