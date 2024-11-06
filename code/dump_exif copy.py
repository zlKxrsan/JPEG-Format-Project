from hexdump import dump, dehex
import re

file_name = "Acer/AcerLiquid.jpg"
file_to_restore_dump_into = "AcerC01_restored.jpg"

with open(file_name, 'rb') as file:
    file_content = file.read()
    dumped_file = dump(file_content, size=2, sep=' ')
    thumbnail_part = re.match("FF D8 (.*) FF D8 ", dumped_file).group()
    file_without_exif_part = dehex("FF D8 " + dumped_file[len(thumbnail_part):])

    with open(file_to_restore_dump_into, 'wb') as restore_file:
        restore_file.write(file_without_exif_part)

# TODO
# regex exception if there is no thumbnail implement
# style guide
# change thumbnail