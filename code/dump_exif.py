from pathlib import Path
import re
from hexdump import dump, dehex

path = Path("jpeg_format/code/dump_exif.py")

file_name = path.parents[2].absolute() / "jpeg_with_exif/canon.jpg"
file_to_restore_dump_into = path[2] / "restored_results/canon_restored.jpg"

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