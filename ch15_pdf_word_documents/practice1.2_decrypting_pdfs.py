# Decrypting PDFs
# Finds all encrypted PDFs in a folder (and its subfolders) and creates
# a decrypted copy of the PDF using a provided password. If the password is
# incorrect, the program prints a message to the user and continues to the next PDF.

import os
from pathlib import Path
import pypdf
from pypdf.errors import FileNotDecryptedError


def decrypt_pdfs(directory, password):
    # Go through every PDF in a folder and its subfolders
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.pdf'):
                path = os.path.join(dirpath, filename)
                pdf_reader = pypdf.PdfReader(path)

                # Try to decrypt the file
                try:
                    pdf_reader.decrypt(password)  # this does not raise the error
                    pdf_writer = pypdf.PdfWriter(clone_from=pdf_reader)  # but this does, if the password is incorrect
                except FileNotDecryptedError as e:
                    print('The attempt to decrypt the encrypted file %s was unsuccessful' % path)
                    continue

                # If all good, create a decrypted copy of the PDF
                basename = Path(path).stem
                new_name = f'{basename}_decrypted.pdf'
                new_path = os.path.join(dirpath, new_name)
                with open(new_path, 'wb') as result_pdf:
                    pdf_writer.write(result_pdf)


if __name__ == '__main__':
    print('Please enter the password to decrypt PDFs:')
    password = input()
    decrypt_pdfs('./practice1_pdfs', password)
