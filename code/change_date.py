import re
from hexdump import dump, dehex
from file_path import FILE_PATH, RESTORE_FILE_PATH

with open(FILE_PATH, "rb") as file:
    file_content = file.read()
    dump_file = dump(file_content, size=1, sep='')
    ffe1_marker = re.match("(.*)FFE1", dump_file).group()
    offset_str = dump_file[len(ffe1_marker)+24:len(ffe1_marker)+32]
    offset_str_big_endian = "".join(reversed([offset_str[i:i+2] for i in range(0, len(offset_str), 2)]))
    segment_offset = int(offset_str_big_endian, 16) * 2 # achtung mal zwei für byte size!!!