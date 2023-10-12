#!/usr/bin/env python3

import qrcode
from PIL import Image, ImageDraw, ImageFont
import time
import xlsxwriter
import os
import sys
import datetime
from datetime import datetime

def generate_qr_code(name_of_part, date, part_num, badge_number):
    # Create a QR code object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to the QR code object
    qr.add_data(f"{name_of_part},{date},{part_num},{badge_number}")
    qr.make(fit=True)

    # Create an image object from the QR code object
    img = qr.make_image(fill_color="black", back_color="white")

    # Get the width and height of the image object
    width, height = img.size

    # Create a new image object with the size of the QR code and the name of the part
    new_img = Image.new("RGB", (width, height + 20), (255, 255, 255))

    # Paste the QR code image onto the new image object
    new_img.paste(img, (0, 20))

    # Create a text object with the name of the part.
    text = Image.new("RGB", (width, 35), (255, 255, 255))
    draw = ImageDraw.Draw(text)
    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 24)
    draw.text(((width-len(name_of_part)*12)/2, 10), name_of_part, font=font, fill=(0, 0, 0))

    # Paste the text object onto the new image object
    new_img.paste(text, (0, 0))

    # Save the new image object as a PNG file
    new_img.save("qr_code.png")



def add_data_to_excel(name_of_part, date, part_number, badge_number):
    workbook = xlsxwriter.Workbook('data.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'Name of Part')
    worksheet.write('B1', 'Date')
    worksheet.write('C1', 'Part Number')
    worksheet.write('D1', 'Badge Number')

    row = 1
    col = 0

    worksheet.write(row, col,     name_of_part)
    worksheet.write(row, col + 1, date)
    worksheet.write(row, col + 2, part_number)
    worksheet.write(row, col + 3, badge_number)

    workbook.close()

def print_qr_code():
    os.system("lp -d 'Printer Name' qr_code.png")

    # Example usage
    #generate_qr_code("Part Name", time.strftime("%m.%d.%Y"), 1, 12345)
    #add_data_to_excel("Part Name", time.strftime("%m.%d.%Y"), 1, 12345)
    #print_qr_code()

def get_date():
    # Get the current date and time
    current_date_time = datetime.now()
    # Format the date as 'mmddyyyy'
    formatted_date = current_date_time.strftime('%m%d%Y')
    return formatted_date

def generate_part_number():
    # Get the current date.
    today = get_date()
    
    # Open the log file to read the previous part numbers
    with open('log.txt', 'r') as file:
        lines = file.readlines()
    
    # Check if a part has been made for that date
    sequence_number = 0
    for line in lines:
        if today in line:
            sequence_number = int(line.split()[-1]) + 1
            break
    
    # Generate the part number
    part_number = today + '0000'.zfill(4 - len(str(sequence_number))) + str(sequence_number)
    
    # Write the new part number to the log file
    with open('log.txt', 'a') as file:
        file.write(f"{today} {sequence_number}\n")
    
    # Return the part number.
    return part_number
def main():
    if len(sys.argv) < 2:
        print("Usage: python qrcode.py generate|all")
        return

    command = sys.argv[1]
    name = input("lol")
    date = get_date()
    part_num = generate_part_number()
    badge_number = 1
    if command == "generate":
        generate_qr_code(name, date, part_num, badge_number)
        print("QR code generated successfully.")
    elif command == "excel":
        add_data_to_excel(name, date, part_num, badge_number)
        print("Data added successfully.")
    elif command == "all":
        print("This command will do all the tasks.")
    else:
        print("Invalid command. Please use 'generate' or 'all'.")

if __name__ == "__main__":
    main()