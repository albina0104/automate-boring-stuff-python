#! /usr/bin/env python3
# multiplication_table_maker.py
# Takes a number N from the command line and creates
# an N×N multiplication table in an Excel spreadsheet.

import sys
import openpyxl
from openpyxl.styles import Font

try:
    number = int(sys.argv[1])
except:
    print('A command line argument must be provided and it must be an integer')
    exit()

wb = openpyxl.Workbook()
sheet = wb.active
bold_font = Font(bold=True)

for row in range(number+1):
    for col in range(number+1):
        cell = sheet.cell(row=row+1, column=col+1)
        if row == 0 and col == 0:
            continue
        elif row == 0:
            cell.value = col
            cell.font = bold_font
        elif col == 0:
            cell.value = row
            cell.font = bold_font
        else:
            cell.value = row * col

wb.save('multiplicationTable.xlsx')
print('Done!')
