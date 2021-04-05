import numpy as np
import random
from math import sin, pi, sqrt
from numpy_array import NPArray
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

from chromozome_tree import ChromozomeTree



class Individual:
    def __init__(self, rand_chrom, data_len=3):
        #fintess
        self.fitness = None
        #chromozome
        self.chromozome = np.empty(data_len, dtype=float)
        #length of chromozome
        self.chromozome_length = data_len

        #range to aproximate
        self.start_point = -10*pi
        self.end_point   =  10*pi

        #generate new random chromozome
        if rand_chrom == True:
            self.randomChromo()
        
    
    def randomChromo(self):
        for i in range(0, int(self.chromozome_length/2)):
            neg = 1
            if random.randint(0,1) == 1:
                neg = -1
            #generate new gene
            self.chromozome[i] = neg*random.uniform(1, 9.9)*(10**( random.randint( int(3*sin(pi*i/int(self.chromozome_length/2))-1) ,
                                                                                  int(3*sin(pi*i/int(self.chromozome_length/2))+1)) ))/10000    #*tmp - tmp #((2.0*tmp*random.randint(0, 4096))/4096 - tmp)
        
        for i in range(int(self.chromozome_length/2), self.chromozome_length):
            neg = 1
            if random.randint(0,1) == 1:
                neg = -1
            #generate new gene
            self.chromozome[i] = neg*random.uniform(1, 9.9)*(10**( -1*(  random.randint(i-int(self.chromozome_length/2), i) ) ) )/10000

        self.computeFitness()

    def randomNumber(self, i):
        tmp = 0.9**i
        rand_num = random.uniform(0, 2048.0)/2048*tmp - tmp
        return rand_num
        """
        old random generator
        tmp = 0.5**i
                self.chromozome[i] += (2.0*tmp*random.randint(0, 4096)/4096 - tmp)
        """


    def useFunction(self, x):
        result = 0
        for i in range(0, self.chromozome_length):
            #coef*x^i
            result+=self.chromozome[i]*(x**i)
        
        return result

    def computeFitness(self):
        self.fitness = 0

        frm_index = self.start_point
        to_index =  self.end_point
        im = 0
        N = 0
        for i in np.arange(frm_index, to_index, 0.55):
            N+=1
            self.fitness += (sin(i)-self.useFunction(i))**2

        self.fitness /= (N)

    def getFitness(self):
        return self.fitness

    def crossover(self, individual):
        oper = random.randint(0, 1)
        point = random.randint(0, self.chromozome_length-1)
      
        if oper==1:
            #swap end part
            for i in range(point, self.chromozome_length):
                tmp = self.chromozome[i]
                self.chromozome[i] = individual.chromozome[i]
                individual.chromozome[i] = tmp 
        else:
            #swap begin part
            for i in range(0, point):
                tmp = self.chromozome[i]
                self.chromozome[i] = individual.chromozome[i]
                individual.chromozome[i] = tmp    
            
        self.computeFitness()
        individual.computeFitness()

        return np.array([self, individual])

        """
        old crossover methods
        if oper == 0:
            for i in range(0, point):
                tmp = self.chromozome[i]
                self.chromozome[i] = individual.chromozome[i]
                individual.chromozome[i] = tmp     
        """     
        """" 
            elif oper==2:
            for i in range(point, self.chromozome_length):
                if random.random() < 0.5:
                    tmp = self.chromozome[i]
                    self.chromozome[i] = individual.chromozome[i]
                    individual.chromozome[i] = tmp """
    
    def mutate(self, mut_prob):
        for i in range(0, int(self.chromozome_length/2)):
            #tmp = 0.5**i
            if mut_prob < random.random():
                neg = 1
                if random.randint(0,1) == 1:
                    neg = -1
                #new random gene, (old+new)/2, first half part
                self.chromozome[i] = (neg*random.uniform(1, 9.9)*(10**( random.randint( int(3*sin(pi*i/int(self.chromozome_length/2))-1) ,
                                                                                        int(3*sin(pi*i/int(self.chromozome_length/2))+1)) ))/10000  
                                                                                        + self.chromozome[i] )/2                                    #old code  |*tmp - tmp #((2.0*tmp*random.randint(0, 4096))/4096 - tmp#self.randomNumber(i)#(self.randomNumber(i) + neg*random.uniform(1, 9.9)*(10**(3*sin(pi*i/int(self.chromozome_length/2))-1)))/2#*tmp - tmp #((2.0*tmp*random.randint(0, 4096))/4096 - tmp)
        
        for i in range(int(self.chromozome_length/2), self.chromozome_length):
            if mut_prob < random.random():
                neg = 1
                if random.randint(0,1) == 1:
                    neg = -1
                #new random gene, (old+new)/2, second half part
                self.chromozome[i] = (neg*random.uniform(1, 9.9)*(10**( -1*( random.randint(i-int(self.chromozome_length/2), i) )) )/10000 
                                        +self.chromozome[i])/2                                                                                      #old code |self.randomNumber(i)#(neg*random.uniform(1, 9.9)*(10**( -1*( random.randint(i-int(self.chromozome_length/2), i) )) ) )/2
        """
        old mutation
        for i in range(0, self.chromozome_length):
            if mut_prob < random.random():
                #tmp = 0.5**i#round((self.chromozome[i]+self.randomNumber())/2, 6)
                self.chromozome[i] = (self.chromozome[i]+ self.randomNumber(i))/2#2.0*tmp*random.randint(0, 4096)/4096 - tmp)
        """
    
    def repairOperator(self):
        #new two individuals for testing
        plus_first = Individual(False, self.chromozome_length)
        minus_first = Individual(False, self.chromozome_length)
        #store in new individuals genes with changed sign
        for i in range(0, self.chromozome_length):
            if i % 2 == 0:
                plus_first.chromozome[i] = +abs(self.chromozome[i])
                minus_first.chromozome[i] = -abs(self.chromozome[i])
            else:
                plus_first.chromozome[i] = -abs(self.chromozome[i])
                minus_first.chromozome[i] = +abs(self.chromozome[i])
        #compute fitness of new individuals
        plus_first.computeFitness()
        minus_first.computeFitness()
        #if one of the individuals is better, use it's chromozome
        if plus_first.getFitness() < minus_first.getFitness():
            if plus_first.getFitness() < self.fitness:
                self.chromozome = plus_first.chromozome
                self.fitness = plus_first.getFitness()
        else:
            if minus_first.getFitness() < self.fitness:
                self.chromozome = minus_first.chromozome
                self.fitness = minus_first.getFitness()

        
        """
        old repair operator
        repair_x = list()
        repair_y = list()
        for i in np.arange(self.start_point, self.end_point, pi/2):
            tmp_list = list()
            for j in range(0, self.chromozome_length):
                tmp_list.append(i**j)
            repair_x.append(tmp_list)
            repair_y.append(2*sin(2*i))

        print("list: ", repair_x)
        print("----------------------")

        poly = PolynomialFeatures(degree=self.chromozome_length)
        #X_ = poly.fit_transform(repair_x)

        lg = LinearRegression(normalize=True)

        lg.fit(repair_x, repair_y)
        
        for i in range(0, self.chromozome_length):
            self.chromozome[i] = lg.coef_[i]

        self.computeFitness()
        """


    def deepCopy(self):
        new_individual = Individual(False, self.chromozome_length)

        for i in range(0, self.chromozome_length):
            new_individual.chromozome[i] = self.chromozome[i]
        
        new_individual.fitness = self.fitness

        return new_individual

    def toString(self):
        output = ""

        for i in range(0, self.chromozome_length):
            if self.chromozome[i] >= 0 and i != 0:
                output+="+"
            output+= str(self.chromozome[i])+"x^"+str(i)+" "
        
        return output





