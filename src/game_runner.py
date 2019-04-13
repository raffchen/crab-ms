import pygame
from game import Game
from pathlib import Path
from random import random, choice, shuffle
import map_generator


class Player:
    def __init__(self, image: str, size: tuple, location: tuple = (0, 0)):
        self.img = pygame.transform.scale(pygame.image.load(image), size)
        self.rect = self.img.get_rect()
        self.rect = self.rect.move(location)


class Crab(Player):
    def __init__(self, image: str, size: tuple, location: tuple = (0, 0)):
        Player.__init__(self, image, size, location)
        self.health = 80
        self._location = location

        self._index = 0
        
        self._standing_still_animation_frames = [
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still0.png"))), (60, 60)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still1.png"))), (60, 60)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still2.png"))), (60, 60)),
            pygame.transform.scale(pygame.image.load(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still3.png"))), (60, 60)),
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
            
        
class Pebble():
    
    img = pygame.transform.scale(pygame.image.load("./data/images/pebble.png"), (20, 20))
    speed = 5
    
    def __init__(self, vector_direction, location):
        self.vector_direction = vector_direction
        self.location = location
        
    def update(self):
        self.location = (self.location[0] + self.vector_direction[0]*Pebble.speed, self.location[1] + self.vector_direction[1]*Pebble.speed)

        

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
        if ((self.direction == "up" and not self.rect.top < self.background.rect.top+350)
            or (self.direction == "left" and not self.rect.left < self.background.rect.left+250)
            or (self.direction == "down" and not self.rect.bottom > self.background.rect.bottom-350)
            or (self.direction == "right" and not self.rect.right > self.background.rect.right-250)
            or (self.direction == "left-up" and not (self.rect.top < self.background.rect.top+350 or
                                                     self.rect.left < self.background.rect.left+250))
            or (self.direction == "right-up" and not (self.rect.top < self.background.rect.top+350 or
                                                      self.rect.right > self.background.rect.right-250))
            or (self.direction == "left-down" and not (self.rect.bottom > self.background.rect.bottom-350 or
                                                       self.rect.left < self.background.rect.left+250))
            or (self.direction == "right-down" and not (self.rect.bottom > self.background.rect.bottom-350 or
                                                        self.rect.right > self.background.rect.right-250))):
            self.rect = self.rect.move(*moves[self.direction])
        else:
            self.direction = choice(["up", "left", "down", "right", "left-up", "right-up", "left-down", "right-down"])


class GameView:
    def __init__(self, game_state):
        self.game = game_state
        self.screen = pygame.display.set_mode((700, 450))
        self.background = Player(str(Path("./data/images/beach.jpg")), (int(0.5*map_generator.ABSOLUTE_BORDER_SIZE*map_generator.IMAGE_WIDTH), int(0.5*map_generator.ABSOLUTE_BORDER_SIZE*map_generator.IMAGE_HEIGHT)))
        self.player = Crab(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still0.png")), (60, 60), (300, 200))
        self.end_screen = Player(str(Path("./data/images/endgame.png")), (700, 450))
        
        self.pebbles = []
        #self.gulls = [Seagull(str(Path("./data/images/seagull.png")), (72, 44), self.background),
        #              Seagull(str(Path("./data/images/seagull.png")), (72, 44), self.background),
        #              Seagull(str(Path("./data/images/seagull.png")), (72, 44), self.background)]

        self.h_bars = [Player(str(Path("./data/images/health0.png")), (216, 134), (237,-10)),\
                       Player(str(Path("./data/images/health1.png")), (216, 134), (237,-10)),\
                       Player(str(Path("./data/images/health2.png")), (216, 134), (237,-10)),\
                       Player(str(Path("./data/images/health3.png")), (216, 134), (237,-10)),\
                       Player(str(Path("./data/images/health4.png")), (216, 134), (237,-10)),\
                       Player(str(Path("./data/images/health5.png")), (216, 134), (237,-10)),\
                       Player(str(Path("./data/images/health6.png")), (216, 134), (237,-10)),\
                       Player(str(Path("./data/images/health7.png")), (216, 134), (237,-10)),\
                       Player(str(Path("./data/images/health8.png")), (216, 134), (237,-10))]
        

    def run(self):
        """initializes, executes, and quits the pygame"""
        pygame.init()
        pygame.display.init()

        clock = pygame.time.Clock()

        while self.game.running:
            for _ in range(4):
                clock.tick(60)
                self._handle_events()
                self._display_board()
            #for gull in self.gulls:
            #    gull.move()
            #    self._display_board()
        pygame.quit()  

    def _display_board(self):
        """displays the board when it changes"""
        self.screen.fill(pygame.Color(255, 255, 255))
        #self.screen.blit(self.background.img, self.background.rect)
        map_generator.loadLevel(self.screen, 'level1.txt')
        #for gull in self.gulls:
        #    self.screen.blit(gull.img, gull.rect)
        
        for pebble in self.pebbles:
            self.screen.blit(Pebble.img, pebble.location)
            pebble.update()
        if self.player.health > 0:
            self.player.update()
            self.screen.blit(self.player.img, self.player.rect)
            
        else:
            self.screen.blit(self.end_screen.img, self.end_screen.rect)
        self.screen.blit(self.h_bars[int(self.player.health/10)].img, self.h_bars[int(self.player.health/10)].rect)
        pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.shoot(pygame.mouse.get_pos())
        keys = pygame.key.get_pressed()
        if self.player.health > 0:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self._move("up")
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self._move("left")
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self._move("down")
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self._move("right")
        else:
            if keys[pygame.K_r]:
                self.__init__(Game())
                map_generator.default_x_coord = map_generator.DEFAULT_STARTING_X_COORD
                map_generator.default_y_coord = map_generator.DEFAULT_STARTING_Y_COORD
    
    def shoot(self, mouse_click):
        vector_direction = [0,0]
        if self.player.get_location()[0] - mouse_click[0] < 0:
            vector_direction[0] = 1
        elif self.player.get_location()[0] - mouse_click[0] > 0:
            vector_direction[0] = -1
        if self.player.get_location()[1] - mouse_click[1] < 0:
            vector_direction[1] = 1
        elif self.player.get_location()[1] - mouse_click[1] > 0:
            vector_direction[1] = -1
        vector_direction = tuple(vector_direction)
        if vector_direction != (0,0):
            self.pebbles.append(Pebble(vector_direction, self.player.get_location()))

    def _move(self, key):
        moves = {"up": (0, 4), "left": (4, 0), "down": (0, -4), "right": (-4, 0)}
        
        #if random() < 0.20:
         #    key = choice(["up", "left", "right", "down"])
                
        if ((key == "up" and not self.player.rect.top <= self.background.rect.top)
            or (key == "left" and not self.player.rect.left <= self.background.rect.left)
            or (key == "down" and not self.player.rect.bottom >= self.background.rect.bottom)
            or (key == "right" and not self.player.rect.right >= self.background.rect.right)):
            self.background.rect = self.background.rect.move(*moves[key])
            if moves[key][0] != 0:
                map_generator.default_x_coord += moves[key][0]
            elif moves[key][1] != 1:
                map_generator.default_y_coord += moves[key][1]
        
        for pebble in self.pebbles:
            if moves[key][0] != 0:
                pebble.location = (pebble.location[0] + moves[key][0], pebble.location[1])
            elif moves[key][1] != 1:
                pebble.location = (pebble.location[0], pebble.location[1] + moves[key][1])
        '''else:
             self._character_move(key)'''


    def _character_move(self, key):
         moves = {"up": (0, 4), "left": (4, 0), "down": (0, -4), "right": (-4, 0)}
         if key == 'up':
             key = 'down'
         elif key == 'down':
             key = 'up'
         elif key == 'left':
             key = 'right'
         elif key == 'right':
             key = 'left'
         if ((key == "up" and self.player.rect.top < self.background.rect.top)
                 or (key == "left" and self.player.rect.left > self.background.rect.left)
                 or (key == "down" and self.player.rect.bottom > self.background.rect.bottom)
                 or (key == "right" and self.player.rect.right < self.background.rect.right+72)):
             self.player.rect = self.player.rect.move(*moves[key])
             self.player.update_location(moves[key])
             

if __name__ == '__main__':
    game = Game()
    view = GameView(game)
    view.run()
