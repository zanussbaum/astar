import numpy as np
import dill as pickle
from tqdm import tqdm
from copy import deepcopy
from collections import defaultdict

def generate_board(depth, board):
    i = 0

    moves = [-1, 1, 3, -3]
    last_move = 0
    while i < depth:
        move = np.random.choice([m for m in moves if m != -last_move])
        pos = board.blank + move
        while not board.valid_move(pos):
            move = np.random.choice([m for m in moves if m != -last_move])
            pos = board.blank + move

        new_board = board.swap_tile(pos)
        i += 1
        board = new_board
        last_move = move
        
    return board

def generate_random_boards():
    puzzles = defaultdict(set)
    goal = np.array([i for i in range(9)])
    done = 0
    pbar = tqdm(total=1200, desc="Generating random boards")
    while done < 12:
        for depth in range(2, 25, 2):
            np.random.shuffle(goal)
            if len(puzzles[depth]) < 100:
                goal_board = Board(goal)
                board = generate_board(depth, goal_board)
            
                use = True
                for value in puzzles.values():
                    if board in value:
                        use = False
                        break

                if use:
                    puzzles[depth].add(board)
                    pbar.update(1)
            else:
                done += 1

    for key, value in puzzles.items():
        with open("puzzles/depth_{}_puzzles.p".format(key), 'wb') as f:
            pickle.dump(value, f)

    print("saved random boards")

    return puzzles
    
class Board:
    def __init__(self, goal=None):
        if goal is None:
            self.goal = np.array([i for i in range(9)])
        else:
            self.goal = goal
        self._board = deepcopy(self.goal)

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
        # these are wrong for random boards
        if value == 0:
            # misplaced tile heuristic
            cost = sum([1 for i in range(9) if self.board[i] != self.goal[i] and self.board[i] != 0])
        else:
            #need to fix
            cost = sum([self._individual_distance(pos) 
                        for pos in range(9) if self.board[pos] != 0 and self.board[pos] != self.goal[pos]])
        
        return cost      

    def _individual_distance(self, pos):
        incorrect_tile = self.board[pos]
        correct_pos = np.argwhere(self.goal==incorrect_tile)

        return abs(pos//3 - correct_pos//3) + abs(pos%3 - correct_pos%3)

    def valid_move(self, end):
        start = self.blank
        if start >= 0 and end < 0 :
            return False

        if end // 3 > 2:
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
    generate_random_boards()