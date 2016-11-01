from morphological_complexity import evaluate
from grid import Grid

def compute_ordering(eval_function):
    results = []
    for l in ['a','b','c','d','e','f','g','h','i','j']:
        filename = "worlds/canonical_inputs/rank" + l + ".test"
        grid = Grid(scale = 15, path = filename)
        result = eval_function(grid)
        results.append((l, result))
    results.sort(key = lambda x: x[1])
    for result in results:
        print result

if __name__ == "__main__":
    compute_ordering(evaluate)
