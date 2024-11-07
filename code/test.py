import re
from file_path import FILE_PATH
from hexdump import dump
from enum import Flag

class Endian(Flag):
    BIG = True
    SMALL = False

#pass auf indexierung von end auf !!!
# und auf die längen und offset angaben weil du mit halben bytes arbeitest

def get_value(endian_type, hex_part):
    if endian_type == Endian.BIG:
        return int(hex_part, 16)
    else:
        return int("".join(reversed([hex_part[i:i+2] for i in range(0, len(hex_part), 2)])), 16)

with open(FILE_PATH, "rb") as file:

    file_content = file.read()
    file_dump = dump(file_content, size=1, sep='')

    exif_segment_span = re.search("FFE1.*?FF[^(00)]{2}", file_dump)
    exif_segment_start = exif_segment_span.start()+4
    exif_segment_end = exif_segment_span.end()-3
    exif_segment = file_dump[exif_segment_start:exif_segment_end]
    exif_segment_length = int(exif_segment[:4],16) # achtung bytest und halbe bytes

    endian_part = re.search("(4949|4D4D)", exif_segment)
    endian_type = Endian.BIG if exif_segment[endian_part.start():endian_part.end()] == "4D4D" else Endian.SMALL
    
    offset_start = endian_part.end()+4
    offset_end = offset_start + 8
    offset = get_value(endian_type, exif_segment[offset_start:offset_end]) # achtung multiplizeren maybe

    num_of_tags_start = offset_end
    num_of_tags_end = num_of_tags_start + 4
    num_of_tags = get_value(endian_type, exif_segment[num_of_tags_start:num_of_tags_end])

    tag_segment = exif_segment[num_of_tags_end:num_of_tags_end + num_of_tags * 24] # 24 steht für 12 bytes

    tags = []

    for i in range(num_of_tags):
        tags.append(tag_segment[24*i:(1+i)*24])

    print(tags)
