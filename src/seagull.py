from pathlib import Path
from player import Player
import pygame

class Seagull(Player):
    def __init__(self, image: str, size: tuple, background, location: tuple = (0, 0)):
        Player.__init__(self, image, size, location)
        self.direction = choice(["up", "left", "down", "right",
                                 "left-up", "right-up", "left-down", "right-down"])
        self.background = background

    def move(self):
        moves = {"up": (0, random()*-5), "left": (random()*-5, 0), "down": (0, random()*5), "right": (random()*5, 0),
                 "left-up": (random()*-3, random()*-3), "right-up": (random()*3, random()*-3),
                 "left-down": (random()*-3, random()*3), "right-down": (random()*3, random()*3)}
        
        vertical_adjustment = 350
        horizontal_adjustment = 250
        if ((self.direction == "up" and not self.rect.top < self.background.rect.top+vertical_adjustment)
            or (self.direction == "left" and not self.rect.left < self.background.rect.left+horizontal_adjustment)
            or (self.direction == "down" and not self.rect.bottom > self.background.rect.bottom-vertical_adjustment)
            or (self.direction == "right" and not self.rect.right > self.background.rect.right-horizontal_adjustment)
            or (self.direction == "left-up" and not (self.rect.top < self.background.rect.top+vertical_adjustment or
                                                     self.rect.left < self.background.rect.left+horizontal_adjustment))
            or (self.direction == "right-up" and not (self.rect.top < self.background.rect.top+vertical_adjustment or
                                                      self.rect.right > self.background.rect.right-horizontal_adjustment))
            or (self.direction == "left-down" and not (self.rect.bottom > self.background.rect.bottom-vertical_adjustment or
                                                       self.rect.left < self.background.rect.left+horizontal_adjustment))
            or (self.direction == "right-down" and not (self.rect.bottom > self.background.rect.bottom-vertical_adjustment or
                                                        self.rect.right > self.background.rect.right-horizontal_adjustment))):
            self.rect = self.rect.move(*moves[self.direction])
        else:
            self.direction = choice(["up", "left", "down", "right", "left-up", "right-up", "left-down", "right-down"])

