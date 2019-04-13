class Animal:

    def __init__(self, direction, game):
        self.speed = 10      // # of times animal can move/60 frames
        self.direct = direction
        self._pos = ()
        self.game = game

    def set_pos(self, coord:tuple):
        self.pos = coord
    
    def get_pos(self):
        return self.pos
