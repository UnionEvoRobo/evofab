import math
import numpy as n

from vector import Vector
from grid import Grid

class GridWorld(object):
    """Describes a GridWorld (the build-plate-world that the printer exists in.
    
    A gridworld can function as simply a drawing canvas. We can also set an ``ideal_grid'', which is an aditional Grid object (often constructed from a given gridfile path) which specifies a ``goal'' for the world (whatever that means for the particular implemention)."""

    def __init__(self,wid,hi,scale):
        """Construct a blank GridWorld with the given dimensions and the given pixel scale for the cells"""
        self.grid = Grid(wid, hi,scale)

    def set_ideal_grid(self, grid):
        """Set the ideal grid for the GridWorld. Allows a user to keep track of the ideal and actual gridworld and query for the difference between them"""
        self.ideal_grid = grid

    def get_starting_position(self):
        if self.ideal_grid.starting_point:
            return self.ideal_grid.starting_point
        else:
            assert(1 == 2) #no ideal grid defined. an ideal grid can be defined for the gridworld with set_ideal_grid

    def inbounds(self,p):
        """Checks if the given pixel coordinates are in bounds for the gridworld"""
        return self.grid.inbounds(p)

    def width(self):
        return self.grid.width

    def height(self):
        return self.grid.height

    def gridsize(self):
        """Returns the cell scale for the GridWorld (the number of pixels making up each cell)"""
        return self.grid.gridsize

    def PenDraw(self,p,pen_size):
        """Draw with the pen in the closest grid location to the pixel location (a tuple)
        
        pen_size: the width of the pen (in gridcells)"""
        if pen_size != 1:
            pixel_dimension = pen_size/2 * self.gridsize()
            topleft_corner = n.subtract(p, (pixel_dimension/2.0, pixel_dimension/2.0))
            bottomright_corner = n.add(p, (pixel_dimension/2.0, pixel_dimension/2.0))
            topleft_cell = self.grid.find_closest_gridloc(topleft_corner)
            bottomright_cell = self.grid.find_closest_gridloc(bottomright_corner)
            #fill all of the cells that fall in the range between topleft -- bottomright
            for i in range(topleft_cell[0], bottomright_cell[0] + 1):
                for j in range(topleft_cell[1], bottomright_cell[1] + 1):
                    self.grid.set_loc_val(i, j, 1)
        else:
            myx,myy = self.grid.find_closest_gridloc(p)
            self.grid.set_loc_val(myx, myy, 1)

    #shouldn't need these for now -- might be useful later?
    def distance(self,startp,endp):
            (endx,endy) = endp
            (startx,starty) = startp
            return math.sqrt(pow(endx - startx,2) + pow(endy - starty,2))
                              
    def manhattan(self,startp,endp):
            (endx,endy) = endp
            (startx,starty) = startp
            '''given two points, return manhattan distance of two points'''
            return (abs(endx - startx) + abs(endy - starty))
    
    def estimate_distance(self,start,end):
             #return self.manhattan(start,end)
             return self.distance(start,end)
