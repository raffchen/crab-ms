import pygame
from pathlib import Path
from random import random, choice, choices
import map_generator
from crab import Crab
from player import Player
from seagull import Seagull
from pebble import Pebble


class GameView:
    def __init__(self):
        self.running = True
        self.screen = pygame.display.set_mode((700, 450))
        self.background = Player(str(Path("./data/images/beach.jpg")), (1156, 1300))
        self.player = Crab(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still0.png")), (35, 35), (300, 200))

        self.pebbles = []
        self.stage = 1
        self.months = [Player(str(Path("./data/images/month1.png")), (216, 134), (500, -12)),
                       Player(str(Path("./data/images/month2.png")), (216, 134), (500, -12)),
                       Player(str(Path("./data/images/month3.png")), (216, 134), (500, -12)),]
        self.end_screen = Player(str(Path("./data/images/endgame.png")), (700, 450))
        '''self.gulls = [Seagull(str(Path("./data/images/seagull.png")), (72, 44), self.background),
                      Seagull(str(Path("./data/images/seagull.png")), (72, 44), self.background),
                      Seagull(str(Path("./data/images/seagull.png")), (72, 44), self.background)]'''
        self.h_bars = [Player(str(Path("./data/images/health0.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health1.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health2.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health3.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health4.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health5.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health6.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health7.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health8.png")), (216, 134), (10, -30))]

        self.moves = {"up": (0, self.player.speed), "left": (self.player.speed, 0),
                      "down": (0, -self.player.speed), "right": (-self.player.speed, 0)}
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.load("./data/music/Intro.mp3")
        pygame.mixer.music.play() 

    def run(self):
        """initializes, executes, and quits the pygame"""
        pygame.init()
        pygame.display.init()

        clock = pygame.time.Clock()

        while self.running:
            for _ in range(4):
                clock.tick(60)
                self._handle_events()
                self._display_board()
        pygame.quit()  

    def _display_board(self):
        """displays the board when it changes"""
        self.screen.fill(pygame.Color(0, 0, 0))
        # self.screen.blit(self.background.img, self.background.rect)
        map_generator.loadLevel(self.screen, 'level1.txt')
        # for gull in self.gulls:
        #    self.screen.blit(gull.img, gull.rect)
        
        for pebble in self.pebbles:
            self.screen.blit(Pebble.img, pebble.location)
            pebble.update()
        if self.player.health > 0:
            self.player.update()
            self.screen.blit(self.player.img, self.player.rect)
            
        else:
            self.screen.blit(self.end_screen.img, self.end_screen.rect)
        self.screen.blit(self.months[self.stage-1].img, self.months[self.stage-1].rect)
        self.screen.blit(self.h_bars[int(self.player.health/10)].img, self.h_bars[int(self.player.health/10)].rect)
        pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
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
                self.__init__()
                pygame.mixer.music.load("./data/music/Crab.mp3")
                pygame.mixer.music.play() 
                map_generator.default_x_coord = map_generator.DEFAULT_STARTING_X_COORD
                map_generator.default_y_coord = map_generator.DEFAULT_STARTING_Y_COORD
    
    def shoot(self, mouse_click):
        vector_direction = [0, 0]
        if self.player.get_location()[0] - mouse_click[0] < 0:
            vector_direction[0] = 1
        elif self.player.get_location()[0] - mouse_click[0] > 0:
            vector_direction[0] = -1
        if self.player.get_location()[1] - mouse_click[1] < 0:
            vector_direction[1] = 1
        elif self.player.get_location()[1] - mouse_click[1] > 0:
            vector_direction[1] = -1
        vector_direction = tuple(vector_direction)
        if vector_direction != (0, 0):
            self.pebbles.append(Pebble(vector_direction, self.player.get_location()))

    def _handle_symptoms(self):
        if random() > 0.99:
            random_symptom = choice(["loss-of-balance", "fatigue"])
            print(f"selected {random_symptom}")
            if not self.player.symptoms[random_symptom]["status"]:
                if random() > .85:
                    self.player.symptoms[random_symptom]["status"] = True
                    print(f"{random_symptom} now active")

    def _move(self, key):
        self._handle_symptoms()
        for symptom, flag in self.player.symptoms.items():
            if symptom == 'loss-of-balance' and flag["status"]:
                if flag["timer"] == 0:
                    self._moves = self.moves.copy()
                    self.moves = dict(zip(sorted(self.moves.keys(), key=lambda x: random()),
                                      sorted(self.moves.values(), key=lambda x: random())))
                    self.player.symptoms[symptom]["timer"] += 1
                elif flag["timer"] == 150:
                    self.moves = self._moves
                    del self._moves
                    self.player.symptoms[symptom]["status"] = False
                    self.player.symptoms[symptom]["timer"] = 0
                else:
                    self.player.symptoms[symptom]["timer"] += 1

            elif symptom == 'fatigue' and flag["status"]:
                if flag["timer"] == 0:
                    self.player.speed = choices([0, 1, 2, 3], [5, 10, 10, 25])[0]/4
                    self.moves = {k: tuple(map(lambda x: int(x * self.player.speed), v)) for k, v in self.moves.items()}
                    self.player.symptoms[symptom]["timer"] += 1
                elif flag["timer"] == 150:
                    self.player.speed = 4
                    self.player.symptoms[symptom]["status"] = False
                    self.player.symptoms[symptom]["timer"] = 0
                    try:
                        self.moves = {k: tuple(map(lambda x: int(x * self.player.speed/x), v))
                                      for k, v in self.moves.items()}
                    except ZeroDivisionError:
                        self.moves = {"up": (0, self.player.speed), "left": (self.player.speed, 0),
                                      "down": (0, -self.player.speed), "right": (-self.player.speed, 0)}
                else:
                    self.player.symptoms[symptom]["timer"] += 1
                
        if ((key == "up" and not self.player.rect.top <= self.background.rect.top)
                or (key == "left" and not self.player.rect.left <= self.background.rect.left)
                or (key == "down" and not self.player.rect.bottom >= self.background.rect.bottom)
                or (key == "right" and not self.player.rect.right >= self.background.rect.right)):
            self.background.rect = self.background.rect.move(*self.moves[key])
            if self.moves[key][0] != 0:
                map_generator.default_x_coord += self.moves[key][0]
            elif self.moves[key][1] != 0:
                map_generator.default_y_coord += self.moves[key][1]

        for pebble in self.pebbles:
            if self.moves[key][0] != 0:
                pebble.location = (pebble.location[0] + self.moves[key][0], pebble.location[1])
            elif self.moves[key][1] != 1:
                pebble.location = (pebble.location[0], pebble.location[1] + self.moves[key][1])


if __name__ == '__main__':
    view = GameView()
    view.run()
