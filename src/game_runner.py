import pygame
from game import Game
from pathlib import Path


class Player:
    def __init__(self, image: str, size: tuple, location: tuple = (0, 0)):
        self.img = pygame.transform.scale(pygame.image.load(image), size)
        self.rect = self.img.get_rect()
        self.rect = self.rect.move(*location)


class GameView:
    def __init__(self, game_state):
        self.game = game_state
        self.screen = pygame.display.set_mode((700, 450))
        self.background = Player(str(Path("./data/images/grid.jpg")), (1000, 1000))
        self.player = Player(str(Path("./data/images/crab.png")), (60, 60), (300, 200))

    def run(self):
        """initializes, executes, and quits the pygame"""
        pygame.init()
        pygame.display.init()

        clock = pygame.time.Clock()

        while self.game.running:
            clock.tick(60)

            self._handle_events()
            self._display_board()

        pygame.quit()

    def _display_board(self):
        """displays the board when it changes"""
        self.screen.fill(pygame.Color(255, 255, 255))
        self.screen.blit(self.background.img, self.background.rect)
        self.screen.blit(self.player.img, self.player.rect)
        pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self._move("up")
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self._move("left")
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self._move("down")
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self._move("right")

    def _move(self, key):
        moves = {"up": (0, 4), "left": (4, 0), "down": (0, -4), "right": (-4, 0)}

        self.screen.fill(pygame.Color(255, 255, 255))
        if ((key == "up" and not self.player.rect.top <= self.background.rect.top)
                or (key == "left" and not self.player.rect.left <= self.background.rect.left)
                or (key == "down" and not self.player.rect.bottom >= self.background.rect.bottom)
                or (key == "right" and not self.player.rect.right >= self.background.rect.right)):
            self.background.rect = self.background.rect.move(*moves[key])
        self.screen.blit(self.background.img, self.background.rect)
        self.screen.blit(self.player.img, self.player.rect)
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    view = GameView(game)
    view.run()
