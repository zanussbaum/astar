import heapq as h
import numpy as np 
from board import Board, generate_board
from collections import deque
from node import Node

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

    nodes = 1

    while len(open_set) > 0:
        current = h.heappop(open_set)
        if current.board.solved:
            return nodes, current.depth

        neighbors = [Node(c, current.depth+1, heuristic) for c in current.board.neighbors()]

        for n in neighbors:
            if n.board not in current_cost or n.cost < current_cost[n.board]:
                current_cost[n.board] = n.cost
                h.heappush(open_set, n)
                came_from[n] = current
                nodes += 1
        
    raise ValueError("Unsolvable")


if __name__ == '__main__':
    goal = np.array([i for i in range(9)])
    np.random.shuffle(goal)
    goal_board = Board(goal)
    board = generate_board(4, goal_board)

    start = Node(board, heuristic=1)
    print("started from: {}\n".format(start))
    nodes, depth, path = a_star(start, 1)
    print(nodes, depth)
    print(path)

