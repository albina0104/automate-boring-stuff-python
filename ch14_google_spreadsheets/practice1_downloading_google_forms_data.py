# Downloading Google Forms Data
# Collects a list of email addresses from a Google spreadsheet
# that the users submitted via Google Forms

import ezsheets

# Load the spreadsheet
ss = ezsheets.Spreadsheet('YOUR_GOOGLE_SPREADSHEET_ID_HERE')
sheet = ss[0]

# Get all emails from column 3, skipping the header
email_column = sheet.getColumn(3)[1:]  # [1:] slices the list to skip the header
email_list = [email for email in email_column if email]  # List comprehension to filter out empty strings

print(email_list)
