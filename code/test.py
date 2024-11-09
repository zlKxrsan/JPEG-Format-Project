import re
from file_path import FILE_PATH
from hexdump import dump
from enum import Flag

class Endian(Flag):
    BIG = True
    SMALL = False

#pass auf indexierung von end auf !!!
# und auf die längen und offset angaben weil du mit halben bytes arbeitest

def to_big_endian(endian_type, hex_part):
    if endian_type == Endian.BIG:
        return hex_part
    else:
        return "".join(reversed([hex_part[i:i+2] for i in range(0, len(hex_part), 2)]))

def get_tags(endian_type, num_of_tags, tags_segment, offset):

    tags = {}
    for i in range(num_of_tags):
        tag = tags_segment[24*i:(1+i)*24]
        tag_id = to_big_endian(endian_type, tag[:4])
        tag_type = None
        match int(to_big_endian(endian_type, tag[4:8]), 16):
            case 1:             #Byte
                tag_type = 2
            case 2:             #ASCII
                tag_type = 2
            case 3:             #Short
                tag_type = 4
            case 4:             #Int
                tag_type = 8    
            case 5:             #Double
                tag_type = 16
            case _:
                Exception("Not an exif type!")
        tag_size = int(to_big_endian(endian_type, tag[8:16]), 16) # doesnt work for idf without offset maybe fixing to x2???
        tag_val_or_offset = int(to_big_endian(endian_type, tag[16:]), 16)*2 + offset # offset from lengt of exif-segment to endian decision umbenenen?
        tags[tag_id] = [tag_type, tag_size, tag_val_or_offset]
    return tags

def get_tags_values(endian_type, exif_segment, tags):

    tags_values = {}
    for tag in tags:    #except pointer tag fix it pls
        tag_type = tags[tag][0]
        tag_size = tags[tag][1]
        tag_offset = tags[tag][2]
        tags_values[tag] = exif_segment[tag_offset:tag_offset+tag_size*tag_type] # Achtung wegen ifdpointer!!!!!!! und little endian
    
    return tags_values



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
    offset = int(to_big_endian(endian_type, exif_segment[offset_start:offset_end]), 16) * 2 # achtung multiplizeren maybe

    num_of_tags_start = offset_end
    num_of_tags_end = num_of_tags_start + 4
    num_of_tags = int(to_big_endian(endian_type, exif_segment[num_of_tags_start:num_of_tags_end]), 16)

    tags_segment = exif_segment[num_of_tags_end:num_of_tags_end + num_of_tags * 24] # 24 steht für 12 bytes

    tags = get_tags(endian_type, num_of_tags, tags_segment, offset)

    tags_values = get_tags_values(endian_type, exif_segment, tags)

    offset_pointer_tags = None
    pointer_tags = {}
    pointer_tags_values = {}
    if "8769" in tags:
        num_of_idf_pointer_tags = int(tags_values["8769"][:4], 16) if endian_type == Endian.BIG else int(to_big_endian(endian_type, tags_values["8769"][:4]), 16)
        pointer_tags_start = tags["8769"][2] + 4
        pointer_tags_end = pointer_tags_start + num_of_idf_pointer_tags * 24
        pointer_tags = get_tags(endian_type, num_of_idf_pointer_tags, exif_segment[pointer_tags_start:pointer_tags_end], 0)
        pointer_tags_values = get_tags_values(endian_type, exif_segment, pointer_tags) # error
        print(pointer_tags_values)
        
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