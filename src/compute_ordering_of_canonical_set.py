import os
from morphological_complexity import evaluate
import perimeter_to_area
import perimeter_to_rectangular_bound
from grid import Grid

def compute_ordering(eval_function):
    results = []
    for f in os.listdir("worlds/canonical_inputs"):
        if f.endswith(".test"):
            f = "worlds/canonical_inputs/" + f
            grid = Grid(scale = 15, path = f)
            result = eval_function(grid)
            results.append((f, result))
    results.sort(key = lambda x: x[1])
    for result in results:
        print result

if __name__ == "__main__":
    compute_ordering(perimeter_to_area.evaluate)
