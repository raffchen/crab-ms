from player import Player
from pathlib import Path
import pygame


class Crab(Player):
    def __init__(self, image: str, size: tuple, location: tuple = (0, 0)):
        Player.__init__(self, image, size, location)
        self.health = 80
        self.side_size = 35
        self._location = location
        self._index = 0
        self._standing_still_animation_frames = [
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still0.png"))), (self.side_size, self.side_size)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still1.png"))), (self.side_size, self.side_size)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still2.png"))), (self.side_size, self.side_size)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still3.png"))), (self.side_size, self.side_size)),
            ]
        self.symptoms = {
            "loss-of-balance": {"status": False, "timer": 0},
            "fatigue": {"status": False, "timer": 0},
            "pain": {"status": False, "timer": 0},
            "vision": {"status": False, "timer": 0}
        }
        self.speed = 6

    def update_location(self, move):
        self._location = (self._location[0]+move[0], self._location[1]+move[1])
        self.rect = pygame.Rect(self._location[0], self._location[1], 35, 35)

    def get_location(self):
        return self._location

    def update(self):
        if pygame.time.get_ticks() % 3 == 0:
            self._index += 1
            if self._index >= len(self._standing_still_animation_frames):
                self._index = 0
            self.img = self._standing_still_animation_frames[self._index]
            
