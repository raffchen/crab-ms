import pygame
from pathlib import Path
from random import random, choice, choices, randint
import map_generator
from crab import Crab
from player import Player
from seagull import Seagull
from pebble import Pebble
from jellyfish import Jellyfish
from littlefish import LittleFish
from stalker_fish import Stalker
from squid import Squid
from ink import Ink

IMAGE_WIDTH = map_generator.IMAGE_WIDTH
IMAGE_HEIGHT = map_generator.IMAGE_HEIGHT
ROW_LENGTH = map_generator.ABSOLUTE_BORDER_SIZE

SPAWN_RATE = 0.01
INVERSE_SPEED = 10

LAST_MOUSE_POSITION = (0,0)


class GameView:
    def __init__(self):
        self.running = True
        self.screen = pygame.display.set_mode((IMAGE_WIDTH*ROW_LENGTH, IMAGE_HEIGHT*ROW_LENGTH))
        self.background = Player(str(Path("./data/images/beach.jpg")), (IMAGE_WIDTH*ROW_LENGTH, IMAGE_HEIGHT*ROW_LENGTH))
        self.player = Crab(str(Path("./data/images/crab_images/Crab Standing Animation/crab_standing_still0.png")), (35, 35), (300, 200))

        self.pebbles = [ ]
        self.jellyfish = [ ]
        self.squids = [ ]
        self.stalkers = [ ]
        self.inks = [ ]
        self.littlefish = []
        self.vignette = None

        self.stage = 1
        # self.months = [Player(str(Path("./data/images/month1.png")), (216, 134), (500, -12)),
        #                Player(str(Path("./data/images/month2.png")), (216, 134), (500, -12)),
        #                Player(str(Path("./data/images/month3.png")), (216, 134), (500, -12)),]
        self.end_screen = Player(str(Path("./data/images/endgame.png")), (700, 450))
        # self.gulls = [Seagull(str(Path("./data/images/seagull.png")), (72, 44), self.background),
        #               Seagull(str(Path("./data/images/seagull.png")), (72, 44), self.background),
        #               Seagull(str(Path("./data/images/seagull.png")), (72, 44), self.background)]
        self.h_bars = [Player(str(Path("./data/images/health0.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health1.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health2.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health3.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health4.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health5.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health6.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health7.png")), (216, 134), (10, -30)),
                       Player(str(Path("./data/images/health8.png")), (216, 134), (10, -30))]

        self.moves = {"up": (0, -self.player.speed), "left": (-self.player.speed, 0),
                      "down": (0, self.player.speed), "right": (self.player.speed, 0)}
        self._moves = self.moves.copy()

        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.load("./data/music/Intro.mp3")
        pygame.mixer.music.play(-1) 

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
        if self.player.health < 0:
            return
        
        
        for pebble in self.pebbles:
            self.screen.blit(Pebble.img, pebble.location)
            pebble.update()
            for jelly in self.jellyfish:
                if pebble.rect.colliderect(jelly.rect):
                    jelly.health -= 1
                    if jelly.health == 0:
                        self.jellyfish.remove(jelly)
                    if pebble in self.pebbles:
                        self.pebbles.remove(pebble)
            for stalker in self.stalkers:
                if pebble.rect.colliderect(stalker.rect):
                    stalker.health -= 1
                    if stalker.health == 0:
                        self.stalkers.remove(stalker)
                    if pebble in self.pebbles:
                        self.pebbles.remove(pebble)
                        
            for squid in self.squids:
                if pebble.rect.colliderect(squid.rect):
                    squid.health -= 1
                    if squid.health == 0:
                        self.squids.remove(squid)
                    if pebble in self.pebbles:
                        self.pebbles.remove(pebble)
            
        l_lst = []
        for fish in self.littlefish.copy():
            self.screen.blit(fish.image, fish._location)
            var = fish.update()
            if(var):
                l_lst.append(var)

        self.littlefish = l_lst
            
        for jelly in self.jellyfish:
            self.screen.blit(jelly.image, jelly._location)
            jelly.update()
            if jelly.rect.colliderect(self.player.rect):
                self.player.health -= 10
                self.jellyfish.remove(jelly)
            
        for stalker in self.stalkers:
            self.screen.blit(stalker.image, stalker._location)
            stalker.update((self.player.get_location()[0]-stalker._location[0], self.player.get_location()[1]-stalker._location[1]))
            if stalker.rect.colliderect(self.player.rect):
                self.player.health -= 10
                self.stalkers.remove(stalker)
                
        for squid in self.squids:
            self.screen.blit(squid.image, squid._location)
            squid.update((self.player.get_location()[0]-squid._location[0], self.player.get_location()[1]-squid._location[1]))
            if pygame.time.get_ticks()%50 == 0:
                self.squid_shoot(squid)
            if squid.rect.colliderect(self.player.rect):
                self.player.health -= 10
                self.squids.remove(squid)
                
        for ink in self.inks:
            self.screen.blit(Ink.img, ink.location)
            ink.update()
            if ink.rect.colliderect(self.player.rect):
                self.player.health -= 10
                self.inks.remove(ink)
            
        if self.player.health > 0:
            self.player.update()
            self.screen.blit(self.player.img, self.player.rect)
            
        else:
            self.screen.blit(self.end_screen.img, self.end_screen.rect)
        if self.vignette is not None:
            self.screen.blit(self.vignette, (0, 0))
        # self.screen.blit(self.months[self.stage-1].img, self.months[self.stage-1].rect)
        self.screen.blit(self.h_bars[int(self.player.health/10)].img, self.h_bars[int(self.player.health/10)].rect)
        pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        global INVERSE_SPEED, SPAWN_RATE
            
        if pygame.time.get_ticks()%1000 == 0:
            if INVERSE_SPEED > 2: INVERSE_SPEED -= 1
            SPAWN_RATE += 0.001

        if pygame.time.get_ticks()%INVERSE_SPEED == 0:
            self.player_shoot(pygame.mouse.get_pos())

        mouse_buttons = pygame.mouse.get_pressed()
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
            if mouse_buttons[0]:
                if pygame.time.get_ticks() % INVERSE_SPEED in (0, 1):
                    self.player_shoot(pygame.mouse.get_pos())
        else:
            if keys[pygame.K_r]:
                self.__init__()
                pygame.mixer.music.load("./data/music/Crab.mp3")
                pygame.mixer.music.play() 
                map_generator.default_x_coord = map_generator.DEFAULT_STARTING_X_COORD
                map_generator.default_y_coord = map_generator.DEFAULT_STARTING_Y_COORD
                
        self.spawn_jellyfish()
        self.spawn_stalker()
        self.spawn_squid()
        self.spawn_littlefish()
        
    def spawn_jellyfish(self):
        if random() <= SPAWN_RATE:
            self.jellyfish.append(Jellyfish((40, 40), (int(random()*IMAGE_WIDTH*ROW_LENGTH), int(random()*IMAGE_HEIGHT*ROW_LENGTH))))
    
    def spawn_littlefish(self):
        if random() <= SPAWN_RATE:
            self.littlefish.append(LittleFish(self.player,(int(random()*IMAGE_WIDTH*ROW_LENGTH), int(random()*IMAGE_HEIGHT*ROW_LENGTH))))
            
            
    def spawn_stalker(self):
        if random() <= SPAWN_RATE:
            self.stalkers.append(Stalker((40, 40), (int(random()*IMAGE_WIDTH*ROW_LENGTH), int(random()*IMAGE_HEIGHT*ROW_LENGTH))))
    
    def spawn_squid(self):
        if random() <= SPAWN_RATE:
            self.squids.append(Squid((40,40), (int(random()*IMAGE_WIDTH*ROW_LENGTH), int(random()*IMAGE_HEIGHT*ROW_LENGTH))))
    
    def player_shoot(self, mouse_click):
        vector_direction = (mouse_click[0]-self.player.get_location()[0],mouse_click[1]-self.player.get_location()[1], )
        if vector_direction != (0, 0):
            self.pebbles.append(Pebble(vector_direction, self.player.get_location()))
            
    def squid_shoot(self, squid):
        vector_direction = pygame.math.Vector2(squid.vector_direction).normalize()
        if vector_direction != (0,0):
            self.inks.append(Ink(vector_direction, squid._location))
        

    def _handle_symptoms(self):
        if random() > 0.99:
            random_symptom = choice(["loss-of-balance", "fatigue", "pain", "vision"])
            print(f"selected {random_symptom}")
            if not self.player.symptoms[random_symptom]["status"]:
                if random() > .87:
                    self.player.symptoms[random_symptom]["status"] = True
                    print(f"{random_symptom} now active")

    def _move(self, key):
        self._handle_symptoms()
        symptom_cooldown = randint(100, 200)
        for symptom, flag in self.player.symptoms.items():
            if symptom == 'loss-of-balance' and flag["status"]:
                if flag["timer"] == 0:
                    self.moves = dict(zip(sorted(self.moves.keys(), key=lambda x: random()),
                                      sorted(self.moves.values(), key=lambda x: random())))
                    self.player.symptoms[symptom]["timer"] += 1
                elif flag["timer"] > symptom_cooldown:
                    self.moves = self._moves
                    self.player.symptoms[symptom]["status"] = False
                    self.player.symptoms[symptom]["timer"] = 0
                else:
                    self.player.symptoms[symptom]["timer"] += 1

            elif symptom == 'fatigue' and flag["status"]:
                if flag["timer"] == 0:
                    self.player.speed = choices([0, 1, 2, 3], [5, 10, 10, 25])[0]/4
                    self.moves = {k: tuple(map(lambda x: int(x * self.player.speed), v)) for k, v in self.moves.items()}
                    self.player.symptoms[symptom]["timer"] += 1
                elif flag["timer"] > symptom_cooldown:
                    self.player.speed = 4
                    self.player.symptoms[symptom]["status"] = False
                    self.player.symptoms[symptom]["timer"] = 0
                    try:
                        self.moves = {k: tuple(map(lambda x: int(x * self.player.speed/x), v))
                                      for k, v in self.moves.items()}
                    except ZeroDivisionError:
                        self.moves = self._moves.copy()
                else:
                    self.player.symptoms[symptom]["timer"] += 1

            elif symptom == 'pain' and flag["status"]:
                damage = choices([10, 5, 2, 1], [2, 8, 20, 20])[0]
                self.player.health -= damage
                print(f"received {damage} damage")
                print(f"{self.player.health} health remaining")
                self.player.symptoms[symptom]["status"] = False

            elif symptom == 'vision' and flag["status"]:
                if flag["timer"] == 0:
                    self.vignette = pygame.image.load(str(Path('./data/images/vignette.png')))
                    self.player.symptoms[symptom]["timer"] += 1
                elif flag["timer"] > symptom_cooldown:
                    self.vignette = None
                    pygame.display.flip()
                    self.player.symptoms[symptom]["timer"] = 0
                    self.player.symptoms[symptom]["status"] = False
                else:
                    self.player.symptoms[symptom]["timer"] += 1
                
        proposed_move = self.player.rect.move(*self.moves[key])
        if (not proposed_move.right > self.background.rect.right and
                not proposed_move.left < self.background.rect.left and
                not proposed_move.top < self.background.rect.top and
                not proposed_move.bottom > self.background.rect.bottom):
            self.player.update_location(self.moves[key])


if __name__ == '__main__':
    view = GameView()
    view.run()
