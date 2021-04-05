# author David Omrai

from individual import Individual
from population import Population
from numpy_array import NPArray
from tkinter import *
from numpy import arange
from math import sin, pi, sqrt

import matplotlib as mpl
mpl.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


import random

class Evolution:
    def __init__(self, generations,population_size, crossover_prob, mutation_prob, poly, window, mode):
        #Size of population
        self.population_size = population_size
        #Mutation probability
        self.mutation_prob = mutation_prob
        #Crossover probability
        self.crossover_prob = crossover_prob
        #Generations
        self.generations = generations
        #Window with visual representation of function
        self.window = window
        #Polynom size
        self.poly_level = poly
        #Mode to use
        self.mode = mode 

    def run(self):
        #Window setting
        f = Figure(figsize=(5,5))
        a = f.add_subplot(111)
        canvas = FigureCanvasTkAgg(f, master=self.window)

        #X line
        x = arange(-10*(pi), 10*(pi), 0.1)

        #Y line
        sine_y = list()
        for i in x:
            sine_y.append(sin(i))

        #Previous fitness
        prev_fitness = 0
        #initial population
        population = Population(self.population_size, self.poly_level, self.mode)
        #repair best individual
        population.getBestIndividual().repairOperator()
        
        #iterate through generations
        for generation in range(0, self.generations):
            #new population individuals
            new_population = NPArray(self.population_size, object)
            #get best individual
            new_population.append(population.getBestIndividual().deepCopy())
            #append individuals to new population
            while new_population.getRealSize() != self.population_size:
                #get parents
                parents = population.selectIndividuals(2)
                #get children with prob
                if random.random() <= self.crossover_prob:
                    children = parents[0].deepCopy().crossover(parents[1].deepCopy())
                else:
                    children = parents
                #mutate first child with prob
                children[0].mutate(self.mutation_prob)
                #compute fitness
                children[0].computeFitness()
                #add first child to population
                new_population.append(children[0])
                #append second child if there is place
                if new_population.getRealSize() < self.population_size:
                    children[1].mutate(self.mutation_prob)
                    children[1].computeFitness()
                    new_population.append(children[1])

            #update population
            population.replacePopulation(new_population.getArr())
            #best fitness
            best_fitness = population.getBestFitness()
            #average fitness
            avg_fitness = population.getAvgFitness()
            #best individual
            best_individual = population.getBestIndividual()
            best_individual.repairOperator()

            #Print info
            print("----------------------------------------------------------------")
            print(generation, " generetion")
            print("best fitness: ", best_fitness, "| avarge fitness: ", avg_fitness)
            print(best_individual.toString())

            #Refrest graph
            if prev_fitness != best_individual.getFitness():
                a.clear()

                y = list()
                for i in x:
                    y.append(best_individual.useFunction(i))
                
                a.set_ylim(-2, 2)

                a.plot(x, sine_y, color="red", label="sine")
                a.plot(x, y, color="green", label="approx")
                
                a.axhline(y=0, color="black", linestyle=":")
                a.axvline(color="black", linestyle=":")

                #canvas.show()
                canvas.get_tk_widget().grid(column=20, row=20)#side=BOTTOM, fill=BOTH, expand=True
                
                canvas.draw_idle()

                self.window.update_idletasks()
                self.window.update()

                prev_fitness = best_individual.getFitness()
            
        #End of generations
        print(" End of Evolution")
