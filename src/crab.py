class Crab(Animal):
    def __init__(self, game):
        self._type = "crab"
        self.game = game

    def move(self, c_dict):
        if(0 <= self.pos[self.direct[0]]+self.direct[1] \
           < self.game._bounds):
            c_dict[self._type]
