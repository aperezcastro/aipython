import random
import math

from mesa import Model
from mesa.time import RandomActivation

from util.Agent import Turtle as Util_Turtle


class PSO(Model):

    def __init__(self, population: int, dimension: int, attraction_best_global: float,
                 attraction_best_personal: float, lim_vel_particles: float,
                 inertia_particle: float, max_iterations: int):
        super().__init__()

        # Number of particles to be created
        self.population = population
        # Dimension of the space search
        self.dimension = dimension

        # Propiedades para las particulas
        self.attraction_best_global = attraction_best_global
        self.attraction_best_personal = attraction_best_personal
        self.lim_vel_particles = lim_vel_particles
        self.inertia_particle = inertia_particle

        self.global_best_pos = []
        self.global_best_value = 0

        self.max_iterations = max_iterations
        self.iter = 0

        self.unique_id = 0
        self.particles = []

        self.schedule = RandomActivation(self)
        self.grid = None
        self.running = True

        self.create_particles()

    def create_particles(self):
        for _ in range(self.population):
            pos_particle = [random.random() for _ in range(self.dimension)]
            velocity = [random.normalvariate(0, 1) for _ in range(self.dimension)]

            particle = Particle(self.unique_id, self, pos_particle, velocity,
                                self.lim_vel_particles, self.inertia_particle,
                                self.attraction_best_global, self.attraction_best_personal)
            particle.personal_best_value = self.evaluation(particle)
            particle.personal_best_pos = particle.pos_particle

            self.schedule.add(particle)
            self.particles.append(particle)
            self.unique_id += 1

        best_particle = self.best_particle()
        self.global_best_value = best_particle.personal_best_value
        self.global_best_pos = best_particle.personal_best_pos

    def get_global_best_value(self) -> float:
        return self.global_best_value

    def get_global_best_pos(self) -> [float]:
        return self.global_best_pos

    def best_particle(self) -> object:
        best = self.particles[0]
        for particle in self.particles:
            if particle.personal_best_value > best.personal_best_value:
                best = particle
        return best

    def update_best(self):
        previous_best = self.best_particle()
        if previous_best.personal_best_value > self.global_best_value:
            self.global_best_value = previous_best.personal_best_value
            self.global_best_pos = previous_best.pos_particle

    def step(self):
        self.schedule.step()
        self.update_best()
        self.pso_external_update()

        self.iter += 1
        if self.iter > self.max_iterations:
            self.running = False


    def get_result(self) -> [float]:
        return [self.global_best_value, self.global_best_pos]

    def evaluation(self, particle: object) -> float:
        # Evaluation reports ther evaluation of the current particle.
        # Must be individualize to fit the necesities of the problem
        return particle.personal_best_value

    def pso_external_update(self):
        # PSO_External_Update contains the set of auxiliary actions to be
        # performed in every iteration of the main loop
        pass


class Particle(Util_Turtle):

    def __init__(self, unique_id: int, model: PSO, pos_particle: [float],
                 velocity: [float], lim_vel_particles: float,
                 inertia_particles: float, attraction_best_global: float,
                 attraction_best_personal: float):
        # Hay que distinguir la posicion de particula pos_particle
        # de la posición en un hipotético grid 2D. pos
        # Al dejarlo vacio en super se marca como [0, 0]
        pos = (0, 0)
        super().__init__(unique_id, model, pos, "red")
        self.velocity: [float] = velocity
        self.personal_best_value = 0
        self.personal_best_pos = []

        self.pos_particle = pos_particle

        self.inertia_particle = inertia_particles
        self.attraction_best_personal = attraction_best_personal
        self.attraction_best_global = attraction_best_global
        self.lim_vel_particles = lim_vel_particles

    # Llama al método de evaluación definido
    def evaluation(self) -> float:
        return self.model.evaluation(self)

    def step(self):
        self.update_velocity_position()
        self.update_best()

    def update_best(self):
        evaluation = self.evaluation()
        if evaluation > self.personal_best_value:
            self.personal_best_value = evaluation
            self.personal_best_pos = self.pos_particle

    def update_velocity_position(self):
        # Consider the inertia, scalar product
        self.velocity = self.scalar_product(self.inertia_particle, self.velocity)

        # Attraction to personal best
        to_personal_best_pos = self.scalar_diff(self.personal_best_pos, self.pos_particle)
        temp = (1 - self.inertia_particle) * self.attraction_best_personal * random.random()
        temp2 = self.scalar_product(temp, to_personal_best_pos)
        self.velocity = self.scalar_sum(temp2, self.velocity)

        # Attraction to global best
        to_global_best_pos = self.scalar_diff(self.model.get_global_best_pos(), self.pos_particle)
        temp = (1 - self.inertia_particle) * self.attraction_best_global * random.random()
        temp2 = self.scalar_product(temp, to_global_best_pos)
        self.velocity = self.scalar_sum(temp2, self.velocity)

        # Bound the velocity
        norm = self.norm(self.velocity)
        if norm > self.lim_vel_particles:
            self.velocity = self.scalar_product((self.lim_vel_particles / norm), self.velocity)

        # Update the position of the particle
        self.pos_particle = list(map(lambda x: self.cut01(x), self.scalar_sum(self.pos_particle, self.velocity)))

    @staticmethod
    def scalar_product(a: float, b: [float]) -> [float]:
        return list(map(lambda x: a * x, b))

    @staticmethod
    def scalar_diff(a: [float], b: [float]) -> [float]:
        return list(map(lambda x, y: x - y, a, b))

    @staticmethod
    def scalar_sum(a: [float], b: [float]) -> [float]:
        return list(map(lambda x, y: x + y, a, b))

    @staticmethod
    def norm(a: [float]) -> float:
        return math.sqrt(sum(list(map(lambda x: x * x, a))))

    @staticmethod
    def cut01(x: float) -> float:
        if x > 1:
            return 1
        if x < 0:
            return 0
        return x
