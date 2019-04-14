from pathlib import Path
from player import Player
import pygame

class Stalker(Player):
    
    img = pygame.transform.scale(pygame.image.load(str(Path("./data/images/stalker_images/stalker_fish0.png"))), (35, 35))

    speed = 3
    
    def __init__(self, size: tuple, location: tuple = (0, 0)):
        self.image = Stalker.img
        self.health = 1
        self.side_size = 35
        self._location = location
        self._index = 0
        self._standing_still_animation_frames = [
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/stalker_images/stalker_fish0.png"))), (self.side_size, self.side_size)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/stalker_images/stalker_fish1.png"))), (self.side_size, self.side_size)),
            ]
        self.rect = pygame.Rect(self._location[0], self._location[1], 30, 30)
        
    def update(self, vector_direction):
        if pygame.time.get_ticks() % 3 == 0:
            self._index += 1
            if self._index >= len(self._standing_still_animation_frames):
                self._index = 0
            self.image = self._standing_still_animation_frames[self._index]
        
        vector_direction = pygame.math.Vector2(vector_direction).normalize()
        self._location = (self._location[0] + vector_direction[0]*Stalker.speed,
                         self._location[1] + vector_direction[1]*Stalker.speed)
        
        self.rect = pygame.Rect(self._location[0], self._location[1], 30, 30)
