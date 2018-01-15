import copy
import math
import random

from util.Agent import Turtle

from mesa import Model
from mesa.time import RandomActivation


class Individual(Turtle):
    def __init__(self, unique_id, model, fitness, content, pos=(0, 0), color="white"):
        super().__init__(unique_id, model, pos, color)
        self.content = content
        self.fitness = fitness


class Genetic(Model):
    def __init__(self, population, num_iters, crossover_ratio, mutation_ratio):
        super().__init__()
        self.population = population
        self.num_iters = num_iters
        self.iter = 1
        self.crossover_ratio = crossover_ratio
        self.mutation_ratio = mutation_ratio

        self.unique_id = 0
        self.grid = None

        self.individuals = []
        # self.max_individual = None

        self.initial_population()
        self.schedule = RandomActivation(self)

    # ;--------------- Procedures to be customized ----------------
    def initial_population(self):
        """
        Creates the initial generation
        :return:
        """
        pass

    def compute_fitness(self, individual):
        """
        Individual report to compute its fitness
        :return:
        """
        pass

    def crossover(self, content1, content2):
        """
        Crossover procedure. It takes content from two parents and returns
        two children.
        When content is a list (as in DNA case) it uses a random cut-point to
        cut buth contents and mix them

        Devuelve una lista con los dos content
        :param content1:
        :param content2:
        :return:
        """
        return [content1, content2]

    def mutate(self, individual):
        """
        Mutation procedure. Individual procedure. Random mutation of units
        of the content.
        :param individual:
        :return:
        """
        # mutation_rate = self.mutation_rate
        pass

    def external_update(self):
        """
        Auxiliary procedure to be executed in every iteration of the main loop
        Usually to show or update some information
        :return:
        """
        pass

    # ;------------------------- Algorithm Procedures -
    def step(self):
        self.create_next_generation()
        self.external_update()
        # Parada si se exceden las iteraciones
        self.iter += 1
        if self.iter >= self.num_iters:
            self.running = False

    def create_next_generation(self):
        """
        Procedure to create the new generation from the current real.
        It selects (from fitness) the individuals to reproduce bt crossover (sexual)
        and by clonation (asexual). After that, it mutates randomly the new DNA
        sequences. The new generation replace the old real.
        :return:
        """
        # Start making a copy ot the current pool
        # Se usa copy y no deepcopy pq queremos los punteros originales
        # old_generation = copy.deepcopy(self.individuals)
        old_generation = copy.copy(self.individuals)

        # Decide how many crossover will be made (in each crossover 2 new
        # individuals will be created
        number_crossovers = math.floor(self.population * self.crossover_ratio / 100 / 2)

        # Make crossover
        for _ in range(number_crossovers):
            # Tournament 3 selection: we take 3 random individuals and choose the best
            # of them. Selectors will be the parents of the new spring.
            father1: Individual = sorted(random.sample(old_generation, 3), key=lambda i: i.fitness, reverse=True)[0]
            father2: Individual = sorted(random.sample(old_generation, 3), key=lambda i: i.fitness, reverse=True)[0]

            # Cruce
            content_child = self.crossover(father1.content, father2.content)

            # From 2 parents we create 2 children
            child1 = Individual(self.unique_id, self, father1.fitness, content_child[0], father1.pos, father1.color)
            self.unique_id += 1
            self.individuals.append(child1)
            child2 = Individual(self.unique_id, self, father2.fitness, content_child[1], father2.pos, father2.color)
            self.unique_id += 1
            self.individuals.append(child2)

        # The rest of pool will be cloned directly from good individuals of the
        # previous generation
        for _ in range(self.population - number_crossovers * 2):
            father1: Individual = sorted(random.sample(old_generation, 3), key=lambda i: i.fitness, reverse=True)[0]
            child1 = Individual(self.unique_id, self, father1.fitness, father1.content[:])
            self.unique_id += 1
            self.individuals.append(child1)

        # Remove the previous generation
        for individual in old_generation:
            self.individuals.remove(individual)

        # Mutate the new spring and compute the new fitness
        for individual in self.individuals:
            self.mutate(individual)
            self.compute_fitness(individual)

    # ;------------------------------------------------------------------------------
    # ; We provide some auxiliary procedures that calculate the diversity of the pool
    # ;  (using the Hamming distance between all individual pairs)

    # ; Provided diversity is the average of Hamming distances between all pairs
    # ; in the population.

    def diversity(self):
        distances = []
        i = 0
        for individual in self.individuals:
            i += 1
            c1 = individual.content
            for individual2 in self.individuals[i:len(self.individuals)]:
                distances.append(self.distance(c1, individual2.content))
        sum_distances = 0
        for distance in distances:
            sum_distances += distance
        return sum_distances / len(distances)

    def distance(self, c1, c2):
        return self.hamming_distance(c1, c2)

    # Hamming distance between two list is the proportion of positions
    # thet differ.
    @staticmethod
    def hamming_distance(c1, c2):
        differences = 0
        for i in range(len(c1)):
            if c1[i] != c2[i]:
                differences += 1
        return differences / len(c1)

