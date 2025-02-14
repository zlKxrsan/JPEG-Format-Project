import sys
import os

sys.path.append(os.path.abspath("code"))

import argparse
from exif_tools import ExifEditor
from dqt_tools import DqtEditor
from monochrom_tools import make_all_types 

def main():

    parser = argparse.ArgumentParser(description="Skript um JPEG-Dateien zu manipulieren.")
    parser.add_argument("-a", "--filename", type=str, help="Dateiname")
    
    args = parser.parse_args()

    input = args.filename

    if input:
        process_file(input)
    
    else:
        jpeg_folder = "jpegs"
        files = os.listdir(jpeg_folder)
        for f in files:
            process_file(f)

def process_file(input):
    exif_obj = ExifEditor(input)
    exif_obj.set_date_and_restore("2010:10:10 10:10:10") #Beispiel Datum

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

if __name__ == "__main__":
    main()