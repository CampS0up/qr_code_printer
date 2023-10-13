#!/usr/bin/env python3

import cv2 
import sys
import pyzbar.pyzbar as pyzbar

# Setup camera capture
cap = cv2.VideoCapture(1)
cap.open(1)
cap.set(3, 640)  # set width
cap.set(4, 480)  # set height
# Check if argument is true
if sys.argv[1] == "true":
    while True:
        # Read frame from camera
        ret, img = cap.read()
        # Decode QR code or barcode
        codes = pyzbar.decode(img)
        for code in codes:
            type = code.type
            if type == "QRCODE":
                print(code.data.decode('utf-8'))
            if type == "BARCODE":
                print ("BAR")
        # Display image
        cv2.imshow('test', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    # Read image file
    img = cv2.imread('qr_code.png')
    # Decode QR code or barcode
    try:
        codes = pyzbar.decode(img)
        for code in codes:
            type = code.type
            if type == "QRCODE":
                print(code.data.decode('utf-8'))
            if type == "BARCODE":
                print ("BAR")
    except:
        print("No QR code or barcode found")
# Release camera
cap.release()
# Destroy all windows
cv2.destroyAllWindows()
