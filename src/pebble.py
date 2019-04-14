import pygame


class Pebble:
    
    img = pygame.transform.scale(pygame.image.load("./data/images/pebble.png"), (20, 20))
    speed = 15
    
    def __init__(self, vector_direction, location):
        print(vector_direction)
        self.vector_direction = pygame.math.Vector2(vector_direction).normalize()
        print(self.vector_direction)
        self.location = location
        
    def update(self):
        self.location = (self.location[0] + self.vector_direction[0]*Pebble.speed,
                         self.location[1] + self.vector_direction[1]*Pebble.speed)
