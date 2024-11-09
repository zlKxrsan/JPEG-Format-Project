import exif_tools
from file_path import FILE_PATH, RESTORE_FILE_PATH

temp = exif_tools.ExifEditor(FILE_PATH)
print(temp.tags)
print()
print(temp.ptr_tags)