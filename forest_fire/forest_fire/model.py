import random

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation

from .agent import TreeCell


class ForestFire(Model):
    def __init__(self, height, width, density, esquinas):
        super().__init__()
        # Parámetros para inicializar modelo
        self.height = height
        self.width = width
        self.density = density

        self.esquinas = esquinas

        self.initialTrees = 0
        self.burnedTrees = 0
        self.percen = 0

        # Creación del planificador y del grid
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)

        # Recolector de datos para gráfica
        self.datacollector = DataCollector(
            {"Fine": lambda m: self.count_type(m, "Fine"),
             "On Fire": lambda m: self.count_type(m, "On Fire"),
             "Burned Out": lambda m: self.count_type(m, "Burned Out")})

        # Creación de los agentes del modelo y configuración de parámetros
        self.setup()

        # Ejecución en navegador despues de crear
        self.running = True

    def setup(self):
        pos = list(filter(lambda t: random.random() < self.density, self.grid.coord_iter()))
        list(map(lambda t: self.add_tree(t[1], t[2]), pos))
        self.initialTrees = len(pos)

    def add_tree(self, x, y):
        new_tree = TreeCell((x, y), self)
        # Set all trees in the first column on fire.
        if x == 0:
            new_tree.condition = "On Fire"
        self.grid._place_agent((x, y), new_tree)
        self.schedule.add(new_tree)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        self.burnedTrees = self.count_type(self, "Burned Out")
        self.percen = self.burnedTrees/self.initialTrees*100

        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        return len(list(filter(lambda t: t.condition == tree_condition, model.schedule.agents)))
