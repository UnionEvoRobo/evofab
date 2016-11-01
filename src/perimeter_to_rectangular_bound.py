from morphological_complexity import identify_boundary_lines

def evaluate(grid):
    boundaries = identify_boundary_lines(grid)
    filled = []
    for x in range(grid.width):
        for y in range(grid.height):
            if grid.val_at(x,y):
                filled.append((x,y))
    min_x = min([x for x,y in filled])
    max_x = max([x for x,y in filled])
    min_y = min([y for x,y in filled])
    max_y = max([y for x,y in filled])
    dx = max_x - min_x
    dy = max_y - min_y
    rect_hull = 2*dx + 2*dy
    return len(boundaries) / float(rect_hull)
