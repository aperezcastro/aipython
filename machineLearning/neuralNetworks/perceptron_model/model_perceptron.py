import random

from util.Agent import Turtle
from util.Agent import Patch
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation


class Cell(Patch):
    pass


class Perceptron:
    def __init__(self, weight):
        self.weight = weight


class Data(Turtle):
    def __init__(self, unique_id, model, pos, data_output=0, data_input=(0, 0), color="black", angle=0):
        super().__init__(unique_id, model, pos, color, angle)
        self.data_output = data_output     # Y (-1 C1 rojo, 1 C2 azul)
        self.data_input = data_input       # (x1, x2)


class Perceptron_Model(Model):
    def __init__(self, height, width, data_size):
        super().__init__()

        self.real = [0, 0]

        self.unique_id = 0
        self.height = height
        self.width = width
        self.data_size = data_size

        # Creación del planificador y del grid
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=False)

        self.perceptron = None
        self.datum = []

        self.setup()
        self.running = True

        self.paso = 0
        self.maxPasos = self.data_size+1

    def setup(self):
        # Create grid
        self.setup_patches_two("l_blue","l_red")

        # Create perceptron
        b = random.randint(0, self.height-1)
        w1 = random.random()*2-1
        weight = [w1, b]
        perceptron = Perceptron(weight)
        self.perceptron = perceptron

        self.colorear()

        # Create random data
        m = random.randint(-1, 1)
        n = random.randint(int(1/3*self.height), int(2/3*self.height))
        self.real = [m, n]

        for _ in range(self.data_size):
            pos = [random.randint(0, self.width-1), random.randint(0, self.height-1) ]
            data_input = pos
            xcor = pos[0]
            ycor = pos[1]
            d = m * xcor - ycor + n

            data_output = self.sign(d)  # 1 if output_angle > 0 else -1
            color = "red" if data_output == -1 else "blue"
            data = Data(self.unique_id, self, pos, data_output, data_input, color)
            self.unique_id += 1
            self.grid.place_agent(data, pos)
            self.datum.append(data)


    def setup_patches_two(self, color1, color2):
        for agent, x, y in self.grid.coord_iter():
            pos = [x, y]
            color = color1 if y > self.height/2 else color2
            cell = Cell(self.unique_id, self, pos, color)
            self.unique_id += 1
            self.grid.place_agent(cell, pos)

    def step(self):
        self.paso += 1
        if self.paso > self.maxPasos:
            self.running = False
        data = self.datum[self.paso % len(self.datum)]
        self.learn_from(data)
        self.colorear()

    def colorear(self):
        w1 = self.perceptron.weight[0]
        b = self.perceptron.weight[1]

        m = w1
        n = b

        for agent_set, x, y in self.grid.coord_iter():
            for agent in agent_set:
                if isinstance(agent, Cell):
                    pos = agent.pos
                    xcor = pos[0]
                    ycor = pos[1]
                    d = m * xcor - ycor + n
                    data_output = self.sign(d)
                    color = "l_red" if data_output == -1 else "l_blue"
                    agent.color = color

    @staticmethod
    def sign(number):
        return 1 if number > 0 else -1

    def learn_from(self, P):
        Y = P.data_output
        [xcor, ycor] = P.data_input
        [w1, b] = self.perceptron.weight
        m = w1
        n = b
        d = m * xcor - ycor + n
        data_output = self.sign(d)
        v = 0.01
        if data_output != Y:
            self.paso = 0
            if Y == 1:
                w1 = w1 + v * xcor
                b = b + 1
            else:
                w1 = w1 - v * xcor
                b = b - 1
            self.perceptron.weight = [w1, b]
