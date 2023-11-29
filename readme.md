# **<u>Campbell Brown</u>** #

## Overview ##
The purpose of this code is to act as a way to catalog all the items being created in a sustainable way.

## Functionality: ##
1. Employee signs in with badge.
2. Employee presses button.
3. Qr code is generated and data is added into spreadsheet, data added is the name of the part, date,
   part number for that day, and employee number.
   (Part number is a sequential number that will increase by one for each part generated each day. At the start of the new day
   the part number will reset to 1)
4. QR code is printed out onto sticker.
5. Sticker is stuck onto part and is cataloged.

## Things to Note ##
1. Excel sheet will be updated for each part.
2. The log.txt file will also be constantly updated.
3. The QR Codes generated will be replaced each time a button is pressed. However, until a new QR code is generated it is saved into the system.

## Use of Functions ##

**<u>QR_CODE.py</u>**
1. Use ```./qr_code.py generate "PART NAME" ``` to generate a standalone qr code to be printed. "PART NAME" can be anything.
2. Use ```./qr_code.py excel "PART NAME" ``` to add the data that would be in the qr code to just an excel sheet. "PART NAME" can be anything.
3. Use ```./qr_code.py all "PART NAME" ``` to generate the qr code and add the data to an excel sheet.

-----------------------------------------------------------------------------------------------------------------------

**<u>QR_DECODE.py</u>**
1. Use ```./qr_decode.py decode badge``` to parse for a badge number this is then saved to be used later in qr_generation.
2. Use ```./qr_decode.py decode part``` to decode a qr code and add the data to a part_num file, this file is parsed when using the excel command.
3. Use ```./qr_decode.py excel "NAME_OF_ASSEMBLY"``` to generate/add data to an assembly excel file by parsing the data in the part_num.txt file.
