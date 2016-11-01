from grid import Grid
from gui_gridworld import GuiGridWorld
import pygame
import time
from math import *

def evaluate(grid):
    boundaries = identify_boundary_lines(grid)
    path = compute_boundary_path(boundaries)
    complexity = calculate_complexity(path)

    return complexity

    #gridworld = GuiGridWorld(grid.width, grid.height, grid.gridsize)
    #gridworld.grid = grid

    ##some pygame trash to get an image of the input grid
    #width = gridworld.width() * gridworld.gridsize()
    #height = gridworld.height() * gridworld.gridsize()
    #window = pygame.display.set_mode((width, height))
    #pygame.init()

    #gridworld.draw(window)
    #pygame.display.update()
    #time.sleep(1000)

def calculate_complexity(path):
    path_of_filled_cells = [x[0] for x in path]
    n = len(path_of_filled_cells)
    
    angles = []
    for i,j in zip(xrange(0,n,2), xrange(2, n, 2)):
        a1, b1 = path_of_filled_cells[i]
        a2, b2 = path_of_filled_cells[j]

        dot = a1 * b1 + a2 * b2
        angle = acos(round(dot/(sqrt(a1*a1 + a2*a2) * sqrt(b1*b1 + b2*b2)), 10))
        angle = angle * 180/pi
        angles.append(angle)

    bin_width = 7
    num_bins = int(floor((max(angles) - min(angles))/bin_width))

    PDF = []
    for x in range(num_bins + 1):
        l = min(angles) + (x * bin_width)
        r = min(angles) + ((x+1) * bin_width)
        num_in_range = 0
        for angle in angles:
            if angle > l and angle < r :
                num_in_range += 1
        PDF.append(num_in_range/float(len(angles)))
    
    #for n,p in enumerate(PDF):
    #    print (min(angles) + (n * bin_width)), "&", (min(angles) + ((n+1)*bin_width)), "&", p
        
    e = 0
    for p in PDF:
        if p > 0:
            e += p * log(p, 10)
    e = -e
    #print
    #print
    #print "entropy", e
    return e
    #end


def compute_boundary_path(boundaries):
    cur = boundaries[0]
    path = [cur]
    go = True
    while go:
        (a,b) = cur[0]
        (x,y) = cur[1]
        #check which coordinate is changed between the two
        if a != x: #the x coordinate
            #either keep moving along the current line or pivot around the filled cell
            right_move = ((a, b + 1), (x, y + 1))
            left_move = ((a, b - 1), (x, y - 1))
            left_pivotfill = ((a,b), (a, b - 1))
            right_pivotfill = ((a,b), (a, b + 1))
            left_pivotempty = ((x, y - 1), (x,y))
            right_pivotempty = ((x,y + 1), (x,y))
            if right_move in boundaries and right_move not in path:
                correct_move = right_move
            elif left_move in boundaries and left_move not in path:
                correct_move = left_move
            #pivot 
            elif left_pivotfill in boundaries and left_pivotfill not in path:
                correct_move = left_pivotfill
            elif right_pivotfill in boundaries and right_pivotfill not in path:
                correct_move = right_pivotfill
            elif left_pivotempty in boundaries and left_pivotempty not in path:
                correct_move = left_pivotempty
            elif right_pivotempty in boundaries and right_pivotempty not in path:
                correct_move = right_pivotempty
            else:
                go = False
        else: # the y coordinate varies
            up_move = ((a + 1, b), (x + 1, y))
            down_move = ((a - 1, b), (x - 1, y))
            up_pivotfill = ((a,b), (a-1, b))
            down_pivotfill = ((a,b), (a+1, b))
            up_pivotempty = (((x-1,y), (x,y)))
            down_pivotempty = (((x+1,y), (x,y)))
            if up_move in boundaries and up_move not in path:
                correct_move = up_move 
            elif down_move in boundaries and down_move not in path:
                correct_move = down_move 
            #pivot 
            elif up_pivotfill in boundaries and up_pivotfill not in path:
                correct_move = up_pivotfill
            elif down_pivotfill in boundaries and down_pivotfill not in path:
                correct_move = down_pivotfill
            elif up_pivotempty in boundaries and up_pivotempty not in path:
                correct_move = up_pivotempty
            elif down_pivotempty in boundaries and down_pivotempty not in path:
                correct_move = down_pivotempty
            else:
                go = False
        cur = correct_move
        path.append(correct_move)
    return path

def identify_boundary_lines(grid):
    """We identify the set of borders between filled and nonfilled cells. Each of these boundaries can be denoted as a pair of cell-coordinate pairs ((a,b),(c,d)) where each of (a,b),(c,d) are the coordinates of a cell (with the two cells next to each other).

    returns a list of cell boundaries containing the subset of all boundaries where one cell is filled and the other is not"""

    #print "computing..."

    boundary_cells = []

    #check all cells and the cell to the right of that cell
    for x_1 in range(grid.width - 1):
        x_2 = x_1 + 1 
        for y_1 in range(grid.height):
            y_2 = y_1
            if grid.val_at(x_1, y_1) != grid.val_at(x_2, y_2):
                boundary_cells.append(((x_1, y_1), (x_2, y_2)))

    #left 
    for x_1 in range(1, grid.width):
        x_2 = x_1 - 1
        for y_1 in range(grid.height):
            y_2 = y_1
            if grid.val_at(x_1, y_1) != grid.val_at(x_2, y_2):
                boundary_cells.append(((x_1, y_1), (x_2, y_2)))
    #up
    for x_1 in range(grid.width):
        x_2 = x_1
        for y_1 in range(grid.height - 1):
            y_2 = y_1 + 1
            if grid.val_at(x_1, y_1) != grid.val_at(x_2, y_2):
                boundary_cells.append(((x_1, y_1), (x_2, y_2)))
    #down
    for x_1 in range(grid.width):
        x_2 = x_1
        for y_1 in range(1, grid.height):
            y_2 = y_1 - 1
            if grid.val_at(x_1, y_1) != grid.val_at(x_2, y_2):
                boundary_cells.append(((x_1, y_1), (x_2, y_2)))

    #eliminate duplicates (order of (a,b) doesn't matter) and sort in order of (filled, non-filled)
    no_duplicates = []
    for boundary in boundary_cells:
        x,y = boundary
        alt = (y,x)
        if (not boundary in no_duplicates) and (not alt in no_duplicates):
            if grid.val_at(*x):
                boundary = boundary
            else:
                boundary = alt
            no_duplicates.append(boundary)

    return no_duplicates

if __name__ == "__main__":
    grid = Grid(scale = 15, path = 'worlds/canonical_inputs/test.test')
    evaluate(grid)
