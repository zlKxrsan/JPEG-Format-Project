import re
from file_path import FILE_PATH, RESTORE_FILE_PATH
from hexdump import dump, dehex
from enum import Flag

"""This Module contains all functions handling the exif-segment of or jpeg-files"""
"""We work with 4 bits instead of 8 due to the handling of the dataflow in hex with hexdump, so every offset is 2x"""

def get_seg(str, start, size):
    end = start + size
    return str[start:end]

class Endian(Flag):
    BIG = True
    SMALL = False


def get_date(exif_segment, tags): # beispiel zur untermalung des verständnisses
    bin_date = get_tag_value(exif_segment, tags["9003"])
    ascii_date = [int(bin_date[i:i+2], 16) for i in range(0, len(bin_date), 2)]
    return ''.join(chr(i) for i in ascii_date)

def set_date(file_dump, new_date, start, tags):
    new_date_converted = ''.join(str(hex(ord(c))[2:]).upper() for c in new_date) + '00'
    (tag_type, tag_size, tag_offset) = tags['9003']
    temp_offset = int(tag_offset, 16)*2 + offset
    return file_dump[:start+temp_offset] + new_date_converted + file_dump[start+temp_offset+int(tag_size, 16)*get_tag_type_size(int(tag_type, 16)):]

class ExifEditor():

    start = 0 
    end = 0
    length = 0
    exif_seg = ""
    offset = 0
    num_of_tags = 0
    tags_seg = ""
    tags = {}
    endian = False

    # Diese Variablen sind für alle IFD-Tags, welche von einem IFDPointer addressiert werden.

    prt_offset = 0
    num_of_ptr_tags = 0
    ptr_tags_seg = ""
    ptr_tags = {}

    def __init__(self, file_name):

        with open(file_name, "rb") as file:

            file_content = file.read()
            file_dump = dump(file_content, size=1, sep='')

            exif_segment_span = re.search("FFE1.*?FF[^(00)]{2}", file_dump)
            self.start = exif_segment_span.start()+4
            self.end = exif_segment_span.end()-3
            self.exif_seg = file_dump[self.start:self.end]
            self.length = int(self.exif_seg[:4],16)

            endian_part = re.search("(4949|4D4D)", self.exif_seg)
            self.endian = Endian.BIG if self.exif_seg[endian_part.start():endian_part.end()] == "4D4D" else Endian.SMALL
            
            #offest wird um *2 erweitert, weil wir durch, dass hex-Format mit halben Bytes arbeiten.
            self.offset = int(self.to_big_endian(get_seg(self.exif_seg, endian_part.end()+4, 8)), 16) * 2

            self.num_of_tags = int(self.to_big_endian(get_seg(self.exif_seg, endian_part.end()+12, 4)), 16)
            self.tags_seg = get_seg(self.exif_seg, endian_part.end()+16, self.num_of_tags*24)
            self.tags = self.get_tags(self.num_of_tags, self.tags_seg)

            self.ptr_offset = int(self.tags["8769"][2], 16) * 2 + self.offset # exception when no pointer einbauen
            self.num_of_ptr_tags = int(self.to_big_endian(get_seg(self.exif_seg, self.ptr_offset, 4)), 16)
            self.ptr_tags_seg = get_seg(self.exif_seg, self.ptr_offset+4, self.num_of_ptr_tags*24+4) #?????=============================================!!!!!!
            self.ptr_tags = self.get_tags(self.num_of_ptr_tags, self.ptr_tags_seg)

            #to_restore = set_date(file_dump, "2010:10:10 10:10:10", start, ptr_tags) # achtung tags welche

            #with open(RESTORE_FILE_PATH, "wb") as file:
            #    file_dumper = dehex(to_restore)
            #    file.write(file_dumper)

    def to_big_endian(self, hex_part):
        if self.endian == Endian.BIG:
            return hex_part
        else:
            return "".join(reversed([hex_part[i:i+2] for i in range(0, len(hex_part), 2)]))

    def get_tags(self, num, seg):

        tags = {}
        for i in range(num):
            tag = seg[24*i:(1+i)*24]
            tag_id = self.to_big_endian(tag[:4])
            tag_type = self.to_big_endian(tag[4:8])
            tag_size = self.to_big_endian(tag[8:16]) # Funktioniert nicht für Tag-Content, welcher ohne offset gespeichert ist.
            tag_offset = self.to_big_endian(tag[16:]) # offset vom tag-Content + offset vom exif-header.
            tags[tag_id] = (tag_type, tag_size, tag_offset)
        return tags
    
    def get_tag_type_size(self, tag_type):

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
                Exception("Not an handled type!")
        return res

    def get_tag_value(self, tag):
        tag_value = None
        (tag_type, tag_size, tag_offset) = tag
        temp_offset = int(tag_offset, 16)*2 + self.offset
        tag_value = self.exif_seg[temp_offset:
                            temp_offset +int(tag_size, 16)*self.get_tag_type_size(int(tag_type, 16))] # Achtung wegen ifdpointer!!!!!!! und little endian
        
        return tag_value

    #Beispiel Funktionen für die Manipulation vom Datum, mit mehr Zeit könnte man auch eine...