from file_path import FILE_PATH, RESTORE_FILE_PATH
from hexdump import dump, dehex
import re

# be aware of end idx -1 !!!
with open(FILE_PATH, "rb") as file:
    file_content = file.read()
    file_dump = dump(file_content, size=1, sep='')
    dqt_seg_span_1 = re.search("FFDB.*?FF((?!00).)", file_dump)
    start_1 = dqt_seg_span_1.start()+4
    end_1 = dqt_seg_span_1.end()-3
    print(file_dump[start_1:end_1])

    dqt_seg_span_2 = re.search("FFDB.*?FF((?!00).)", file_dump[end_1:])
    start_2 = end_1 + dqt_seg_span_2.start()+4
    end_2 = end_1 + dqt_seg_span_2.end()-3

    print(file_dump[start_2:end_2])
    #print(dqt_seg_span_2)