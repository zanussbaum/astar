import numpy as np
from tqdm import tqdm
from copy import deepcopy

def generate_boards(depth, num, board=None):
    if not board:
        goal = Board()
    unique = set()
    already_seen = set()
    possible = [goal]
    prog = tqdm(total=100)
    
    current_depth = 1
    while len(possible):
        next = []
        for b in possible:
            neighbors = b.neighbors()
            if current_depth == depth:
                unique.update([n for n in neighbors if n.valid_board() 
                                and not n.solved and n not in already_seen])
                prog.update(len(neighbors))
                if len(unique) >= num:
                    return unique
            else:
                not_seen = set(neighbors) - already_seen
                next.extend(not_seen)
                already_seen.update(not_seen)
        current_depth += 1
        possible = next
    
    return unique
class Board:
    def __init__(self, goal=None):
        if goal is None:
            self.goal = np.array([i for i in range(9)])
        self._board = np.array([i for i in range(9)])

    @property
    def board(self):
        return self._board

    @property
    def blank(self):
        return self._blank()

    @property
    def solved(self):
        return np.array_equal(self.board, self.goal)

    def valid_board(self):
        inversions = 0
        for i in range(8):
            for j in range(i, 9): 
                if self.board[i] and self.board[j] and self.board[i] > self.board[j]:
                        inversions += 1

        return (inversions % 2 == 0 and inversions > 0)

    def heuristic(self, value):
        if value == 0:
            # misplaced tile heuristic
            cost = sum([1 for i in range(9) if i != self.board[i] and self.board[i] != 0])
        else:
            cost = sum([self._individual_distance(pos) 
                        for pos in range(9) if self.board[pos] != 0 and self.board[pos] != pos])
        
        return cost      

    def _individual_distance(self, pos):
        incorrect = self.board[pos]

        return abs(incorrect//3 - pos//3) + abs(incorrect%3 - pos%3)

    def valid_move(self, end):
        start = self.blank
        if start >= 0 and end < 0 :
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
                neighbors.add(new_board)

        return neighbors

    def _blank(self):
        return np.argwhere(self._board == 0)[0]

    def __eq__(self, value):
        return np.array_equal(self._board, value.board)

    def __repr__(self):
        return "\n{}".format(self.board.reshape(3, 3))

    def __hash__(self):
        return hash(str(self.board))


if __name__ == '__main__':
    generate_boards(64, 100)