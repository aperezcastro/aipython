from mesa.visualization.modules import CanvasGrid

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from machineLearning.kmedias.kmedias_model.model_kmedias import Kmedias

from machineLearning.kmedias.kmedias_model.model_kmedias import Cell
from machineLearning.kmedias.kmedias_model.model_kmedias import Topic

from util.Util import colors


def pso_portrayal(agent):

    if agent is None:
        return

    if type(agent) is Cell:
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        (x, y) = agent.get_pos()
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = colors[agent.get_color()]
    elif type(agent) is Topic:
        portrayal = {"Shape": "circle", "r": 0.5, "Filled": "false", "Layer": 1}
        (x, y) = agent.get_pos()
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = colors[agent.get_color()]
    else:
        portrayal = {"Shape": "circle", "r": 1, "Filled": "false", "Layer": 2}
        (x, y) = agent.get_pos()
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = colors[agent.get_color()]

    return portrayal


grid_width = 50
grid_height = 50
canvas_width = 500
canvas_height = 500

model_params = {
    "initial_topics": UserSettableParameter("slider", "initial_topics", 100, 1, 1000, 1),
    "agrupados": UserSettableParameter('checkbox', 'agrupados', value=True),
    "dispersion": UserSettableParameter("slider", "dispersion", 5, 1, 100, 1),
    "tam_dispersion": UserSettableParameter("slider", "tam_dispersion", 2, 1, 10, 1),
    "num_cluster": UserSettableParameter("slider", "num_cluster", 5, 1, 20, 1),
    "tolerancia": 0,
    "representar_areas": UserSettableParameter('checkbox', 'representar_areas', value=True),
    "height": grid_height,
    "width": grid_width
}

canvas_element = CanvasGrid(pso_portrayal, grid_width, grid_height, canvas_width, canvas_height)

server = ModularServer(Kmedias, [canvas_element], "K medias", model_params)