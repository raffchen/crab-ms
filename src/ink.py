import pygame

class Ink:
    
    img = pygame.transform.scale(pygame.image.load("./data/images/squid_images/ink.png"), (20, 20))
    speed = 2
    
    def __init__(self, vector_direction, location):
        self.vector_direction = pygame.math.Vector2(vector_direction).normalize()
        self.location = location
        self.rect = pygame.Rect(self.location[0], self.location[1], 15, 15)
        
    def update(self):
        self.location = (self.location[0] + self.vector_direction[0]*Ink.speed,
                         self.location[1] + self.vector_direction[1]*Ink.speed)
        self.rect = pygame.Rect(self.location[0], self.location[1], 15, 15)
