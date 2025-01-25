# Text Files to Spreadsheet
# Reads in the contents of several text files and inserts those contents into a spreadsheet,
# with one line of text per row. The lines of the first text file will be in the cells of
# column A, the lines of the second text file will be in the cells of column B, and so on.

import os
from pathlib import Path
import openpyxl
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

os.chdir('text_files')

wb = openpyxl.Workbook()
sheet = wb.active

col_num = 0
for filename in Path.cwd().glob('*.txt'):
    col_num += 1
    with open(filename, 'r') as file:
        logging.debug(f'Writing file {filename} to column {col_num}')
        row_num = 0
        for line in file.readlines():
            row_num += 1
            sheet.cell(row=row_num, column=col_num, value=line.rstrip('\n'))

spreadsheet_filename = 'textFilesToSpreadsheet.xlsx'
wb.save(spreadsheet_filename)
logging.info(f'Results saved to file {spreadsheet_filename}')
