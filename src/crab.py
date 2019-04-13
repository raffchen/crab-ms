from player import Player
from pathlib import Path
import pygame

class Crab(Player):
    def __init__(self, image: str, size: tuple, location: tuple = (0, 0)):
        Player.__init__(self, image, size, location)
        self.health = 80
        self._location = location
        self.side_size = 35
        self._index = 0
        
        self._standing_still_animation_frames = [
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still0.png"))), (self.side_size, self.side_size)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still1.png"))), (self.side_size, self.side_size)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still2.png"))), (self.side_size, self.side_size)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still3.png"))), (self.side_size, self.side_size)),
            ]
        
    def update_location(self,move):
        self._location = (self._location[0]+move[0],self._location[1]+move[1])
       

    def get_location(self):
        return self._location
    
    def update(self):
        if pygame.time.get_ticks()%5 == 0:
            self._index += 1
            if self._index >= len(self._standing_still_animation_frames):
                self._index = 0
            self.img = self._standing_still_animation_frames[self._index]