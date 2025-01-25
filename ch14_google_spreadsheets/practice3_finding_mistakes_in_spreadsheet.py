# Finding Mistakes in a Spreadsheet
# Identifies which row in the sheet has incorrect total.

import ezsheets

ss = ezsheets.Spreadsheet('1jDZEdvSIh4TmZxccyy0ZXrH-ELlrwq8_YYiZrEOB4jg')
sheet = ss[0]

for i in range(2, sheet.rowCount + 1):
    if sheet.getRow(i)[0] == '':
        continue
    if int(sheet.getRow(i)[0]) * int(sheet.getRow(i)[1]) != int(sheet.getRow(i)[2]):
        print(f'The row {i} has incorrect total!')
