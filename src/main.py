from evolution import Evolution
import individual
import sys
from tkinter import *

def makeWindow():
    #make tkinter
    window = Tk()

    window.title("Aproximation of sine")

    window.geometry('700x700')

    #generations
    gen_txt = Label(window, text="Generations")

    gen_txt.grid(column=0, row=2)

    gen = Spinbox(window, from_=0, to=100, width=5)

    gen.grid(column=1,row=2)

    #mutation prob
    mut_txt = Label(window, text="Mutation prob.")

    mut_txt.grid(column=0, row=3)

    mut = Spinbox(window, from_=0, to=100, width=5)

    mut.grid(column=1,row=3)

    #cross prob
    cross_txt = Label(window, text="Crossover prob.")

    cross_txt.grid(column=0, row=4)

    cross = Spinbox(window, from_=0, to=100, width=5)

    cross.grid(column=1,row=4)

    #population size
    popul_txt = Label(window, text="Population size")

    popul_txt.grid(column=0, row=5)

    popul = Spinbox(window, from_=0, to=100, width=5)

    popul.grid(column=1,row=5)

    #population size
    poly_txt = Label(window, text="Polynom level")

    poly_txt.grid(column=0, row=6)

    poly = Spinbox(window, from_=0, to=100, width=5)

    poly.grid(column=1,row=6)

    #used mode 
    v = IntVar()

    Radiobutton(window, text="Polynom reg.", variable=v, value=1).grid(column=0, row=7)
    Radiobutton(window, text="Random func.", variable=v, value=2).grid(column=0, row=8)

    #button
    btn = Button(window, text="process", command=lambda: clicked(window, int(gen.get()), float(mut.get()), float(cross.get()), int(popul.get()), int(poly.get()), int(v.get()) ))

    btn.grid(column=0, row=9)

    btn_exit = Button(window, text="end", command=lambda: sys.exit())
    btn_exit.grid(column=0, row=10)

    window.mainloop()

def clicked(window, generations, mutation_prob, crossover_prob, population_size, poly, mode):
    if mode != 0 and generations != 0 and population_size != 0 and poly != 0:
        #create first evolution
        evol = Evolution(generations, population_size, crossover_prob, mutation_prob, poly, window, mode)
        #run first evolution
        evol.run()
    

def main():
    makeWindow()


if __name__ == "__main__":
    main()