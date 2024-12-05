from file_path import get_path, get_restore_path
from hexdump import dump, dehex
import re

"""This modul isn't meant to handle dqt 02 and 03 and 16-bit presizion tabelles"""
class DqtEditor():

    file_dump = None
    seg_1 = None
    seg_2 = None
    start_1 = None
    start_2 = None
    end_1 = None
    end_2 = None
    table_1 = None
    table_2 = None
    restore_path = None

    def __init__(self, input):

        self.restore_path = get_restore_path(input, "dqt")

        with open(get_path(input), "rb") as file:

            file_content = file.read()
            self.file_dump = dump(file_content, size=1, sep='')

            self.start_1, self.end_1, self.seg_1 = self.get_dqt(0)
            self.start_2, self.end_2, self.seg_2 = self.get_dqt(self.end_1)

            self.table_1 = self.__get_table(self.start_1)
            self.table_2 = self.__get_table(self.start_2)
    
    def get_dqt(self, offset):

        span = re.search("FFDB.*?FF((?!00).)", self.file_dump[offset:])
        start = offset + span.start()+4
        end = offset + span.end()-3
        return start, end, self.file_dump[start:end]
    
    def __get_table(self, start):

        table = []
        for i in range(0,8):
            temp = self.file_dump[start+6+i*16:start+6+(i+1)*16]
            table.append(temp)
            
        return table

    def get_table(self, num):
        table = []
        if num == 0:
            for col in self.table_1:
                table.append(' '.join(col[i:i+2] for i in range(0, len(col), 2)))
            return table
        elif num == 1:
            for col in self.table_2:
                table.append(' '.join(col[i:i+2] for i in range(0, len(col), 2)))
            return table
        else:
            Exception("no such table found")
    
    def set_and_restore_table(self, num, table):

        if num != 0 and num != 1:
            Exception("no such table found")
        if len(table) != 8:
            Exception("table has wrong row size")
        for col in range(0,8):
            table[col] = table[col].replace(" ", "")
            if len(table[col]) != 16:
                Exception("wrong column size")
        
        if num == 0:
            self.table_1 = table
            self.file_dump = self.file_dump[:self.start_1+6] + ''.join(table) + self.file_dump[self.end_1:]
            self.restore()

        elif num == 1:
            self.table_2 = table
            self.file_dump = self.file_dump[:self.start_2+6] + ''.join(table) + self.file_dump[self.end_2:]
            self.restore()
            
    def restore(self):

        with open(self.restore_path, "wb") as file:
            temp_dumper = dehex(self.file_dump)
            file.write(temp_dumper)