import os

def get_large_files_list(folder):
    """
    Walk through a folder tree and print the absolute path of files
    larger than 100MB.
    """
    folder = os.path.abspath(folder)
    for folder_name, subfolders, filenames in os.walk(folder):
        for filename in filenames:
            full_file_path = os.path.join(folder_name, filename)
            try:
                file_size_bytes = os.path.getsize(full_file_path)
                file_size_mb = round(file_size_bytes / 1_048_576)
                if file_size_mb > 100:
                    print(f'{file_size_mb}MB - {full_file_path}')
            except Exception as e:
                print(f'Error accessing {full_file_path}: {e}')


get_large_files_list('./example_folder')
