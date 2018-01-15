from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import TextElement

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

# from mesa.visualization

# from mesa.visualization.TextVisualization import TextElement


from .model_PSO_sample import SamplePSO
from .model_PSO_sample import Patch


class BestText(TextElement):
    def __init__(self):
        pass
    def render(self, model):
        return "Best: " + str(model.global_best_value)

class AverageText(TextElement):
    def __init__(self):
        pass
    def render(self, model):
        return "Average: " + str(model.average())


def pso_portrayal(agent):
    if agent is None:
        return

    # portrayal = {}

    if type(agent) is Patch:
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        (x, y) = agent.get_pos()
        portrayal["x"] = x
        portrayal["y"] = y
        # Colors es un diccionario
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
                  "grey0": "#F2F4F4",
                  "grey1": "#E5E8E8",
                  "grey2": "#CCD1D1",
                  "grey3": "#B2BABB",
                  "grey4": "#99A3A4",
                  "grey5": "#7F8C8D",
                  "grey6": "#707B7C",
                  "grey7": "#616A6B",
                  "grey8": "#515A5A",
                  "grey9": "#424949"
                  }
        portrayal["Color"] = colors[agent.get_color()]
    else:
        portrayal = {"Shape": "circle", "r": 1, "Filled": "true", "Layer": 1}
        (x, y) = agent.get_pos()
        portrayal["x"] = x
        portrayal["y"] = y
        # Colors es un diccionario
        colors = {"red": "#FF0000",
                  "orange": "#DC7633"}
        portrayal["Color"] = colors[agent.get_color()]

    return portrayal


# (self, portrayal_method, grid_width, grid_height,canvas_width=500, canvas_height=500)
grid_width = 100
grid_height = 100
canvas_width = 500
canvas_height = 500

canvas_element = CanvasGrid(pso_portrayal, grid_width, grid_height, canvas_width, canvas_height)

# # El método recolector de datos lo usa este cambas
# tree_chart = ChartModule([{"Label": "Fine", "Color": "green"},
#                           {"Label": "On Fire", "Color": "red"},
#                           {"Label": "Burned Out", "Color": "black"}])
#

best_text = BestText()
average_text = AverageText()

pso_chart = ChartModule([{"Label": "Best", "Color": "green"},
                         {"Label": "Average", "Color": "red"}])

#self, population: int, dimension: int, attraction_best_global: float,
#                 attraction_best_personal: float, lim_vel_particles: float,
#                 inertia_particle: float, max_iterations: int,
#                 width: int, height: int, num_max_locales: int,
#                 suavizar_espacio: int

model_params = {
    #"population": 18,#18,
    "population": UserSettableParameter("slider", "Population", 18, 0, 50, 1),
    "dimension": 2,
    #"attraction_best_global": 1.9,
    "attraction_best_global": UserSettableParameter("slider", "attraction_best_global ", 1.9, 0, 5, 0.1),
    #"attraction_best_personal": 1.5,
    "attraction_best_personal": UserSettableParameter("slider", "attraction_best_personal", 1.5, 0, 5, 0.1),
    #"lim_vel_particles": 0.36,
    "lim_vel_particles": UserSettableParameter("slider", "lim_vel_particles", 0.36, 0, 1, 0.01),
    #"inertia_particle": 0.24,
    "inertia_particle": UserSettableParameter("slider", "inertia_particle", 0.24, 0, 1, 0.01),
    #"max_iterations": 50,
    "max_iterations": UserSettableParameter("slider", "max_iterations", 50, 0, 100, 1),
    "width": 100,
    "height": 100,
    #"num_max_locales": 21,
    "num_max_locales": UserSettableParameter("slider", "num_max_locales", 21, 0, 200, 1),
    #"suavizar_espacio": 20#20
    "suavizar_espacio": UserSettableParameter("slider", "suavizar_espacio", 20, 0, 100, 1),
    # "density": UserSettableParameter("slider", "Tree density", 0.65, 0.01, 1.0, 0.01),
    # "esquinas": UserSettableParameter('checkbox', 'Quemas esquinas', value=True)
    # "prueba": UserSettableParameter('number', 'My Number', value=123),
    # "n": UserSettableParameter('static_text', value="hola")
    # "holi": text_element
}
# server = ModularServer(ForestFire, [canvas_element, tree_chart, text_element], "Forest Fire",
#                       model_params)

server = ModularServer(SamplePSO, [canvas_element, pso_chart, best_text, average_text], "PSO Sample", model_params)
