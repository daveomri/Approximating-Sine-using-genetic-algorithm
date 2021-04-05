# author David Omrai

from individual import Individual, IndividualRandomFunction
import numpy as np
from numpy_array import NPArray
import random

class Population:
    def __init__(self, population_size, poly_size, mode):
        #Number of individuals to join turnament
        self.turnament_count = random.randint(int(population_size/4), int(population_size/3))
        #Population size
        self.population_size = population_size
        #Populations, array of individuals
        self.population = np.empty(population_size, dtype=object)
        #Size of polynom
        self.poly_size = poly_size
        #Used method
        self.mode = mode
        for i in range(0, population_size):
            if mode == 1:
                #Regresion method
                self.population[i] = Individual(True, poly_size)
            else:
                #Random function method
                self.population[i] = IndividualRandomFunction(True, poly_size)

    def selectIndividuals(self, number):
        """
        Select number of individuals from population
        turnament selection
        """
        #check if parameters are correct
        if number > self.turnament_count or number > self.population_size:
            return None
        #array for tournament
        tournament_individuals = NPArray(self.turnament_count, object)
        #get random permutation of population
        perm = np.random.permutation(self.population_size)
        for i in range(0, self.turnament_count):
            tournament_individuals.append(self.population[perm[i]])
        arr = tournament_individuals.getArr()
        sorted(arr, key=lambda x: x.getFitness())
        #get best elements
        return arr[-number-1:-1]
    
    def replacePopulation(self, new_population):
        self.population = new_population

    def getAvgFitness(self):
        avg_fitness = 0
        num = 0
        #Sum all fitnesses
        for x in self.population:
            num+=1
            avg_fitness+= x.getFitness()
        #Devide sum with number of individuals
        return avg_fitness/num
    
    def getBestFitness(self):
        return self.getBestIndividual().getFitness()

    def getBestIndividual(self):
        #Save first individual
        best_individual = self.population[0]
        #Find better individual
        for x in self.population:
            if x.getFitness() < best_individual.getFitness():
                best_individual = x
        
        return best_individual
