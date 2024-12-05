from exif_tools import ExifEditor
from dqt_tools import DqtEditor
from monochrom_tools import make_all_types 

input = "bird1"

exif_obj = ExifEditor(input)
exif_obj.set_date_and_restore("2010:10:10 10:10:10") # achtung tags welche

dqt_obj = DqtEditor(input)
dqt_table = ['0F 0F 0F 0F 0F 0F 0F 0F',
              '02 02 02 02 02 02 03 05', 
              '03 03 03 03 03 06 04 04',
              '03 05 07 06 07 07 07 06', 
              '07 07 08 09 0B 09 08 08',
              '0A 08 07 07 0A 0D 0A 0A', 
              '0B 0C 0C 0C 0C 07 09 0E',
              '0F 0D 0C 0E 0B 0C 0C 0C']
dqt_obj.set_and_restore_table(1, dqt_table)
dqt_obj.set_and_restore_table(0, dqt_table)

make_all_types(input)