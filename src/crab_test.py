import unittest
from game import Game

class CrabTest(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def _test_that_board_initialized_correctly(self):
        self.game.print_board()
        print(self.game._board())

if __name__ == '__main__':
    unittest.main()
