import re
import os
import shutil

def fill_in_gaps(folder, base_name, extension):
    """
    Finds all files with a given prefix, such as spam001.txt, spam002.txt,
    and so on, in a single folder and locates any gaps in the numbering
    (such as if there is a spam001.txt and spam003.txt but no spam002.txt).
    Renames all the later files to close the gap.
    """
    filename_regex = re.compile(f'{base_name}(\\d+)\\.{extension}')
    folder_path = os.path.abspath(folder)
    filenames_list = os.listdir(folder_path)
    filenames_list.sort()

    current_count = 0
    for file_name in filenames_list:
        match_obj = filename_regex.fullmatch(file_name)
        if match_obj:
            digits_str = match_obj.group(1)
            digits_length = len(digits_str)
            digits_int = int(digits_str)
            current_count += 1
            if digits_int - current_count > 0:
                # need to rename the file
                new_file_name = f"{base_name}{str(current_count).rjust(digits_length, '0')}.{extension}"
                try:
                    shutil.move(os.path.join(folder_path, file_name), os.path.join(folder_path, new_file_name))
                except Exception as e:
                    print(f'Error renaming file {file_name}: {e}')


def add_gap(folder, base_name, extension, gap_number):
    """
    Inserts a gap into numbered files so that a new file can be added.
    """
    filename_regex = re.compile(f'{base_name}(\\d+)\\.{extension}')
    folder_path = os.path.abspath(folder)
    filenames_list = os.listdir(folder_path)
    filenames_list.sort(reverse=True)

    for file_name in filenames_list:
        match_obj = filename_regex.fullmatch(file_name)
        if match_obj:
            digits_str = match_obj.group(1)
            digits_length = len(digits_str)
            digits_int = int(digits_str)
            if digits_int >= gap_number:
                # need to rename the file
                new_file_name = f"{base_name}{str(digits_int + 1).rjust(digits_length, '0')}.{extension}"
                try:
                    shutil.move(os.path.join(folder_path, file_name), os.path.join(folder_path, new_file_name))
                except Exception as e:
                    print(f'Error renaming file {file_name}: {e}')


fill_in_gaps('./example_folder', 'example_name', 'txt')
add_gap('./example_folder', 'example_name', 'txt', 27)
