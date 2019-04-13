import pygame
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
        self.symptoms = {
            "loss-of-balance": {"status": False, "timer": 0},
            "fatigue": {"status": False, "timer": 0},
            "vision": {"status": False, "timer": 0},
            "weakness": {"status": False, "timer": 0}
        }

    def update_location(self, move):
        self._location = (self._location[0]+move[0], self._location[1]+move[1])

    def get_location(self):
        return self._location
        

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
    def __init__(self):
        self.running = True
        self.screen = pygame.display.set_mode((700, 450))
        self.background = Player(str(Path("./data/images/beach.jpg")), (1156, 1300))
        self.player = Crab(str(Path("./data/images/crab.png")), (72, 44), (300, 200))
        # TEST
        self.player.symptoms['loss-of-balance']['status'] = True
        # END TEST
        self.end_screen = Player(str(Path("./data/images/endgame.png")), (700, 450))
        self.gulls = [Seagull(str(Path("./data/images/seagull.png")), (72, 44), self.background),
                      Seagull(str(Path("./data/images/seagull.png")), (72, 44), self.background),
                      Seagull(str(Path("./data/images/seagull.png")), (72, 44), self.background)]
        self.h_bars = [Player(str(Path("./data/images/health0.png")), (216, 134), (237, -10)),
                       Player(str(Path("./data/images/health1.png")), (216, 134), (237, -10)),
                       Player(str(Path("./data/images/health2.png")), (216, 134), (237, -10)),
                       Player(str(Path("./data/images/health3.png")), (216, 134), (237, -10)),
                       Player(str(Path("./data/images/health4.png")), (216, 134), (237, -10)),
                       Player(str(Path("./data/images/health5.png")), (216, 134), (237, -10)),
                       Player(str(Path("./data/images/health6.png")), (216, 134), (237, -10)),
                       Player(str(Path("./data/images/health7.png")), (216, 134), (237, -10)),
                       Player(str(Path("./data/images/health8.png")), (216, 134), (237, -10))]

        self.moves = {"up": (0, 4), "left": (4, 0), "down": (0, -4), "right": (-4, 0)}

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
            for gull in self.gulls:
                gull.move()
                self._display_board()
        pygame.quit()  

    def _display_board(self):
        """displays the board when it changes"""
        self.screen.fill(pygame.Color(255, 255, 255))
        #self.screen.blit(self.background.img, self.background.rect)
        map_generator.loadLevel(self.screen, 'level1.txt')
        for gull in self.gulls:
            self.screen.blit(gull.img, gull.rect)
        if self.player.health > 0:
            self.screen.blit(self.player.img, self.player.rect)
        else:
            self.screen.blit(self.end_screen.img, self.end_screen.rect)
        self.screen.blit(self.h_bars[int(self.player.health/10)].img, self.h_bars[int(self.player.health/10)].rect)
        pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
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

    def _move(self, key):
        for symptom, flag in self.player.symptoms.items():
            if flag["status"]:
                if symptom == 'loss-of-balance':
                    if flag["timer"] == 0:
                        self._moves = self.moves.copy()
                        self.moves = dict(zip(sorted(self.moves.keys(), key=lambda x: random()),
                                          sorted(self.moves.values(), key=lambda x: random())))
                        self.player.symptoms[symptom]["timer"] += 1
                    elif flag["timer"] == 60:
                        self.moves = self._moves
                        del self._moves
                        self.player.symptoms[symptom]["status"] = False
                        self.player.symptoms[symptom]["timer"] = 0
                        print(flag["timer"])
                    else:
                        self.player.symptoms[symptom]["timer"] += 1
                        print(flag["timer"])
                
        if ((key == "up" and not self.player.rect.top <= self.background.rect.top)
                or (key == "left" and not self.player.rect.left <= self.background.rect.left)
                or (key == "down" and not self.player.rect.bottom >= self.background.rect.bottom)
                or (key == "right" and not self.player.rect.right >= self.background.rect.right)):
            self.background.rect = self.background.rect.move(*self.moves[key])
            if self.moves[key][0] != 0:
                map_generator.default_x_coord += self.moves[key][0]
            elif self.moves[key][1] != 0:
                map_generator.default_y_coord += self.moves[key][1]

        if random() > 0.9:
            self.player.health -= 1


if __name__ == '__main__':
    view = GameView()
    view.run()
