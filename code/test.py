import re
from file_path import FILE_PATH
from hexdump import dump
from enum import Flag

"""This Module contains all functions handling the exif-segment of or jpeg-files"""
"""We work with 4 bits instead of 8 due to the handling of the dataflow in hex with hexdump, so every calculation takes twice the coefficient"""

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

def get_tag_type_size(tag_type):
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
        
def get_tag_value(exif_segment, tags, tag, offset): # Ausnahme ist der IDFPointer-Tag, weil im an der offset stelle nur zwei Bytes für die anzahl an tags stehen.

    tag_value = None
    (tag_type, tag_size, tag_offset) = tags[tag]
    temp_offset = int(tag_offset, 16)*2 + offset
    tag_value = exif_segment[temp_offset:
                        temp_offset +int(tag_size, 16)*get_tag_type_size(int(tag_type, 16))] # Achtung wegen ifdpointer!!!!!!! und little endian
    
    return tag_value



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
    print(pointer_tags)

    print(get_tag_value(exif_segment, pointer_tags, "9003", offset))


    #offset_pointer_tags = None
    #pointer_tags = {}
    #pointer_tags_values = {}
#    if "8769" in tags:
#        num_of_idf_pointer_tags = int(tags_values["8769"][:4], 16) if endian_type == Endian.BIG else int(to_big_endian(endian_type, tags_values["8769"][:4]), 16)
#        pointer_tags_start = tags["8769"][2] + 4
#        pointer_tags_end = pointer_tags_start + num_of_idf_pointer_tags * 24
#        pointer_tags = get_tags(endian_type, num_of_idf_pointer_tags, exif_segment[pointer_tags_start:pointer_tags_end], 0)
#        pointer_tags_values = get_tags_values(endian_type, exif_segment, pointer_tags) # error
#        print(pointer_tags_values)
        
# Machen wir ein Tag lister damit
#    for i in range(num_of_tags):
#        tag = tag_segment[24*i:(1+i)*24]
#        tag_id = to_big_endian(endian_type, tag[:4])
#        tag_type = to_big_endian(endian_type, tag[4:8])
#        tag_size = to_big_endian(endian_type, tag[8:16])
#        tag_val_or_offset = to_big_endian(endian_type, tag[16:])
#        tags[tag_id] = [tag_type, tag_size, tag_val_or_offset]
#
#    print(tags)
#

#fehler mit großen datentypen beim offset berechnen

#def get_tags(endian_type, num_of_tags, tags_segment, offset):
#
#    tags = {}
#    for i in range(num_of_tags):
#        tag = tags_segment[24*i:(1+i)*24]
#        tag_id = to_big_endian(endian_type, tag[:4])
#        tag_type = None
#        match int(to_big_endian(endian_type, tag[4:8]), 16):
#            case 1:             #Byte
#                tag_type = 2
#            case 2:             #ASCII
#                tag_type = 2
#            case 3:             #Short
#                tag_type = 4
#            case 4:             #Int
#                tag_type = 8    
#            case 5:             #Double
#                tag_type = 16
#            case _:
#                Exception("Not an exif type!")
#        tag_size = int(to_big_endian(endian_type, tag[8:16]), 16) # Funktioniert nicht für Tag-Content, welcher ohne offset gespeichert ist.
#        tag_offset = int(to_big_endian(endian_type, tag[16:]), 16)*2 + offset # offset vom tag-Content + offset vom exif-header.
#        tags[tag_id] = [tag_type, tag_size, tag_offset]
#    return tags
#