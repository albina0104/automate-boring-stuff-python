# Mad Libs
# Reads in text files and lets the user add their own text
# anywhere the word ADJECTIVE, NOUN, ADVERB, or VERB appears in the text file.

import re

# Open file and get a string
text_file = open('text_for_mad_libs.txt')
text_file_content = text_file.read()
text_file.close()

# Find and replace strings
str_regex = re.compile(r'(ADJECTIVE|NOUN|ADVERB|VERB)')
found_words = str_regex.findall(text_file_content)
for word in found_words:
    prompt = f"Enter a{'n' if word.startswith('A') else ''} " + word.lower() + ':\n'
    new_word = input(prompt)
    text_file_content = text_file_content.replace(word, new_word, 1)

# Print and save as a new file
print(text_file_content)
new_text_file = open('mad_libs_replaced_text.txt', 'w')
new_text_file.write(text_file_content)
new_text_file.close()
