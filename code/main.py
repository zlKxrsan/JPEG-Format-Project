from exif_tools import ExifEditor
from file_path import FILE_PATH, RESTORE_FILE_PATH
from hexdump import dehex
from dqt_tools import DqtEditor

temp = ExifEditor(FILE_PATH, RESTORE_FILE_PATH)
temp.set_date_and_restore("2010:10:10 10:10:10") # achtung tags welche
print(temp.get_date())

temp2 = DqtEditor(FILE_PATH, RESTORE_FILE_PATH)
#table = temp.get_table(0)
test_table = ['0F 0F 0F 0F 0F 0F 0F 0F',
              '02 02 02 02 02 02 03 05', 
              '03 03 03 03 03 06 04 04',
              '03 05 07 06 07 07 07 06', 
              '07 07 08 09 0B 09 08 08',
              '0A 08 07 07 0A 0D 0A 0A', 
              '0B 0C 0C 0C 0C 07 09 0E',
              '0F 0D 0C 0E 0B 0C 0C 0C']
temp2.set_and_restore_table(1, test_table)
temp2.set_and_restore_table(0, test_table)
print(temp2.get_table(1))