#-------------------------------------------------------------------------------------
class IndividualRandomFunction:
    def __init__(self, rand_chrom, data_len=3):
        #fitness
        self.fitness = None
        #mse error
        self.mse = None
        #generate new random chromozome
        if rand_chrom == False:
            self.chromozome_length = data_len
        else:
            self.chromozome_length = random.randint(int(3*data_len/4), data_len)
        #new chromozome
        self.chromozome = ChromozomeTree(self.chromozome_length, rand_chrom)#np.empty(self.chromozome_length, dtype=float)
        
        #range to aproximate
        self.start_point = -10*pi
        self.end_point   =  10*pi

        #compute fitness and repair
        if rand_chrom == True:
            self.computeFitness()
            self.repairOperator()

   
    def computeFitness(self):
        self.fitness = 0

        frm_index = self.start_point
        to_index =  self.end_point
        im = 0
        N = 0
        #(1/N)*sum(abs(sin(i)-f(i)))
        for i in np.arange(frm_index, to_index, 0.55):
            N+=1
            self.fitness += abs(sin(i)-self.useFunction(i))
        
        self.fitness /= (N)
        self.fitness *= self.chromozome_length

        """
        old code
        if self.fitness == None:
            frm_index = self.start_point
            to_index = self.end_point
            self.fitness = 0
            self.mse=0
            for i in np.arange(frm_index, to_index, 0.56):
                result = self.chromozome.getValue(i)
                self.fitness += abs(sin(i)-result)
                self.mse+= (sin(i)-result)**2

            self.mse/=abs(-frm_index+to_index)
            self.fitness*=self.chromozome.length
            """
    
    def useFunction(self, x):
        return self.chromozome.getValue(x)

    def getFitness(self):
        return self.fitness

    def mutate(self, mut_prob):
        #remove gene with prob
        if (mut_prob < random.random()) and self.chromozome.length >=64:
            random_len = random.randint(int(3*self.chromozome.length/4), self.chromozome.length-2)
            new_chromozome = NPArray(random_len, int)
            new_param = NPArray(random_len+1, float)

            if random.random() < 0.5:
                #from end
                for i in range(0, random_len):
                    new_chromozome.append(self.chromozome.chromozome[i])
                    new_param.append(self.chromozome.parameters[i])
                new_param.append(self.chromozome.parameters[random_len])
            else:
                #from begin
                for i in range(self.chromozome.length-random_len, self.chromozome.length):
                    new_chromozome.append(self.chromozome.chromozome[i])
                    new_param.append(self.chromozome.parameters[i])
                new_param.append(self.chromozome.parameters[self.chromozome.length])

            #Save new chromozome and length
            self.chromozome.chromozome = new_chromozome.getArr()
            self.chromozome.parameters = new_param.getArr()
            self.chromozome.length = random_len
            self.chromozome_length = random_len
            
        #change op with prob
        for i in range(0, self.chromozome.length):
            if random.random() < mut_prob:
                self.chromozome.chromozome[i] = random.randint(1, 4)

        self.repairOperator()

    
    def crossover(self, individual):
        #make new random points in both array
        first_random = random.randint(1, self.chromozome_length-1)
        second_random = random.randint(1, individual.chromozome_length-1)
        #calculate length of both arrays
        first_len = first_random + (individual.chromozome_length - second_random)
        second_len = second_random + (self.chromozome_length - first_random)
        #make arrays
        first_array = NPArray(first_len, int)
        second_array = NPArray(second_len, int)
        #make new individuals
        first_one = IndividualRandomFunction(False, first_len)
        second_one = IndividualRandomFunction(False, second_len)
        #change chromozomes first part
        for i in range(0, first_random):
            first_array.append(self.chromozome.chromozome[i])
        for i in range(0, second_random):
            second_array.append(individual.chromozome.chromozome[i])
        #change chromozomes second part
        for i in range(second_random, individual.chromozome_length):
            first_array.append(individual.chromozome.chromozome[i])
        for i in range(first_random, self.chromozome_length):
            second_array.append(self.chromozome.chromozome[i])
        #get arrays
        first_one.chromozome.chromozome = first_array.getArr()
        second_one.chromozome.chromozome = second_array.getArr()

        #Repair new individuals
        first_one.repairOperator()
        second_one.repairOperator()

        return np.array([first_one, second_one])
        
    def repairOperator(self):
        result = 1
        #Repair posible zeros in equation
        for i in range(0, self.chromozome.length):
            if self.chromozome.chromozome[i] == 1:#+
                if result == -1:
                    self.chromozome.chromozome[i] = 2
                    result-=1
            elif self.chromozome.chromozome[i] == 2:#-
                if result==1:
                    self.chromozome.chromozome[i] = 1
                    result+=1

    def deepCopy(self):
        #make new infividual
        new_individual = IndividualRandomFunction(False, self.chromozome_length)
        #copy parameters and chromozome
        for i in range(0, self.chromozome_length):
            #print("i: ", i)
            new_individual.chromozome.chromozome[i] = self.chromozome.chromozome[i]
        #get fitness
        new_individual.fitness = self.fitness
        #return new clone
        return new_individual


    def toString(self):
        output = ""
        pre_str = ""
        for i in range(0, self.chromozome.length):
            pre_str+="("
            
            output+=str(self.chromozome.getPar(i))+")"
            
            output+=str(self.chromozome.getOp(i))

        output+=str(self.chromozome.getPar(self.chromozome_length))

        return pre_str+output

    #------------------------------------------------------------------------
