from pathlib import Path
from player import Player
import pygame

class Jellyfish(Player):
    
    img = pygame.transform.scale(pygame.image.load(str(Path("./data/images/jellyfish_images/sprite_jellyfish0.png"))), (35, 35))

    
    def __init__(self, size: tuple, location: tuple = (0, 0)):
        self.image = Jellyfish.img
        self.health = 2
        self.side_size = 35
        self._location = location
        self._index = 0
        self._standing_still_animation_frames = [
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/jellyfish_images/sprite_jellyfish0.png"))), (self.side_size, self.side_size)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/jellyfish_images/sprite_jellyfish1.png"))), (self.side_size, self.side_size)),
            ]
        
    def update(self):
        if pygame.time.get_ticks() % 3 == 0:
            self._index += 1
            if self._index >= len(self._standing_still_animation_frames):
                self._index = 0
            self.img = self._standing_still_animation_frames[self._index]