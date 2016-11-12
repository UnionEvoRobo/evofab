from morphological_complexity import identify_boundary_lines

def evaluate(grid):
    boundaries = identify_boundary_lines(grid)
    filled = 0
    for x in range(grid.width):
        for y in range(grid.height):
            if grid.val_at(x,y):
                filled += 1
    return (len(boundaries)*len(boundaries)) / float(filled)
