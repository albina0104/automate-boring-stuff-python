#! /usr/bin/env python3
# Identifying Photo Folders on the Hard Drive
# Goes through every folder on your hard drive and finds potential photo folders.
# A "photo folder" is any folder where more than half of the files are photos.
# A photo file must have the file extension .png or .jpg,
# and a photo file’s width and height must both be larger than 500 pixels.

import os
import logging
import traceback
from PIL import Image

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='identifying_photo_folders.log')
logger = logging.getLogger(__name__)

SEARCH_DIRECTORY = os.path.expanduser('~')

try:
    for foldername, subfolders, filenames in os.walk(SEARCH_DIRECTORY):
        num_photo_files = 0
        num_non_photo_files = 0

        for filename in filenames:
            # Check if file extension isn't .png or .jpg.
            if not (filename.lower().endswith('.png') or filename.lower().endswith('.jpg')):
                num_non_photo_files += 1
                continue    # skip to next filename

            # Open image file using Pillow.
            full_path = os.path.join(foldername, filename)
            try:
                image = Image.open(full_path)

                # Check if width & height are larger than 500.
                width, height = image.size
                if (width > 500) and (height > 500):
                    # Image is large enough to be considered a photo.
                    num_photo_files += 1
                else:
                    # Image is too small to be a photo.
                    num_non_photo_files += 1
            except Exception as e:
                logger.error('Error while processing image %s - %s. %s' % (full_path, e, traceback.format_exc()))

        # If more than half of files were photos,
        # print the absolute path of the folder.
        if num_photo_files > num_non_photo_files:
            print(foldername)

except Exception as e:
    logger.error('An error occurred - %s. %s' % (e, traceback.format_exc()))
