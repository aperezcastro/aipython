import math
import random

from util.Agent import Turtle
from util.Agent import Patch

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation


class Topic(Turtle):
    def __init__(self, unique_id, model, pos, color="black", angle=random.randint(0, 359)):
        super().__init__(unique_id, model, pos, color, angle)
        self.clase = 0


class Cluster(Turtle):
    def __init__(self, unique_id, model, pos, color="black", angle=random.randint(0, 359)):
        super().__init__(unique_id, model, pos, color, angle)
        self.movido = True
        self.clase_color = "red"


class Cell(Patch):
    pass


class Kmedias(Model):
    def __init__(self, height, width, initial_topics, agrupados,
                 dispersion, tam_dispersion, num_cluster, tolerancia,
                 representar_areas):
        super().__init__()
        self.height = height
        self.width = width

        # Numero de topics a clasificar
        self.initial_topics = initial_topics
        self.agrupados = agrupados
        self.dispersion = dispersion
        self.tam_dispersion = tam_dispersion
        self.num_cluster = num_cluster
        self.tolerancia = tolerancia
        self.representar_areas = representar_areas

        self.unique_id=0

        # Creación del planificador y del grid
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.width, self.height, torus=False)

        self.topics = []
        self.clusters = []

        self.colors = {0: "lime",
                       1: "yellow",
                       2: "green",
                       3: "blue",
                       4: "fuchsia",
                       5: "brown"}

        self.setup()

        self.running = True

    def setup(self):
        if self.agrupados==True:
            self.setup_topics2()
        else:
            self.setup_topics()
        self.setup_cluster()

    def setup_topics(self):
        self.setup_patches("grey0")
        for _ in range(self.initial_topics):
            pos = [random.randint(0, self.width-1), random.randint(0, random.randint(0, self.height-1))]
            topic = Topic(self.unique_id, self, pos, "black")
            self.unique_id +=1
            self.grid.place_agent(topic, pos)
            self.topics.append(topic)

    def setup_topics2(self):
        self.setup_patches("grey0")
        bolsas = random.randint(1, self.dispersion)
        for _ in range(bolsas):
            pos = [random.randint(0, self.width - 1), random.randint(0, random.randint(0, self.height - 1))]
            topic = Topic(self.unique_id, self, pos, "black")
            self.unique_id += 1
            self.grid.place_agent(topic, pos)
            self.topics.append(topic)

        for _ in range(self.initial_topics - bolsas):
            # Clonar uno de los topics darle orientacion random (ya la tienen)
            # y hacer que avance 0-5 posiciones posiciones
            ram = random.randint(0, len(self.topics)-1)
            topic_father = self.topics[ram]
            pos = topic_father.pos
            topic = Topic(self.unique_id, self, pos, "black", random.randint(0, 359))
            self.unique_id += 1
            self.grid.place_agent(topic, pos)
            self.topics.append(topic)
            for _ in range(random.randint(0, self.tam_dispersion)):
                if topic.can_move():
                    topic.forward()

    def setup_patches(self, color):
        for agent, x, y in self.grid.coord_iter():
            pos = [x,y]
            cell = Cell(self.unique_id,self,pos,color)
            self.unique_id +=1
            self.grid.place_agent(cell,pos)

    def setup_cluster(self):
        # 1. Generar centros aleatorios
        for i in range(self.num_cluster):
            topic = self.topics[random.randint(0, len(self.topics)-1)]
            pos = topic.pos
            color = "red"
            cluster = Cluster(self.unique_id, self, pos, color)
            self.unique_id += 1
            self.grid.place_agent(cluster, pos)
            self.clusters.append(cluster)
            cluster.clase_color = self.colors[i]

    def step(self):
        # print("step turulu")
        # 4. Mientras algún centro de mueva
        if self.any_cluster_movido():
            # 2. Asignar un grupo a cada elemento
            for topic in self.topics:
                topic.clase = self.get_clase(topic)
                topic.color = self.colors[topic.clase]
            # Contar los elementos asignados a cada cluster
            i = 0
            for cluster in self.clusters:
                topicClase = []
                for topic in self.topics:
                    if topic.clase == i:
                        topicClase.append(topic)
                if len(topicClase) > 0:
                    centroide = self.calcular_centroide(topicClase)
                    if self.distance(centroide, cluster.pos) > 0.01:
                        cluster.movido = True
                    else:
                        cluster.movido = False
                    self.grid.move_agent(cluster, centroide)
                else:
                    x_pos = random.randint(0, self.width-1)
                    y_pos = random.randint(0, self.height-1)
                    self.grid.move_agent(cluster, [x_pos, y_pos])
                    cluster.movido = True
                i += 1

        else:
            # No se moveran más los cluster
            if self.representar_areas:
                self.areas()
                self.representar_areas = False
            else:
                self.running = False

    def areas(self):

        # Poner todos los topics en negro
        for topic in self.topics:
            topic.color = "black"

        # Colorear con color al centroide más cercano
        for (agentset, x, y) in self.grid.coord_iter():
            for agent in agentset:
                if isinstance(agent, Cell):
                    clase = self.get_clase(agent)
                    agent.color = self.colors[clase]

    def calcular_centroide(self, topicClase):
        sum_x = 0
        sum_y = 0
        for topic in topicClase:
            sum_x += topic.pos[0]
            sum_y += topic.pos[1]
        x = int(sum_x / len(topicClase))
        y = int(sum_y / len(topicClase))
        return [x,y]

    def any_cluster_movido(self):
        for c in self.clusters:
            if c.movido == True:
                return True
        return False

    def get_clase(self, topic):
        clase = 0
        distance = self.distance(topic.pos, self.clusters[0].pos)
        for i in range(1,len(self.clusters)):
            new_distance = self.distance(topic.pos, self.clusters[i].pos)
            if new_distance < distance:
                distance = new_distance
                clase = i
        return clase

    @staticmethod
    def distance(pos1, pos2):
        return math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)
