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
        a_fill, a_empty = a
        b_fill, b_empty = b
        #if (a_fill == b_fill and a_empty != b_empty) or (a_fill != b_fill and a_empty == b_empty) or (a_fill == b_empty and a_empty != b_fill) or (a_fill != b_empty and a_empty == b_empty):
        if (a_empty == b_empty):
            perim += corner_to_corner
            skip = True
        else:
            if not skip:
                perim += 1
            else:
                skip = False
    a_fill, a_empty = path[-1]
    b_fill, b_empty = path[0]
    if (a_empty == b_empty):
        perim += corner_to_corner
        perim -= 1
    else:
        perim += 1


    #compute number filled cells
    filled = 0
    for x in range(grid.width):
        for y in range(grid.height):
            if grid.val_at(x,y):
                filled += 1
    return (perim*perim) / float(filled)
