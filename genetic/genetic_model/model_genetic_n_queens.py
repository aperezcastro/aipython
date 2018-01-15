import random

from mesa.space import MultiGrid

from util.Agent import Patch

from genetic.genetic_model.model_genetic import Genetic
from genetic.genetic_model.model_genetic import Individual

from mesa.datacollection import DataCollector


class Cell(Patch):
    pass


class CellQueen(Patch):
    pass


class Queen(Individual):
    pass


class GeneticNQueens(Genetic):
    def __init__(self, population, num_iters, crossover_ratio, mutation_ratio, n_queens):
        self.n_queens = n_queens

        super().__init__(population, num_iters, crossover_ratio, mutation_ratio)
        self.grid = MultiGrid(self.n_queens, self.n_queens, False)
        self.queens = []

        self.best: Individual = None
        self.create_board()

        self.running = True

        # Captura de datos para grafica
        self.datacollector = DataCollector(
            {"Best": lambda m: m.best.fitness,
             "Average": lambda m: m.average(),
             "Worst": lambda m: m.worst(),
             "Diversity": lambda m: m.diversity()})

    def average(self):
        sum = 0
        for individual in self.individuals:
            sum += individual.fitness
        return sum / len(self.individuals)

    def worst(self):
        worst = self.individuals[0].fitness
        for individual in self.individuals[1:len(self.individuals)]:
            if worst > individual.fitness:
                worst = individual.fitness
        return worst

    def create_board(self):
        for i in range(self.n_queens):
            cell_queen = CellQueen(self.unique_id, self, (i, 0))
            self.unique_id += 1
            self.grid.place_agent(cell_queen, (i, 0))
            self.queens.append(cell_queen)
            for j in range(self.n_queens):
                color = "white" if divmod(i + j, 2)[1] == 1 else "black"
                cell = Cell(self.unique_id, self, (i,j), color)
                self.unique_id += 1
                self.grid.place_agent(cell, (i, j))
        self.update_best()

    def update_board(self):
        i = 0
        for queen in self.queens:
            self.grid.move_agent(queen, (i, self.best.content[i]))
            i += 1

    def update_best(self):
        best = self.individuals[0]
        for individual in self.individuals[1:len(self.individuals)]:
            if individual.fitness > best.fitness:
                best = individual
        self.best = best

    # Metodos de la clase padre
    def initial_population(self):
        for _ in range(self.population):
            content = [random.randint(0,self.n_queens-1) for _ in range(self.n_queens)]
            individual = Individual(self.unique_id, self, 0, content)
            self.unique_id += 1
            self.compute_fitness(individual)
            self.individuals.append(individual)

    def compute_fitness(self, individual):
        res = 0
        lis = [i for i in range(len(individual.content))]
        for i in lis:
            for j in lis[i:len(lis)]:
                if j > i:
                    res += self.threat(i, j, individual.content)
        individual.fitness = self.n_queens - res

    def threat(self, i, j, content):
        eli = content[i]
        elj = content[j]
        if (eli == elj) or\
                ((elj - eli) == (j - i)) or\
                ((elj - eli) == (i - j)):
            return 1
        return 0

    def crossover(self, content1, content2):
        cut_point = 1 + random.randint(0, len(content1) - 1)
        c1 = content1[0:cut_point] + content2[cut_point:len(content2)]
        c2 = content2[0:cut_point] + content1[cut_point:len(content1)]
        return [c1, c2]

    def mutate(self, individual):
        for i in range(len(individual.content)):
            if random.random() * 100 < self.mutation_ratio:
                individual.content[i] = random.randint(0, self.n_queens-1)

    def external_update(self):
        self.update_best()

        self.update_board()

        # Recoger datos para plot
        self.datacollector.collect(self)

        # Parada de simulacion si se encuentra solucion
        # O si se acaban las iteraciones
        if self.best.fitness == self.n_queens:
            self.running = False