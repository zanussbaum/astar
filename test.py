import dill as pickle
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def plot_nodes(avg_results):
    man_label = "Manhattan Depth"
    mis_label = "Misplaced Depth"
    for depth in range(2, 25, 2):
        plt.plot(depth, avg_results[depth]['misplaced']['avg_nodes'], 'o', 
                label=mis_label if depth == 2 else "", c='r')
        plt.plot(depth, avg_results[depth]['manhattan']['avg_nodes'], 'o', 
                label=man_label if depth == 2 else "", c='b')

    plt.legend(loc='best')
    plt.title("Average Number of Nodes vs Depth")
    plt.savefig("Average Number of Nodes vs Depth")
    plt.close()

def plot_ebf(avg_results):
    man_label = "Manhattan Depth"
    mis_label = "Misplaced Depth"
    for depth in range(2, 25, 2):
        plt.plot(depth, avg_results[depth]['misplaced']['avg_ebf'], 'o', 
                label=mis_label if depth == 2 else "", c='r')
        plt.plot(depth, avg_results[depth]['manhattan']['avg_ebf'], 'o', 
                label=man_label if depth == 2 else "", c='b')

    plt.legend(loc='best')
    plt.title("Average EBF vs Depth")
    plt.savefig("Average EBF vs Depth")
    plt.close()
