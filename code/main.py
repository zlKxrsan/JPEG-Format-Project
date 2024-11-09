from exif_tools import ExifEditor
from file_path import FILE_PATH, RESTORE_FILE_PATH
from hexdump import dehex

temp = ExifEditor(FILE_PATH, RESTORE_FILE_PATH)
temp.set_date_and_restore("2010:10:10 10:10:10") # achtung tags welche
print(temp.get_date())