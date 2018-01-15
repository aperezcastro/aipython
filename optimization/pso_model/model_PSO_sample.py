import random

from mesa.datacollection import DataCollector

from optimization.pso_model.model_PSO import PSO
from optimization.pso_model.model_PSO import Particle

from mesa.space import MultiGrid

from util.Agent import Patch as Util_Patch


class Patch(Util_Patch):
    def __init__(self, unique_id, model, pos, val, color="white"):
        super().__init__(unique_id, model, pos, color)
        self.val = val

    def diffuse_val(self, diffusion_rate: float):
        # Se difumina el difussión rate entre los 8 vecinos
        # diffusion_rate es en tantos por 1
        diffuses = self.val * diffusion_rate
        self.val -= diffuses

        for patch in self.model.grid.get_neighbors(self.pos, True):
            if isinstance(patch, Patch):
                patch.val += diffuses / 8

    def set_color(self):
        color = {0: "white",
                 1: "grey1",
                 2: "grey2",
                 3: "grey3",
                 4: "grey4",
                 5: "grey5",
                 6: "grey6",
                 7: "grey7",
                 8: "grey8",
                 9: "grey9",
                 10: "black"
                 }
        n_color = int(self.val*10)
        self.color = color[n_color]


class SamplePSO(PSO):
    def __init__(self, population: int, dimension: int, attraction_best_global: float,
                 attraction_best_personal: float, lim_vel_particles: float,
                 inertia_particle: float, max_iterations: int,
                 width: int, height: int, num_max_locales: int,
                 suavizar_espacio: int):
        super().__init__(population, dimension, attraction_best_global, attraction_best_personal, lim_vel_particles,
                         inertia_particle, max_iterations)

        self.width = width
        self.height = height
        self.grid = MultiGrid(self.width, self.height, torus=False)

        # Variables para el espacio de busqueda
        self.num_max_locales = num_max_locales
        self.suavizar_espacio = suavizar_espacio

        # Crear espacio de busqueda
        self.setup_search_space()

        # Crear particulas
        # Lo hace la clase padre

        # Colocar particulas
        # Hay que adaptar pos interno al espacio de busqueda
        self.place_particles(True)

        # Captura de datos para grafica
        self.datacollector = DataCollector(
            {"Best": lambda m: m.global_best_value,
            "Average": lambda m: m.average()})

    def average(self):
        sum = 0
        for agent in self.schedule.agents:
            if isinstance(agent, Particle):
                sum += agent.personal_best_value
        return sum / self.population

    # Se modifica step del padre para añadir el collector

    def step(self):
        super().step()
        # Collect data
        self.datacollector.collect(self)
        # Stop si llega al máximo
        if self.global_best_value == 1:
            self.running = False

    def place_particles(self, initial=False):
        for particle in self.particles:
            pos = self.pos_particle_to_pos(particle)

            if initial:
                self.grid.place_agent(particle, pos)
            else:
                self.grid.move_agent(particle, pos)

    def pos_particle_to_pos(self, particle: Particle):
        # Convierte posiciones de particula [0 1] en posiciones de grid 2D
        min_xcor = 0
        max_xcor = self.width - 1
        min_ycor = 0
        max_ycor = self.height - 1
        x_cor = self.convert(particle.pos_particle[0], min_xcor, max_xcor)
        y_cor = self.convert(particle.pos_particle[1], min_ycor, max_ycor)
        return (x_cor, y_cor)

    @staticmethod
    def convert(x: float, a: float, b: float) -> int:
        # Bijection from [0, 1] to [a, b]
        return int(a + x * (b - a))

    def setup_search_space(self):
        # Preparar un espacio de busqueda con colinas y valles

        if self.num_max_locales == 0:
            for agent, x, y in self.grid.coord_iter():
                val = random.random()
                patch = Patch(self.unique_id, self, (x, y), val)
                self.unique_id += 1
                self.grid.place_agent(patch, (x, y))
        else:
            n_elements = (self.width-1)*(self.height-1)
            selected_elements = random.sample(range(n_elements), self.num_max_locales)
            element = 0
            for (agentSet, x, y) in self.grid.coord_iter():
                val = 10*random.random() if element in selected_elements else 0
                patch = Patch(self.unique_id, self, (x, y), val)
                self.unique_id += 1
                self.grid.place_agent(patch, (x, y))
                element += 1

        # Suavizado del espacio
        for _ in range(self.suavizar_espacio):
            for (agentSet, x, y) in self.grid.coord_iter():
                for agent in agentSet:
                    if isinstance(agent, Patch):
                        agent.diffuse_val(1)

        # Normalizacion del espacio 0 y 0.99999
        min_val = 0
        max_val = 0
        for (agentSet, x, y) in self.grid.coord_iter():
            for agent in agentSet:
                if isinstance(agent, Patch):
                    if agent.val < min_val:
                        min_val = agent.val
                    if agent.val > max_val:
                        max_val = agent.val
        for (agentSet, x, y) in self.grid.coord_iter():
            for agent in agentSet:
                if isinstance(agent, Patch):
                    agent.val = 0.99999 * (agent.val - min_val) / (max_val - min_val)

        # Marcar a 1 el máximo
        max_val = 0
        max_patch = None
        for (agentSet, x, y) in self.grid.coord_iter():
            for agent in agentSet:
                if isinstance(agent, Patch):
                    if agent.val > max_val:
                        max_patch = agent
        if isinstance(max_patch, Particle):
            max_patch.val = 1

        # Colorear patches
        for (agentSet, x, y) in self.grid.coord_iter():
            for agent in agentSet:
                if isinstance(agent, Patch):
                    agent.set_color()

    # Se han de definir los métodos evaluation y psoexternalUpdate

    def evaluation(self, particle: Particle):
        # Se podría usar particle.pos si se ejecutara primero pso_external_update
        # Pero se ejecuta despues

        # Hay que revisar la primera evaluación al crear particulas
        if self.grid is not None:

            pos = self.pos_particle_to_pos(particle)
            for patch in self.grid.get_cell_list_contents(pos):
                if isinstance(patch, Patch):
                    return patch.val
        else:
            return 0

    def pso_external_update(self):
        self.place_particles()
