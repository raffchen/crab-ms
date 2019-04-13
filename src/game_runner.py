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

        self.size_tuple = (700, 450)

        self.game = game_state
        self.background = Player(str(Path("./data/images/grid.jpg")), (1000, 1000))
        self.player = Player(str(Path("./data/images/crab.png")), (80, 80), (300, 200))

    def run(self):
        """initializes, executes, and quits the pygame"""
        pygame.init()

        pygame.display.init()

        self._resize_screen(self.size_tuple)
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
            elif event.type == pygame.VIDEORESIZE:
                self._resize_screen(event.size)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self._move("w")
        if keys[pygame.K_a]:
            self._move("a")
        if keys[pygame.K_s]:
            self._move("s")
        if keys[pygame.K_d]:
            self._move("d")

    def _move(self, key):
        moves = {"w": (0, 4), "a": (4, 0), "s": (0, -4), "d": (-4, 0)}

        self.screen.fill(pygame.Color(255, 255, 255))
        self.background.rect = self.background.rect.move(*moves[key])
        self.screen.blit(self.background.img, self.background.rect)
        self.screen.blit(self.player.img, self.player.rect)
        pygame.display.flip()

    def _resize_screen(self, size: (int, int)) -> None:
      """changes the size of the game screen"""
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)


if __name__ == '__main__':
    game = Game()
    view = GameView(game)
    view.run()
