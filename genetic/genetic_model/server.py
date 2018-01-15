from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import TextElement as Te

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model_genetic_n_queens import GeneticNQueens
from .model_genetic_n_queens import Cell


class BestText(Te):
    def __init__(self):
        super().__init__()

    def render(self, model):
        return "Best: " + str(model.best.content) + " Fitness: " + str(model.best.fitness)


def pso_portrayal(agent):
    if agent is None:
        return

    if type(agent) is Cell:
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}

        colors = {"white": "#FFFFFF",
                  "black": "#000000"
                  }
        portrayal["Color"] = colors[agent.get_color()]
    else:
        portrayal = {"Shape": "genetic_model/resources/queen.png",
                     "Layer": 1, "scale": 0.8}
    return portrayal


canvas_width = 500
canvas_height = 500

best_text = BestText()

fitness_chart = ChartModule([{"Label": "Best", "Color": "green"},
                             {"Label": "Average", "Color": "blue"},
                             {"Label": "Worst", "Color": "red"}
                             ])

diversity_chart = ChartModule([{"Label": "Diversity", "Color": "green"}])

model_params = {
    "population": UserSettableParameter("slider", "Population", 200, 0, 1000, 1),
    "num_iters": UserSettableParameter("slider", "Num_iters", 100, 0, 1000, 1),
    "crossover_ratio": UserSettableParameter("slider", "Crossover_ratio", 70, 0, 100, 1),
    "mutation_ratio": UserSettableParameter("slider", "Mutation_ratio", 0.5, 0, 10, 0.1),
    "n_queens": UserSettableParameter("slider", "N_queens", 8, 4, 10, 1),
}

grid_width = model_params["n_queens"].max_value
grid_height = grid_width

canvas_element = CanvasGrid(pso_portrayal, grid_width, grid_height, canvas_width, canvas_height)

server = ModularServer(GeneticNQueens, [canvas_element, best_text, fitness_chart, diversity_chart], "Genetic N Queens", model_params)
