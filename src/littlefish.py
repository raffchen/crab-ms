import pygame
from pathlib import Path
from player import Player
import map_generator
from math import sqrt

class LittleFish(Player):
    img = pygame.transform.scale(pygame.image.load(str(Path("./data/images/littlefish.png"))), (20, 26))

    def __init__(self, crab, location: tuple = (0, 0)):
        self.image = LittleFish.img
        self.health = 10
        self._location = location
        self.crab = crab
        self.speed = 5
        self.rect = pygame.Rect(self._location[0], self._location[1], 20, 26)


    def _contains(self):
        if(sqrt(((self.crab.get_location()[0]-self.get_location()[0])**2)+\
           ((self.crab.get_location()[1]-self.get_location()[1])**2 )) < 17):
            print(sqrt(((self.crab.get_location()[0]-self.get_location()[0])**2)+\
           ((self.crab.get_location()[1]-self.get_location()[1])**2 )))
            return True
        return False

    def update(self):
        if(self._contains()):
            if(self.crab.health<80):
                self.crab.health+=10
            else:
                self.crab.health = 80
            return
        else:
            if((10>=self._location[0] and self.speed<0) or \
               (self._location[0]>=map_generator.IMAGE_WIDTH*map_generator.ABSOLUTE_BORDER_SIZE-10 and self.speed>0)):
                self.speed *=-1
                
            self._location = (self._location[0]+self.speed,self._location[1])
        self.rect = pygame.Rect(self._location[0], self._location[1], 20, 26)
        return self

    def get_location(self):
        return self._location
                
        
