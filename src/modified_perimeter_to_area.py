from morphological_complexity import identify_boundary_lines, compute_boundary_path
from math import sqrt

def evaluate(grid):
    boundaries = identify_boundary_lines(grid)
    path = compute_boundary_path(boundaries)
    #compute perimeter of path (counting single ``jaggies'' from corner to corner --- as sqrt(2) --- instead of 2 units)
    corner_to_corner = sqrt(2)
    perim = 0
    skip = False
    for a,b in zip(path[:-2], path[1:]):
        a_1, a_2 = a
        b_1, b_2 = b
        if (a_1 == b_1 and a_2 != b_2) or (a_1 != b_1 and a_2 == b_2) or (a_1 == b_2 and a_2 != b_1) or (a_1 != b_2 and a_2 == b_2):
            perim += 1 
            skip = True
        else:
            if not skip:
                perim += 1
            else:
                skip = False
    a_1, a_2 = path[-1]
    b_1, b_2 = path[0]
    if (a_1 == b_1 and a_2 != b_2) or (a_1 != b_2 and a_2 == b_2):
        perim += corner_to_corner
    else:
        perim += 2

    #compute number filled cells
    filled = 0
    for x in range(grid.width):
        for y in range(grid.height):
            if grid.val_at(x,y):
                filled += 1
    return (perim*perim) / float(filled)
