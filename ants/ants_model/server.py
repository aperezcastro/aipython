from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from .model import World
from .model import Patch


def ants_portrayal(agent):
    if agent is None:
        return

    if type(agent) is Patch:
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        [x, y] = agent.get_pos()
        portrayal["x"] = x
        portrayal["y"] = y
        colors = {"white": "#FFFFFF",
                  "black": "#000000",
                  "cyan": "#E0FFFF",
                  "sky": "#87CEE8",
                  "blue": "#0000FF",
                  "violet": "#EE82EE",
                  "green0": "#FFFF99",
                  "green1": "#D5F5E3",
                  "green2": "#ABEBC6",
                  "green3": "#82E0AA",
                  "green4": "#58D68D",
                  "green5": "#2ECC71",
                  "green6": "#28B463",
                  "green7": "#239B56",
                  "green8": "#1D8348",
                  "green9": "#186A3B",
                  "grey": "#808080"
                  }
        portrayal["Color"] = colors[agent.get_color()]
    else:
        portrayal = {"Shape": "circle", "r": 1, "Filled": "true", "Layer": 1}
        (x, y) = agent.get_pos()
        portrayal["x"] = x
        portrayal["y"] = y
        colors = {"red": "#FF0000",
                  "orange": "#DC7633"}
        portrayal["Color"] = colors[agent.get_color()]

    return portrayal


grid_width = 70
grid_height = 70
canvas_width = 500
canvas_height = 500

canvas_element = CanvasGrid(ants_portrayal, grid_width, grid_height, canvas_width, canvas_height)

model_params = {
    "height": 70,
    "width": 70
}

server = ModularServer(World, [canvas_element], "Ants", model_params)
