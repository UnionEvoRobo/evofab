from gui_ann_runner import *

class CompGuiAnnRunner(GuiAnnRunner):

    def __init__(self, cell_size, pen_size, camera_cell_size, camera_grid_dimension, use_global_coordinates, nodes_per_coordinate, world_dimension, draw_each=False, draw_full=False):
        assert(camera_grid_dimension %2 != 0) #must have odd camera dimensions so that the camera aligns with the grid cells
        self.dimension = world_dimension
        self.cell_size = cell_size
        self.pen_size = pen_size
        self.camera_cell_size = camera_cell_size
        self.camera_grid_dimension = camera_grid_dimension
        self.use_global_coordinates = use_global_coordinates
        self.nodes_per_coordinate = nodes_per_coordinate

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
            sensor_vals = self.camera.all_cell_values()
            if self.use_global_coordinates:
                x_vals = self.get_val_for_coord_inputs(self.printer.position.x)
                y_vals = self.get_val_for_coord_inputs(self.printer.position.y)
                sensor_vals = sensor_vals + x_vals + y_vals
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

    def get_val_for_coord_inputs(self, coord):
        value_per = coord / self.dimension
        result = []
        for x in range(self.nodes_per_coordinate):
            v = coord % value_per
            if v:
                result.append(v)
                coord -= v
            elif coord > 0:
                result.append(value_per)
            else:
                result.append(0)
        return result
