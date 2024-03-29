#!/bin/bash

# Update package list
echo "Updating package lists..."
sudo apt-get update -y

# Install Python 3 and pip
echo "Installing Python 3 and pip..."
sudo apt-get install -y python3 python3-pip

# Install QR code library
echo "Installing qrcode library..."
pip3 install qrcode[pil]

# Install XlsxWriter library
echo "Installing XlsxWriter library..."
pip3 install xlsxwriter

# Install Openyxl library
echo "Installing Openpyxl..."
pip3 install openpyxl

# Install Opencv and pyzbar libraries
echo "Installing pyzbar"
sudo apt install libzbar0
pip3 install pyzbar opencv-python


# Install libraries for website
pip3 install pandas flask werkzeug.utils

# Install Gunicorn
pip3 install gunicorn

# Install needed CLI for cloud stroage of data
sudo curl https://cli-assets.heroku.com/install-ubuntu.sh | sh