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