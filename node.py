class Node:
    def __init__(self, board, depth=0, heuristic=0):
        super().__init__()
        self.board = board
        self.depth = depth
        self.cost = board.heuristic(heuristic) + depth

    def __eq__(self, value):
        return self.cost == value.cost

    def __lt__(self, value):
        if self.cost == value.cost:
            return self.depth < value.depth

    def __repr__(self):
        return self.board.__repr__()
    
    def __hash__(self):
        return self.board.__hash__()