from gui_ann_runner import *

class CompGuiAnnRunner(GuiAnnRunner):

    def __init__(self, cell_size, pen_size, camera_cell_size, camera_grid_dimension, draw_each=False, draw_full=False):
        assert(camera_grid_dimension %2 != 0) #must have odd camera dimensions so that the camera aligns with the grid cells
        self.dimension = 100
        self.cell_size = cell_size
        self.pen_size = pen_size
        self.camera_cell_size = camera_cell_size
        self.camera_grid_dimension = camera_grid_dimension

        self.draw_each = draw_each
        self.draw_full = draw_full
        self.gridworld = GuiGridWorld(self.dimension, self.dimension, cell_size)
        self.printer = GuiPrinter(10, 10, pen_size, self.gridworld)
        self.camera = GuiCamera(self.gridworld.grid, self.printer, camera_grid_dimension, camera_cell_size * cell_size)

        if draw_each or draw_full:
            #gui stuff
            width = self.gridworld.width() * self.gridworld.gridsize()
            height = self.gridworld.height() * self.gridworld.gridsize()

            self.window = pygame.display.set_mode((width, height))
            pygame.init()

    def reset(self):
        self.gridworld = GuiGridWorld(100, 100, self.cell_size)
        self.printer = GuiPrinter(10, 10, self.pen_size, self.gridworld)
        self.camera = GuiCamera(self.gridworld.grid, self.printer, self.camera_grid_dimension, self.camera_cell_size * self.cell_size)

    def run(self, n, iterations=10000):
        self.printer.set_position_on_grid(50, 50)
        self.printer.setPenDown()
        count_doing_nothing = 0
        for i in xrange(iterations):
            x_vals = self.get_val_for_coord_inputs(self.printer.position.x)
            y_vals = self.get_val_for_coord_inputs(self.printer.position.y)
            sensor_vals = self.camera.all_cell_values() + x_vals + y_vals
            result = n.propagate(sensor_vals)
            result = [int(round(x)) for x in result]
            vel =  self.get_velocity(result)
            if vel == (0, 0):
                count_doing_nothing += 1
            self.printer.set_printer_direction(*vel)
            self.printer.simulate(self.camera, self.gridworld)
            if count_doing_nothing > 20:
                break
            if self.draw_full:
                self.update()
        if self.draw_each:
            self.update()
        return self.gridworld

    def get_val_for_coord_inputs(self, n):
        a = b = c = 0
        each_n = self.dimension/3.0
        if n > each_n:
            a = each_n
            n -= each_n
            if n > each_n:
                b = each_n
                n -= each_n
                if n > each_n:
                    c = each_n
                else:
                    c = n
            else:
                c = n
        else:
            a = n
        return [a,b,c]
