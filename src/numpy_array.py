import numpy as np

class NPArray:
    def __init__(self, size, item_type):
        #Size of array
        self.size = size
        #Array
        self.arr = np.empty(size, dtype=item_type)
        #Position of the last append
        self.cur_pos = 0
    #change current position
    def setCurPos(self, pos):
        self.cur_pos = pos
    #append array
    def append(self, item):
        self.arr[self.cur_pos] = item
        self.cur_pos+=1
    #array
    def getArr(self):
        return self.arr
    #size of array
    def getSize(self):
        return self.size
    def getRealSize(self):
        return self.cur_pos