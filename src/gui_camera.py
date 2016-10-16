from grid import Grid
from vector import Vector
from camera import Camera
from gui_printer import GuiPrinter
import pygame

class GuiCamera(Camera):
    """Visual wrapper on the camera class"""

    def __init__(self, grid, printer, n, cell_size):
        super(GuiCamera, self).__init__(grid, printer, n, cell_size)
        self.color = pygame.color.Color("black")

    def draw(self, window):
        topleft = self.get_top_left_camera_coords()
        for row in xrange(self.n + 1):
                #xcoord = (col * self.grid.gridsize) + self.get_top_left_camera_coords().x
                pygame.draw.line(window, pygame.color.Color("black"), (topleft[0], topleft[1] + self.cell_size * row), (topleft[0] + self.cell_size * self.n, topleft[1] + self.cell_size * row))
        for col in xrange(self.n + 1):
                pygame.draw.line(window, pygame.color.Color("black"), (topleft[0] + self.cell_size * col, topleft[1]), (topleft[0] + self.cell_size * col, topleft[1] + self.cell_size * self.n))
