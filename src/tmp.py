import ann_io
from comp_gui_ann_runner import CompGuiAnnRunner

def run_from_file(cell_size, printer_pen_size, camera_cell_size, camera_grid_dimension, outputfolder, printer_runtime):
    n = ann_io.load(outputfolder + '/curbest.ann')
    runner = CompGuiAnnRunner(cell_size, printer_pen_size, camera_cell_size, camera_grid_dimension, draw_each=True, draw_full=True)
    runner.run(n, iterations=printer_runtime)

run_from_file(5, 5, 13, 3, '../', 1000)
