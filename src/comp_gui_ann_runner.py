from gui_ann_runner import *

class CompGuiAnnRunner(GuiAnnRunner):

    def __init__(self, cell_size, pen_size, camera_cell_size, camera_grid_dimension, draw_each=False, draw_full=False):
        assert(camera_grid_dimension %2 != 0) #must have odd camera dimensions so that the camera aligns with the grid cells
        self.draw_each = draw_each
        self.draw_full = draw_full
        self.gridworld = GuiGridWorld(100, 100, cell_size)
        self.printer = GuiPrinter(10, 10, pen_size, self.gridworld)
        self.camera = GuiCamera(self.gridworld.grid, self.printer, camera_grid_dimension, camera_cell_size * cell_size)

        if draw_each or draw_full:
            #gui stuff
            width = self.gridworld.width() * self.gridworld.gridsize()
            height = self.gridworld.height() * self.gridworld.gridsize()

            self.window = pygame.display.set_mode((width, height))
            pygame.init()

    def run(self, n, iterations=10000):
        self.printer.set_position_on_grid(50, 50)
        self.printer.setPenDown()
        for i in xrange(iterations):
            sensor_vals = self.camera.all_cell_values()
            result = n.propagate(sensor_vals)
            result = [int(round(x)) for x in result]
            self.printer.set_printer_direction(*self.get_velocity(result))
            self.printer.simulate(self.camera, self.gridworld)
            if self.draw_full:
                self.update()
        if self.draw_each:
            self.update()
        return self.gridworld
