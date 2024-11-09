import exif_tools
from file_path import FILE_PATH, RESTORE_FILE_PATH
from hexdump import dehex

temp = exif_tools.ExifEditor(FILE_PATH, RESTORE_FILE_PATH)
temp.set_date_and_restore("2010:10:10 10:10:10", temp.ptr_tags) # achtung tags welche
