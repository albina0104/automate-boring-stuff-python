# Brute-Force PDF Password Breaker
# Decrypts the PDF by trying every word from the provided dictionary
# until it finds one that works.

import os
import pypdf
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_list_from_txt_file(filename: str) -> list:
    if not os.path.exists(filename):
        logger.error(f'The file {filename} does not exist.')
        return []

    try:
        with open(filename) as txt_file:
            txt_file_contents = txt_file.read()
            return txt_file_contents.strip().split('\n')
    except Exception as e:
        logger.error(f'Could not open the file: {filename}, error: {e}')
        return []


def find_pdf_password(pdf_filename: str, password_list: list) -> str:
    pdf_reader = pypdf.PdfReader(pdf_filename)
    for password in password_list:
        result = pdf_reader.decrypt(password)
        if result != 0:
            return password
        else:
            password = password.lower()
            result = pdf_reader.decrypt(password)
            if result != 0:
                return password
    return ''


if __name__ == '__main__':
    logger.info('The program has started')
    dictionary = get_list_from_txt_file('dictionary.txt')
    if dictionary:
        password = find_pdf_password('encrypted.pdf', dictionary)
        if password:
            print(f'The password for the PDF file is "{password}"')
        else:
            print('The password has not been found!')
    logger.info('End of the program')
