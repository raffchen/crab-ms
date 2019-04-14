import pygame
from pathlib import Path
from player import Player

class LittleFish(Player):
    img = pygame.transform.scale(pygame.image.load(str(Path("./data/images/littlefish.png"))), (35, 35))
    def __init__(self, crab, location: tuple = (0, 0)):
        self.image = LittleFish.img
        self.health = 10
        self.location = location
        self.crab = crab
        self.speed = 5
        self.lst = lst

    def _contains(self):
        if(((crab.get_location()[0]-self.get_location()[0])**2)+\
           (crab.get_location()[0]-self.get_location()[0])**2 < 17):
            return True
        return False

    def update(self):
        if(self._contains()):
            if(self.crab.health<80):
                self.crab.health+=10
            else:
                self.crab.health = 80
            return
        elif(pygame.time.get_ticks() % 2 == 0):
            if(10<self.location[0]<690):
                self.location = (self.location[0]+speed,self.location[1])
        return self

    def get_location(self):
        return self.location()
                
        
