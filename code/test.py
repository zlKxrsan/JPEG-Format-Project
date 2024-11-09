import re
from file_path import FILE_PATH
from hexdump import dump
from enum import Flag

"""This Module contains all functions handling the exif-segment of or jpeg-files"""
"""We work with 4 bits instead of 8 due to the handling of the dataflow in hex with hexdump, so every offset is 2x"""

class Endian(Flag):
    BIG = True
    SMALL = False

def to_big_endian(hex_part):
    if endian_type == Endian.BIG:
        return hex_part
    else:
        return "".join(reversed([hex_part[i:i+2] for i in range(0, len(hex_part), 2)]))

def get_tags(num_of_tags, tags_segment):

    tags = {}
    for i in range(num_of_tags):
        tag = tags_segment[24*i:(1+i)*24]
        tag_id = to_big_endian(tag[:4])
        tag_type = to_big_endian(tag[4:8])
        tag_size = to_big_endian(tag[8:16]) # Funktioniert nicht für Tag-Content, welcher ohne offset gespeichert ist.
        tag_offset = to_big_endian(tag[16:]) # offset vom tag-Content + offset vom exif-header.
        tags[tag_id] = (tag_type, tag_size, tag_offset)
    return tags

def get_tag_type_size(tag_type): #this function cant handle exif_type over 5
    res = None
    match tag_type:
        case 1:             #Byte
            res = 2
        case 2:             #ASCII
            res = 2
        case 3:             #Short
            res = 4
        case 4:             #Int
            res = 8    
        case 5:             #Double
            res = 16
        case _:
                Exception("Not an exif type!")
    return res
        
def get_tag_value(exif_segment, tag): # Ausnahme ist der IDFPointer-Tag, weil im an der offset stelle nur zwei Bytes für die anzahl an tags stehen.

    tag_value = None
    (tag_type, tag_size, tag_offset) = tag
    temp_offset = int(tag_offset, 16)*2 + offset
    tag_value = exif_segment[temp_offset:
                        temp_offset +int(tag_size, 16)*get_tag_type_size(int(tag_type, 16))] # Achtung wegen ifdpointer!!!!!!! und little endian
    
    return tag_value


def get_date(exif_segment, tags): # beispiel zur untermalung des verständnisses
    bin_date = get_tag_value(exif_segment, tags["9003"])
    ascii_date = [int(bin_date[i:i+2], 16) for i in range(0, len(bin_date), 2)]
    return ''.join(chr(i) for i in ascii_date)

#def set_date(file_dump, new_date, start, end, tags):
#    new_date_converted = ''.join(str(hex(ord(c))[2:]).upper() for c in new_date) + '00'
#    (tag_type, tag_size, tag_offset) = tags['9003']
#    temp_offset = int(tag_offset, 16)*2 + offset
#    return

    

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
    offset = int(to_big_endian(exif_segment[offset_start:offset_end]), 16) * 2 # achtung multiplizeren maybe

    num_of_tags_start = offset_end
    num_of_tags_end = num_of_tags_start + 4
    num_of_tags = int(to_big_endian(exif_segment[num_of_tags_start:num_of_tags_end]), 16)

    tags_segment = exif_segment[num_of_tags_end:num_of_tags_end + num_of_tags * 24] # 24 steht für 12 bytes

    tags = get_tags(num_of_tags, tags_segment)

    pointer_tags_offset = int(tags["8769"][2], 16) * 2 + offset # exception when no pointer einbauen
    num_of_pointer_tags = int(to_big_endian(exif_segment[pointer_tags_offset:pointer_tags_offset+4]), 16)
    pointer_tags_segment = exif_segment[pointer_tags_offset+4:pointer_tags_offset*num_of_pointer_tags*24+4]
    pointer_tags = get_tags(num_of_pointer_tags, pointer_tags_segment)

#    set_date(file_dump, "9999:99:99 99:99:99", idx1, idx2, tags)

    #print(get_tag_value(exif_segment, pointer_tags["9003"]))
    #print(get_date(exif_segment, pointer_tags))
