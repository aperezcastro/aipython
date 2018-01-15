from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import TextElement as Te

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from machineLearning.neuralNetworks.perceptron_model.model_perceptron import Perceptron_Model
from machineLearning.neuralNetworks.perceptron_model.model_perceptron import Cell
from util.Util import colors


class Rectas(Te):

    def __init__(self):
        super().__init__()

    def render(self, model):
        m = str(model.real[0])
        n = str(model.real[1])
        [w1, b] = model.perceptron.weight
        mp = str(w1)
        np = str(b)
        return "y= " + m + "x + " + n + " (real) <br> y= " + mp + "x + " + np + " (perceptron)"


def pso_portrayal(agent):
    if agent is None:
        return

    if type(agent) is Cell:
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        (x, y) = agent.get_pos()
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = colors[agent.get_color()]
    else:
        portrayal = {"Shape": "circle", "r": 0.7, "Filled": "false", "Layer": 1}
        (x, y) = agent.get_pos()
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = colors[agent.get_color()]

    return portrayal


grid_width = 50
grid_height = 50
canvas_width = 500
canvas_height = 500

rectas = Rectas()


model_params = {
    "data_size": UserSettableParameter("slider", "data_size", 40, 1, 100, 1),
    "height": grid_height,
    "width": grid_width
}

canvas_element = CanvasGrid(pso_portrayal, grid_width, grid_height, canvas_width, canvas_height)

server = ModularServer(Perceptron_Model, [canvas_element, rectas], "perceptron", model_params)
