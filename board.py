import numpy as np
from copy import deepcopy

class Board:
    def __init__(self):
        self._board = np.array([i for i in range(9)])

    @property
    def board(self):
        return self._board

    @property
    def blank(self):
        return self._blank()

    @property
    def solved(self):
        return np.array_equal(self.board, np.array([i for i in range(9)]))

    def valid_board(self):
        inversions = 0
        for i in range(8):
            for j in range(i, 9): 
                if self.board[i] and self.board[j] and self.board[i] > self.board[j]:
                        inversions += 1

        return (inversions % 2 == 0 and inversions > 0)
    
    def valid_move(self, end):
        start = self.blank
        if start == 0 and end < 0 :
            return False

        if end / 3 > 2:
            return False

        if start // 3 != end // 3:
            if (start % 3 > end % 3) or (start % 3 < end % 3):
                return False

            return True
        
        return True

    def swap_tile(self, pos):
        board_obj = deepcopy(self)

        board = board_obj.board
        blank = self.blank

        temp = board[pos]
        board[blank] = temp
        board[pos] = 0

        return board_obj

    def neighbors(self):
        neighbors = set()
        blank = self.blank

        possible_moves = [-1, 1, -3, 3]
        for move in possible_moves:
            to_swap = blank + move
            if self.valid_move(to_swap):
                new_board = self.swap_tile(to_swap)
                if new_board not in neighbors:
                    neighbors.add(new_board)

        return neighbors

    def _blank(self):
        return np.argwhere(self._board == 0)[0]

    def __eq__(self, value):
        return np.array_equal(self._board, value.board)

    def __repr__(self):
        return str(self.board.reshape(3, 3))

    def __hash__(self):
        return hash(str(self.board))


if __name__ == '__main__':
    b = Board()
    print(b)

    n = b.neighbors()
    print(n)