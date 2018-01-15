from mesa.visualization.modules import CanvasGrid

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from machineLearning.kvecinos.kvecinos_model.model_kvecinos import Kvecinos
from machineLearning.kvecinos.kvecinos_model.model_kvecinos import Cell


def pso_portrayal(agent):
    colors = {"white": "#FFFFFF",
              "black": "#000000",
              "cyan": "#E0FFFF",
              "sky": "#87CEE8",
              "blue": "#0000FF",
              "violet": "#EE82EE",
              "green0": "#FFFF99",
              "green1": "#D5F5E3",
              "red": "#FF0000",
              "orange": "#DC7633"
              }

    if agent is None:
        return

    if type(agent) is Cell:
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        (x, y) = agent.get_pos()
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = colors[agent.get_color()]
    else:
        portrayal = {"Shape": "circle", "r": 0.5, "Filled": "false", "Layer": 1}
        (x, y) = agent.get_pos()
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = colors["black"]

    return portrayal


grid_width = 50
grid_height = 50
canvas_width = 500
canvas_height = 500

model_params = {
    "initial_population": UserSettableParameter("slider", "initial_population", 20, 1, 100, 1),
    "n_clases": UserSettableParameter("slider", "n_clases", 3, 1, 5, 1),
    "k": UserSettableParameter("slider", "Crossover_ratio", 1, 1, 10, 1),
    "height": grid_height,
    "width": grid_width
}

canvas_element = CanvasGrid(pso_portrayal, grid_width, grid_height, canvas_width, canvas_height)

server = ModularServer(Kvecinos, [canvas_element], "K vecinos", model_params)
