import pygame

class GameView:
    def __init__(self):
        self.size_tuple = (400,600)

    def run(self):
        '''initializes, executes, and quits the pygame'''
        pygame.init()
        self._resize_screen((400,600))
        self.clock = pygame.time.Clock()

    def _display_board(self):
        '''displays the board when it changes'''
        self.screen.fill(pygame.Color(255,255,255))
        self._build_board()
        pygame.display.flip()
    def _resize_screen(self, size: (int,int)) -> None:
        '''changes the size of the game screen'''
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE) 

if __name__ == '__main__':
    view = GameView()
    view.run()

