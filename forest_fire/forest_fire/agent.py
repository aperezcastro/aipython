from mesa import Agent


class TreeCell(Agent):
    def __init__(self, pos, model):

        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        if self.condition == "On Fire":
            # More = esquinas para coger vecinos esquina
            for neighbor in self.model.grid.neighbor_iter(self.pos, moore=self.model.esquinas):
                if neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"

    def get_pos(self):
        return self.pos
