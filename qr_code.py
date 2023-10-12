import qrcode
from PIL import Image
import time
import xlsxwriter
import os

def generate_qr_code(name_of_part, date, part_number, badge_number):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"{name_of_part},{date},{part_number},{badge_number}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr_code.png")

def add_data_to_excel(name_of_part, time, date, part_number, badge_number):
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
generate_qr_code("Part Name", time.strftime("%H:%M:%S"), time.strftime("%m.%d.%Y"), 1, 12345)
add_data_to_excel("Part Name", time.strftime("%H:%M:%S"), time.strftime("%m.%d.%Y"), 1, 12345)
print_qr_code()