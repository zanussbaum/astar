import heapq as h
from collections import deque
from node import Node
from board import generate_boards, Board

def reconstruct_path(came_from, current):
    path = deque([current])

    while current in came_from:
        current = came_from[current]
        path.appendleft(current)

    return path

def a_star(start, heuristic):
    open_set = [start]

    came_from = {}
    came_from[start] = None

    current_cost = {}
    current_cost[start.board] = 0

    while len(open_set) > 0:
        current = h.heappop(open_set)
        if current.board.solved:
            return reconstruct_path(came_from, current)

        neighbors = [Node(c, current.depth+1, heuristic) for c in current.board.neighbors()]

        for n in neighbors:
            if n.board not in current_cost or n.cost < current_cost[n.board]:
                current_cost[n.board] = n.cost
                h.heappush(open_set, n)
                came_from[n] = current
        
    raise ValueError("Unsolvable")


if __name__ == '__main__':
    boards = generate_boards(8, 1)

    start = Node(boards.pop())
    print("started from: {}\n".format(start))
    path = a_star(start, 1)
    print(path)

