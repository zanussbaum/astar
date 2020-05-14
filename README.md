# A* Algorithm

A naive implementation of A*

This is my best attempt at replicating results from Russel and Norvig (AIMA pg. 104)
Currently, we generate 100 random puzzles with solution depths from 2 to 24 (only even) and then run the A* algorithm to compare two heuristics, misplaced tiles and Manhattan distance.

Dependencies (Run on Python 3.7)
===
* Matplotlib
* dill
* numpy
* tqdm
