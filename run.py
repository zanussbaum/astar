import numpy as np
import dill as pickle
import multiprocessing as mp
from tqdm import tqdm
from node import Node
from a_star import a_star
from board import generate_random_boards, Board
from collections import defaultdict


def effective_branching_factor(nodes, depth):
    total = nodes + 1

    max_error = 1e-4
    error = float('inf')

    low = 0
    high = 4
    while abs(error) > max_error:
        mid = (low + high)/ 2
        summation = sum(mid**i for i in range(depth + 1))
        error = summation - total

        if error > 0:
            high = mid
        else:
            low = mid

    return mid
    
def solve(depth, puzzles):
    results = {"misplaced": {
            "nodes": [],
            "depth": [],
            "ebf":[]
        },
        "manhattan": {
            "nodes": [],
            "depth": [],
            "ebf":[]
        }
    }

    for puzzle in tqdm(puzzles, desc="Depth {}".format(depth)):
        misplaced_nodes, misplaced_depth = a_star(Node(puzzle), 0)
        results["misplaced"]["nodes"].append(misplaced_nodes)
        results["misplaced"]["depth"].append(misplaced_depth)
        results["misplaced"]["ebf"].append(effective_branching_factor(misplaced_nodes, misplaced_depth))

        man_nodes, man_depth = a_star(Node(puzzle), 1)
        results["manhattan"]["nodes"].append(man_nodes)
        results["manhattan"]["depth"].append(man_depth)
        results["manhattan"]["ebf"].append(effective_branching_factor(man_nodes, man_depth))

    return results
