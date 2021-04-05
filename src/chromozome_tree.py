import random
import math
import numpy as np

class ChromozomeTree:
    def __init__(self, length, random_tree):
        #length of chromozome
        self.length = length
        #chromozome
        self.chromozome = np.empty(length, dtype=int)
        # random number from range -1 to 1, -3 represent 'x'
        self.parameters = np.full(shape=(length+1), fill_value=-3,dtype=float)#np.empty((length+1), dtype=float)

        if random_tree == True:
            self.generateChromozome()
    
    def generateChromozome(self):
        for i in range(0, self.length):
            #new gene
            self.chromozome[i] = random.randint(1, 4)
            self.parameters[i] = -3
        self.parameters[self.length] = -3

    def getValue(self, x):
        output = self.countValue(x)
        return output

    #iterate to get output for functon represented by tree function
    def countValue(self, x): #num, i, x):
        result = x        
        for i in range(0, self.length):
            if self.chromozome[i] == 1:#+
                result+=x
            elif self.chromozome[i] == 2:#-
                result-=x
            elif self.chromozome[i] == 3:#*
                result*=x
            elif self.chromozome[i] == 4:#/
                if x != 0:
                    result/=x

        return result

        """
        old code
        result = self.parameters[i]

        #change value-----------------------------
        if self.parameters[i] == -3:
                result = x
        else:
            result = self.parameters[i]
        
        if i >= self.length:
            return result
        
        #main logic of iteration------------------
        if self.chromozome[i] == 1: #+
            result=self.countValue(result, i+1, x)
            result+=num
        elif self.chromozome[i] == 2: #-
            result=self.countValue(result, i+1, x)
            result=num-result
        elif self.chromozome[i] == 3: #*
            result*=num
            result=self.countValue(result, i+1, x)
        else:                       #/
            if result != 0:
                result=num/result
                result=self.countValue(result, i+1, x)

        return result
        """

    def getOp(self, index):
        if len(self.chromozome) <= index:
            return None
        translate_op = {
            1: "+",
            2: "-",
            3: "*",
            4: "/"
        }
        return translate_op[self.chromozome[index]]

    def getPar(self, index):
        if len(self.parameters) <= index:
            return None

        if (self.parameters[index] == -3):
            return "x"
        return self.parameters[index]