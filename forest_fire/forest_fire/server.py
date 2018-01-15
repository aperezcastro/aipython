from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import TextElement

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import ForestFire


class NewTextElement(TextElement):

    def render(self, model):
        return "Porcentaje quemado: " + str(model.percen) + " %"


def forest_fire_portrayal(tree):
    if tree is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    colors = {"Fine": "#00AA00",
              "On Fire": "#880000",
              "Burned Out": "#000000"}
    portrayal["Color"] = colors[tree.condition]
    return portrayal


grid_width = 100
grid_height = 100
canvas_width = 500
canvas_height = 500

canvas_element = CanvasGrid(forest_fire_portrayal, grid_width, grid_height, canvas_width, canvas_height)

# El método recolector de datos lo usa este cambas
tree_chart = ChartModule([{"Label": "Fine", "Color": "green"},
                          {"Label": "On Fire", "Color": "red"},
                          {"Label": "Burned Out", "Color": "black"}])

text_element = NewTextElement()

model_params = {
    "height": 100,
    "width": 100,
    "density": UserSettableParameter("slider", "Tree density", 0.65, 0.01, 1.0, 0.01),
    "esquinas": UserSettableParameter('checkbox', 'Quemas esquinas', value=True)
}
server = ModularServer(ForestFire, [canvas_element, tree_chart, text_element], "Forest Fire",
                       model_params)
