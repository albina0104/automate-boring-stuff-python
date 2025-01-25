# Regex Search
# Opens all .txt files in a folder and searches for any line
# that matches a user-supplied regular expression.
# The results are printed to the screen.

import re
from pathlib import Path

# Get regex from user
regex_string = input('Input a regular expression:\n')
user_regex = re.compile(regex_string, re.DOTALL)    # Without re.DOTALL, nothing is matching because lines in .txt files end with \n

# Open all *.txt files, check each line
cur_dir = Path('.')
txt_files = cur_dir.glob('*.txt')

for txt_file in txt_files:
    with open(txt_file) as file_content:
        for line in file_content:
            if user_regex.search(line):
                print(f'{txt_file}: {line.strip()}')
