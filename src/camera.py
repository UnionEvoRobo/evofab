from grid import Grid
from vector import Vector
from printer import Printer

class Camera(object):
    """ Simulates a camera attached to the print head of the printer.
    It is defined in a grid, and does processing on each grid space to
    determine the percentage filled with material in that camera region.

    """

    def __init__(self, grid, printer, n, cell_size):
        """constructs a Camera based on the given world grid,
        printer, and n (it is an n x n grid camera).

        grid: the grid (representation of the world/build plate that the camera is "looking at"
        printer: the printer that the camera is attached to
        n: the camera is an n x n grid
        cell_size: the pixel width of each camera cell"""

        self.grid = grid
        self.printer = printer
        self.n = n
        self.cell_size = cell_size

    def all_cell_values(self):
        output = [self.percent_in_view((x, y)) for x in range(self.n) for y in range(self.n)]
        return output

    def get_top_left_camera_coords(self):
        printer_loc = (self.printer.position.x, self.printer.position.y)
        #calculate the location of the top left camera cell
        x = printer_loc[0] - int(self.cell_size*(self.n/2.0))
        y = printer_loc[1] - int(self.cell_size*(self.n/2.0))
        return (x,y)

    def get_bottom_right_camera_coords(self):
        topleft = self.get_top_left_camera_coords()
        return (topleft[0] + self.cell_size*(self.n), topleft[1] + self.cell_size*(self.n))

    def percent_in_view(self, camera_cell):
        printer_loc = (self.printer.position.x, self.printer.position.y)
        #calculate the location of the top left camera cell
        x = printer_loc[0] - int(self.cell_size*(self.n/2.0))
        y = printer_loc[1] - int(self.cell_size*(self.n/2.0))
        topleft_grid_corner = (x,y)
        topleft_corner_of_cell = (topleft_grid_corner[0] + (camera_cell[0] * self.cell_size), topleft_grid_corner[1] + (camera_cell[1] * self.cell_size))
        bottomright_corner_of_cell = (topleft_corner_of_cell[0] + self.cell_size, topleft_corner_of_cell[1] + self.cell_size)
        topleft_gridloc = self.grid.find_closest_gridloc(topleft_corner_of_cell)
        bottomright_gridloc = self.grid.find_closest_gridloc(bottomright_corner_of_cell)
        count = 0
        for i in range(topleft_gridloc[0], bottomright_gridloc[0]):
            for j in range(topleft_gridloc[1], bottomright_gridloc[1]):
                if not (self.grid.width - 1 < i or i < 0 or self.grid.height -1 < j or j < 0):
                    if self.grid.val_at(i,j) == 1:
                        count += 1
        num_cells = (bottomright_gridloc[0] - topleft_gridloc[0]) * (bottomright_gridloc[1] - topleft_gridloc[1])
        return count/float(num_cells)
