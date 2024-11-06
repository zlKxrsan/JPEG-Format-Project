import re
import exifread
from hexdump import dump, dehex
from file_path import FILE_PATH, RESTORE_FILE_PATH

""" This module contains functions to manipulate and read exif-headers """

def read_exif():
    with open(FILE_PATH, "rb") as file:

        tags = exifread.process_file(file, details=False)

        for tag in tags.keys():
            if tag in ("Image Model", "Image Make", "EXIF DateTimeDigitized",
                "EXIF DateTimeOriginal", "Image Orientation"):
                print(tag + " " + str(tags[tag]))

def remove_thumbnail_part():

    with open(FILE_PATH, 'rb') as file:

        try:
            file_content = file.read()
            dumped_file = dump(file_content, size=2, sep=' ')
            thumbnail_part = re.match("FF D8 (.*) FF D8 ", dumped_file).group()
            file_without_exif_part = dehex("FF D8 " + dumped_file[len(thumbnail_part):])

            with open(RESTORE_FILE_PATH, 'wb') as restore_file:
                restore_file.write(file_without_exif_part)
        except:
            print("No exif preview-picture or thumbnailintegration detected!")