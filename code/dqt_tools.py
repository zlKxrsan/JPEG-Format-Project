from file_path import FILE_PATH, RESTORE_FILE_PATH
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

    def __init__(self, file_path, restore_path):

        self.restore_path = restore_path

        with open(file_path, "rb") as file:

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
            self.file_dump = self.file_dump[:self.start_1+6] + ''.join(table).replace(" ", "") + self.file_dump[self.end_1:] #achtung whitespace bei join?
            self.restore()

        elif num == 1:
            self.table_2 = table
            self.file_dump = self.file_dump[:self.start_2+6] + ''.join(table).replace(" ", "") + self.file_dump[self.end_2:]
            self.restore()
            
    def restore(self):

        with open(self.restore_path, "wb") as file:
            temp_dumper = dehex(self.file_dump)
            file.write(temp_dumper)

temp = DqtEditor(FILE_PATH, RESTORE_FILE_PATH)
#table = temp.get_table(0)
test_table = ['0F 0F 0F 0F 0F 0F 0F 0F',
              '02 02 02 02 02 02 03 05', 
              '03 03 03 03 03 06 04 04',
              '03 05 07 06 07 07 07 06', 
              '07 07 08 09 0B 09 08 08',
              '0A 08 07 07 0A 0D 0A 0A', 
              '0B 0C 0C 0C 0C 07 09 0E',
              '0F 0D 0C 0E 0B 0C 0C 0C']
temp.set_and_restore_table(1, test_table)

# set and restore is wrong