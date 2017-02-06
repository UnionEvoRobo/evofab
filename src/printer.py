from vector import Vector

class Printer(object):
    """A simple model of a 2d 3d-printer. Can draw in a GridWorld"""

    def __init__ (self, x, y, pen_size, grid):
        """Constructs a printer which draws in a GridWorld and moves in increments of fractions of cell widths

        x: the x coordinate for the printer start position
        y: the y coordinate for the printer start position
        pen_size: the size of the pen that the printer draws with (in gridcell units). If >1 then the printer will draw in multiple grid cells at a time. Note, the pen effectively has a hitbox of this width
        grid: the gridworld that the printer can act upon
        """

        self.position = Vector(float(x), float(y))
        self.pen_size = pen_size
        self.r = (grid.gridsize() * pen_size) / 2
        move_unit_pixels = grid.gridsize()
        self.v = Vector(move_unit_pixels, move_unit_pixels)
        self.grid = grid
        self.penDown = False

    def set_printer_direction(self, leftright, updown):
        """Set the direction the printer will move in on the following time steps.

        leftright: -1 = left motion, 0 = no leftright motion, 1 = right motion
        updown: -1 = down motion, 0 = no updown motion, 1 = up motion"""
        self.v = Vector(leftright*self.grid.gridsize(), updown*self.grid.gridsize())

    def set_position_on_grid(self, xcell, ycell):
        """ Move the printer to the specified cell position on the grid"""
        self.position = Vector((xcell * self.grid.gridsize()) + self.grid.gridsize()/2, (ycell * self.grid.gridsize())+ self.grid.gridsize()/2)

    def setPenUp(self):
        self.penDown = False
        
    def setPenDown(self):
        self.penDown = True

    def simulate(self, camera=None, gridworld=None):
        """Simulate a single time unit for the printer (which will be moving in a particular direction and may or may not have the pen down
        
        if provided a camera and gridworld, will take into account the size of the camera array and will not let the printer move so that the camera is no longer within the frame of the world"""

        is_valid = self.move_is_valid(camera, gridworld)
        if self.penDown:
            if is_valid:
                self.position = self.position.plus(self.v)
                position = (self.position.x, self.position.y)
                self.grid.PenDraw(position, self.pen_size)

    def move_is_valid(self, camera, gridworld):
        """ Checks if moving with the given dt will cause collision with the boundaries of the grid """
        new_loc_v = self.position.plus(self.v)
        new_loc = (new_loc_v.x, new_loc_v.y)
        return self.grid.inbounds(new_loc)
#        if not (camera and gridworld):
#            return self.grid.inbounds(new_loc)
#        else:
#            camera_bottom_right = camera.get_bottom_right_camera_coords()
#            camera_top_left = camera.get_top_left_camera_coords()
#            return self.grid.inbounds(camera_bottom_right) and self.grid.inbounds(camera_top_left)
