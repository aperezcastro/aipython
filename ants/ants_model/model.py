import random
import math

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from util.Agent import Patch as Util_Patch
from util.Agent import Turtle as Util_Turtle


class Patch(Util_Patch):
    def __init__(self, unique_id, model, pos, color="white", chemical=0,
                 food=0, is_nest=False, nest_scent=0, food_source_number=0):
        super().__init__(unique_id, model, pos, color)

        self.chemical = chemical
        self.food = food
        self.is_nest = is_nest
        self.nest_scent = nest_scent
        self.food_source_number = food_source_number

    def set_color(self):
        food_color = {1: "cyan", 2: "sky", 3: "blue"}
        if self.is_nest:
            self.color = "violet"
        elif self.food > 0:
            self.color = food_color[self.food_source_number]
        elif self.chemical > 0:
            self.set_color_chemical()

    def set_color_chemical(self):
        color = {0: "white",
                 1: "green1",
                 2: "green2",
                 3: "green3",
                 4: "green4",
                 5: "green5",
                 6: "green6",
                 7: "green7",
                 8: "green8",
                 9: "green9"
                 }
        n_color = int(self.chemical)
        if n_color > 9:
            n_color = 9
        self.color = color[n_color]

    def step(self):
        self.diffuse_chemical(self.model.diffusion_rate)
        self.evaporate_chemical(self.model.evaporation_rate)
        self.set_color()

    def diffuse_chemical(self, diffusion_rate):
        # Se difumina el difussión rate entre los 8 vecinos
        diffuses = self.chemical * (diffusion_rate / 100)
        self.chemical -= diffuses

        for patch in self.model.grid.get_neighbors(self.pos, True):
            if type(patch) == Patch:
                patch.chemical += diffuses / 8

    def evaporate_chemical(self, evaporation_rate):
        self.chemical = self.chemical * (100 - evaporation_rate) / 100


class Ant(Util_Turtle):
    def __init__(self, unique_id, model, pos, color="red",
                 angle=random.randint(0, 359)):
        super().__init__(unique_id, model, pos, color, angle)

        self.food = False

    def step(self):
        if self.color == "red":
            self.look_for_food()
        else:
            self.return_to_nest()
        self.wiggle()
        self.forward()

    def look_for_food(self):
        if self.patch.food > 0:
            self.color = "orange"
            self.patch.food -= 1
            self.rotate(180)
        # Mover en la dirección del químico
        if (self.patch.chemical >= 0.05) and (self.patch.chemical < 2):
            self.uphill_chemical()

    def return_to_nest(self):  # Buscar nido
        if self.patch.is_nest:
            self.color = "red"
            self.rotate(180)
        else:
            self.patch.chemical += 60
            self.uphill_nest_scent()

    def wiggle(self):  # Contoneo
        self.rotate(random.randint(0, 40))
        self.rotate(random.randint(-40, 0))
        if not self.can_move():
            self.rotate(180)

    def uphill_chemical(self):
        scent_ahead = self.chemical_scent_at_angle(0)
        scent_right = self.chemical_scent_at_angle(45)
        scent_left = self.chemical_scent_at_angle(-45)
        if (scent_right > scent_ahead) or (scent_left > scent_ahead):
            if scent_right > scent_left:
                self.rotate(45)
            else:
                self.rotate(-45)

    def chemical_scent_at_angle(self, angle):
        patch = self.patch_right_and_ahead(angle)
        if patch:
            return patch.chemical
        else:
            return 0

    def uphill_nest_scent(self):
        scent_ahead = self.nest_scent_at_angle(0)
        scent_rigth = self.nest_scent_at_angle(45)
        scent_left = self.nest_scent_at_angle(-45)
        if (scent_rigth > scent_ahead) or (scent_left > scent_ahead):
            if scent_rigth > scent_left:
                self.rotate(45)
            else:
                self.rotate(-45)

    def nest_scent_at_angle(self, angle):
        patch = self.patch_right_and_ahead(angle)
        if patch:
            return patch.nest_scent
        else:
            return 0


class World(Model):
    def __init__(self, width, height):
        super().__init__()
        self.height = height
        self.width = width

        self.n_ants = int(125)
        self.diffusion_rate = 50
        self.evaporation_rate = 10

        # Para dar identificador único a los agentes
        self.unique_id = 0

        # Creación del planificador y del grid
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=False)

        # Inicialización de patches
        self.setup_patches()

        # Inicialización de hormigas
        self.setup_ants()

        # Ejecución en navegador despues de crear
        self.running = True

    # Inicialización de hormigas
    def setup_ants(self):
        for i in range(self.n_ants):
            # Colocar hormigas aleatorias
            # x = random.randint(0, self.width - 1)
            # y = random.randint(0, self.height - 1)
            # pos = (x, y)
            # Colocar hormigas en el centro
            pos = (int(self.width/2)-1, int(self.height/2)-1)
            ant = Ant(self.unique_id, self, pos)
            self.unique_id += 1
            self.grid.place_agent(ant, pos)
            self.schedule.add(ant)

    # Inicialización de patches
    def setup_patches(self):
        """Inicialización del mundo"""
        # Colocar 1 patch en cada punto del grid
        for agent, x, y in self.grid.coord_iter():
            patch = Patch(self.unique_id, self, (x, y))
            self.unique_id += 1
            self.grid.place_agent(patch, (x, y))
            # Quizás no es necesario añadir al schedule
            self.schedule.add(patch)

        # Colocar Nido
        self.setup_nest()
        # Colocar Comida
        self.setup_food()
        # Colorear patches
        self.setup_color()

    def setup_nest(self):
        """Creación del nido"""
        # Se pone nido en el centro y 5 cuadros alrededor
        center = (int(self.width / 2)-1, int(self.height / 2)-1)
        for agent in self.grid.get_neighbors(center, True, True, 5):
            if isinstance(agent, Patch):
                agent.is_nest = True

        # Distancia al hormiguero
        for (agentSet, x, y) in self.grid.coord_iter():
            for agent in agentSet:
                if isinstance(agent, Patch):
                    agent.nest_scent = 200 - self.distance(center, (x, y))

    @staticmethod
    def distance(pos1, pos2):
        return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1])

    def setup_food(self):
        """Creación de la comida"""
        center = (int(self.width / 2)-1, int(self.height / 2)-1)
        center_food1 = (int(center[0] + 0.6 * center[0]), int(center[1]))
        center_food2 = (int(center[0] - 0.6 * center[0]), int(center[1] - 0.6 * center[1]))
        center_food3 = (int(center[0] - 0.8 * center[0]), int(center[1] + 0.8 * center[1]))
        for agent in self.grid.get_neighbors(center_food1, True, True, 5):
            if isinstance(agent, Patch):
                agent.food_source_number = 1
                agent.food = random.randint(1, 2)

        for agent in self.grid.get_neighbors(center_food2, True, True, 5):
            if isinstance(agent, Patch):
                agent.food_source_number = 2
                agent.food = random.randint(1, 2)

        for agent in self.grid.get_neighbors(center_food3, True, True, 5):
            if isinstance(agent, Patch):
                agent.food_source_number = 3
                agent.food = random.randint(1, 2)

    def setup_color(self):
        for (agentSet, x, y) in self.grid.coord_iter():
            for agent in agentSet:
                if isinstance(agent, Patch):
                    agent.set_color()

    def step(self):
        self.schedule.step()
