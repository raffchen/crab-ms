from pathlib import Path
from player import Player
import pygame

class Squid(Player):
    
    img = pygame.transform.scale(pygame.image.load(str(Path("./data/images/squid_images/squid0.png"))), (35, 35))

    
    def __init__(self, size: tuple, location: tuple = (0, 0)):
        self.image = Squid.img
        self.health = 1
        self.side_size = 35
        self._location = location
        self._index = 0
        self._standing_still_animation_frames = [
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/squid_images/squid0.png"))), (self.side_size, self.side_size)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/squid_images/squid1.png"))), (self.side_size, self.side_size)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/squid_images/squid2.png"))), (self.side_size, self.side_size)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/squid_images/squid3.png"))), (self.side_size, self.side_size)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/squid_images/squid4.png"))), (self.side_size, self.side_size)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/squid_images/squid5.png"))), (self.side_size, self.side_size)),
            ]
        self.rect = pygame.Rect(self._location[0], self._location[1], 30, 30)
        
    def update(self, vector_direction):
        if pygame.time.get_ticks() % 3 == 0:
            self._index += 1
            if self._index >= len(self._standing_still_animation_frames):
                self._index = 0
            self.image = self._standing_still_animation_frames[self._index]
        self.rect = pygame.Rect(self._location[0], self._location[1], 30, 30)
        self.vector_direction = vector_direction
        