"""
    old code
    def useAsFunction(self, x):
        result = 0
        #print("one chrom-------------")
        for i in range(0, self.chromozome_length):
            #if i%2==1:
            result += self.chromozome[i]*(x**i)

        return result

    def computeFitness(self):
        if self.fitness == None:
            frm_index = 0#pi*(-10)
            to_index = pi#*(10)
            self.fitness = 0
            for i in np.arange(frm_index, to_index, 0.1):
                self.fitness += abs((sin(i))-self.useAsFunction(i))
            

    def getFitness(self):
        return self.fitness

    def mutate(self, mut_prob):
        for gene in self.chromozome:
                if random.random() < mut_prob:
                    gene = (gene+random.random())/2

    def crossover(self, individual):
        first_one = Individual(False)
        second_one = Individual(False)

        for i in range(0, self.chromozome_length):
            if random.random()<=0.5:
                first_one.chromozome[i] = self.chromozome[i]
                second_one.chromozome[i] = individual.chromozome[i]
            else:
                first_one.chromozome[i] = individual.chromozome[i]
                second_one.chromozome[i] = self.chromozome[i]
        for i in range(0, rand_int):
            first_one.chromozome[i] = self.chromozome[i]
            second_one.chromozome[i] = individual.chromozome[i]
        for i in range(rand_int, self.chromozome_length):
            first_one.chromozome[i] = individual.chromozome[i]
            second_one.chromozome[i] = self.chromozome[i]
        return np.array([first_one, second_one])

    def deepCopy(self):
        new_individual = Individual(False)
        for i in range(0, self.chromozome_length):
            new_individual.chromozome[i] = self.chromozome[i]
        new_individual.fitness = self.fitness
        return new_individual

    def toString(self):
        output = ""
        for i in range(0, self.chromozome_length):
            sign = ""
            if self.chromozome[i] >= 0:
                sign = "+"
            output += sign + "" + str(self.chromozome[i]) + "x^(" + str(i) + ") "
        print(output)
    """

