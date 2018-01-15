import random
from mesa import Agent


class Patch(Agent):
    def __init__(self, unique_id: int, model: object, pos: [int]=(0, 0), color: str="white"):
        super().__init__(unique_id, model)
        self.pos = pos
        self.color = color

    def get_pos(self):
        return self.pos

    def get_color(self):
        return self.color


class Turtle(Agent):
    def __init__(self, unique_id, model, pos, color="black",
                 angle=random.randint(0, 359)):
        super().__init__(unique_id, model)

        self.pos = pos
        self.color = color
        self.angle = angle

        # Se ha de crear el patch antes que la tortuga
        # ? Necesario añadir el patch

        self.patch = None if self.model.grid is None else self.get_patch()

    def get_color(self):
        return self.color

    def get_pos(self):
        return self.pos

    def can_move(self):
        # 1 2 3
        # 0 x 4
        # 7 6 5
        width = self.model.width
        height = self.model.height
        x = self.pos[0]
        y = self.pos[1]
        direction = int(((self.angle + 22.5) % 360) / 45)
        possible = {0: x > 0,
                    1: x > 0 and y > 0,
                    2: y > 0,
                    3: x < width - 1 and y > 0,
                    4: x < width - 1,
                    5: x < width - 1 and y < height - 1,
                    6: y < height - 1,
                    7: x > 0 and y < height - 1
                    }
        return possible[direction]

    def forward(self):  # Paso hacia adelante
        # 1 2 3
        # 0 x 4
        # 7 6 5
        direction = int(((self.angle + 22.5) % 360) / 45)
        x = self.pos[0]
        y = self.pos[1]
        new_position = {0: (x - 1, y),
                        1: (x - 1, y - 1),
                        2: (x, y - 1),
                        3: (x + 1, y - 1),
                        4: (x + 1, y),
                        5: (x + 1, y + 1),
                        6: (x, y + 1),
                        7: (x - 1, y + 1)
                        }
        self.model.grid.move_agent(self, new_position[direction])
        self.patch = self.get_patch()

    def get_patch(self):  # Coger el patch sobre el que se está
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        patch = [obj for obj in this_cell if isinstance(obj, Patch)]
        return patch[0]

    def rotate(self, angle):  # Cambiar orientación de hormiga
        self.angle += angle
        self.angle %= 360

    def patch_right_and_ahead(self, angle):
        direction = int(((self.angle + 22.5 + angle) % 360) / 45)
        x = self.pos[0]
        y = self.pos[1]
        new_position = {0: (x - 1, y),
                        1: (x - 1, y - 1),
                        2: (x, y - 1),
                        3: (x + 1, y - 1),
                        4: (x + 1, y),
                        5: (x + 1, y + 1),
                        6: (x, y + 1),
                        7: (x - 1, y + 1)
                        }

        patch_position = new_position[direction]
        if (patch_position[0] < 0) or \
                (patch_position[0] > self.model.width-1) or \
                (patch_position[1] < 0) or \
                (patch_position[1] > self.model.height-1):
            return None
        else:
            other_cell = self.model.grid.get_cell_list_contents([patch_position])
            patch = [obj for obj in other_cell if isinstance(obj, Patch)]
            return patch[0]
