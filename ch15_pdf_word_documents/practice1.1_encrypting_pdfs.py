# Encrypting PDFs
# Goes through every PDF in a folder (and its subfolders) and encrypts the PDFs
# using a password provided on the command line. Saves each encrypted PDF with an
# _encrypted.pdf suffix added to the original filename. Before deleting the original
# file, attempts to read and decrypt the file to ensure that it was encrypted correctly.

import os
from pathlib import Path
import pypdf
from pypdf.errors import FileNotDecryptedError


def encrypt_pdfs(directory, password):
    # Go through every PDF in a folder and its subfolders
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.pdf'):
                path = os.path.join(dirpath, filename)
                pdf_reader = pypdf.PdfReader(path)
                pdf_writer = pypdf.PdfWriter(clone_from=pdf_reader)
                # Encrypt the PDF
                pdf_writer.encrypt(password, algorithm='AES-256-R5')
                basename = Path(path).stem
                new_name = f'{basename}_encrypted.pdf'
                new_path = os.path.join(dirpath, new_name)
                with open(new_path, 'wb') as result_pdf:
                    pdf_writer.write(result_pdf)

                # Try to read the encrypted file
                pdf_file_obj = open(new_path, 'rb')
                pdf_reader = pypdf.PdfReader(pdf_file_obj)
                try:
                    pdf_reader.decrypt(password)  # this does not raise the error
                    page = pdf_reader.pages[0]  # but this does, if the password is incorrect
                except FileNotDecryptedError as e:
                    print('The attempt to decrypt the encrypted file %s was unsuccessful, so original file was not deleted' % new_path)
                    continue

                # If all good, delete the file
                os.remove(path)


if __name__ == '__main__':
    print('Please enter the password for PDF encryption:')
    password = input()
    encrypt_pdfs('./practice1_pdfs', password)
