# Selective Copy
# Walks through a folder tree and searches for files with a certain file extension.
# Copies these files to a new folder.

import os
import shutil
from pathlib import Path

def selective_copy(path, extension, new_path):
    path = os.path.abspath(path)
    new_path = Path(os.path.abspath(new_path))
    new_path.mkdir(parents=True, exist_ok=True)

    for folder_name, subfolders, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(f'.{extension}'):
                source = os.path.join(folder_name, filename)
                destination = os.path.join(new_path, filename)
                print(f'The file {source} will be copied to {destination}')
                shutil.copy(source, destination)
    print('Done!')

selective_copy('./example_folder', 'txt', './new_folder')
