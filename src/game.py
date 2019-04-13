from random import randrange

class Game:
    def __init__(self):
        self._running = True
        self._board = []
        self._init_board()

    def _init_board(self):
        num_col = 6
        num_row = 6
        for row in range(num_row):
            col_lst = []
            for col in range(num_col+2):
                if(row == 0 and col == 1):
                    col_lst.append('c')
                elif(col in [0, num_col+1]):
                    col_lst.append('|')
                else:
                    col_lst.append(' ')
            self._board.append(col_lst)
    
    def print_board(self):
        for row in self._board:
            for col in row:
                print(col, end = '')
            print()

if __name__ == '__main__':
    game = Game()
    game.print_board()
