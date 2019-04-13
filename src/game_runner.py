import pygame
from game import Game


class GameView:
    def __init__(self, game_state):
        self.size_tuple = (700, 450)
        self.game = game_state
        self.counter = 0

    def run(self):
        """initializes, executes, and quits the pygame"""
        pygame.init()

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
        pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.VIDEORESIZE:
                self._resize_screen(event.size)

    def _resize_screen(self, size: (int,int)) -> None:
        """changes the size of the game screen"""
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE) 


if __name__ == '__main__':
    game = Game()
    view = GameView(game)
    view.run()

