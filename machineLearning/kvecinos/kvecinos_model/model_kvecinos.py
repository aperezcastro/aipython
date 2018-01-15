import math
import random

from util.Agent import Turtle
from util.Agent import Patch

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation


class Individual(Turtle):
    def step(self):
        pass


class Cell(Patch):
    def step(self):
        # todos los elementos que no sean clases
        if self not in self.model.clases:
            # Se ordena por distancia los vecinos
            # Se crean pares, distancia-color
            vecinos = []
            for vecino in self.model.clases:
                vecinos.append([self.distance(vecino), vecino.get_color()])
            # Se ordenan los vecinos por la distancia
            vecinos.sort()

            # Se corta la lista
            vecinos = vecinos[0:self.model.k]

            mode = self.mode(vecinos)
            self.color = mode


    def distance(self, vecino):
        pos1 = self.get_pos()
        pos2 = vecino.get_pos()
        return math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)

    def mode(self, vecinos):
        # Se limita a colores
        i = 0
        for vecino in vecinos:
            vecinos[i] = vecino[1]
            i += 1

        # Se ve el que tiene mas repeticiones
        max_rep = 0
        for vecino in vecinos:
            rep = vecinos.count(vecino)
            if rep > max_rep:
                max_rep = rep

        # Se cuentan todos y se coge uno al azar
        modes = []
        for vecino in vecinos:
            rep = vecinos.count(vecino)
            if rep == max_rep:
                modes.append(vecino)

        mode = random.choice(modes)
        return mode


class Kvecinos(Model):
    def __init__(self, height, width, initial_population, n_clases, k):
        super().__init__()
        self.height = height
        self.width = width
        self.initial_population = initial_population
        # N_class será el número de colores
        self.n_clases = n_clases
        self.k = k
        self.unique_id=0

        # Creación del planificador y del grid
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=False)

        self.colors = {0: "red",
                       1: "blue",
                       2: "green0",
                       3: "violet",
                       4: "cyan",
                       5: "orange"}

        self.clases = []

        self.setup()

        self.running = True

    def setup(self):
        for agent, x, y in self.grid.coord_iter():
            patch = Cell(self.unique_id,self,(x,y),"black")
            self.unique_id += 1
            self.grid.place_agent(patch, (x,y))
            self.schedule.add(patch)

        for i in range(self.initial_population):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            pos = (x, y)
            color = random.randint(0, self.n_clases-1)

            cell = self.grid.get_cell_list_contents(pos)[0]
            self.clases.append(cell)
            self.clases[i].color = self.colors[color]

            individual = Individual(self.unique_id, self, pos, self.colors[color])
            self.unique_id += 1
            self.grid.place_agent(individual,pos)

    def step(self):
        self.schedule.step()
