import dill as pickle
from run import *
from test import *

try:
    puzzles = {}
    for i in range(2, 25, 2):
        with open("puzzles/depth_{}_puzzles.p".format(i), "rb") as f:
            puzzles[i] = pickle.load(f)

except FileNotFoundError:
    puzzles = generate_random_boards()


with mp.Pool(processes=mp.cpu_count()) as p:
    results = [p.starmap(solve, [(depth, puzzles[depth]) for depth in range(2, 25, 2)])]


with open("results.p", "wb") as f:
    pickle.dump(results, f)

avg_results = defaultdict(lambda : defaultdict(lambda: defaultdict(float)))

for i, depth in enumerate(range(2, 25, 2)):
    avg_results[depth]['misplaced']['avg_nodes'] = np.mean(results[0][i]["misplaced"]["nodes"])
    avg_results[depth]['misplaced']['avg_ebf'] = np.mean(results[0][i]["misplaced"]["ebf"])

    avg_results[depth]["manhattan"]["avg_nodes"] = np.mean(results[0][i]["manhattan"]["nodes"])
    avg_results[depth]["manhattan"]["avg_ebf"] = np.mean(results[0][i]["manhattan"]["ebf"])


plot_nodes(avg_results)
plot_ebf(avg_results)