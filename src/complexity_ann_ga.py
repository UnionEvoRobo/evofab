import modified_perimeter_to_area
import perimeter_to_area
import thread
from ann_genetic_algorithms import *
from comp_gui_ann_runner import CompGuiAnnRunner 



class CompPopulation(AnnPopulation):
    """A population of relatively simple neural networks. Currently impelmented to be semi-specific to the task of optimimizing neural netowrks to control a 3d-printer to draw particular (specified) shapes"""
    def __init__(self, random_seed, printer_runtime, size, mutation_rate, mutation_range, crossover_rate, replacement_number, num_input, num_hidden, num_output, outputfolder, use_global_coordinates = False, nodes_per_coordinate = 3, world_dimension = 100, reward_for_correct=None, punishment_for_incorrect=None, goal=None, is_visual=True, dump_to_files=False, cell_size=0, camera_grid_dimension=3, camera_cell_size = 1, printer_pen_size=1, recur = 0, time = 1):
        """Constructs a population on which to perform evolution to optimize to the defined fitness function

        random_seed: the random seed for the stochastic components of the system. Needs to be specified so that we have repeatable experiments
        printer_runtime: the amount of time steps for which the printer will draw on the world before being cut off
        size: the size of the population
        mutation_rate: the likelyhood of a component of a genotype being randomly changed during mutation (evaluated for each individual component of the encoding
        mutation_range: the range of values for mutation
        crossover_rate: the probability that a new member of the population will be created using crossover (breeding) instead of randomly mutated from a fitness-proportionally-selected parent
        replacement_number: the number of members of the population to cull after fitness ranking. must be even because crossover yields two children
        num_input: the number of input nodes for the neural network
        num_hidden: the number of hidden nodes for the neural network
        num_output: the number of output nodes for the neural network
        outputfolder: relative path to the folder where results shouldbe output to
        reward_for_correct: reward for putting material where there is supposed to be material
        punishment_for_incorrect: punishment for not putting material where there should be material
        goal: a list of relative paths to ``ideal/goal'' grid specifications (text files containing a rectangle of 0s and 1s (where a 1 means ``there should be material here'') and a single ``S'' denoting the start location for the printer
        is_visual: False if there should be GUI (pygame) output during evaluation, and False otherwise
        dump_to_files: Whether or not to dump statistics about fitness over time and a Pickled version of the highest-fitness individual so far to the appropriate directory
        cell_size: the number of pixels in a single grid cell
        camera_grid_dimension: n, the number of cells in one dimension of the nxn camera grid.  must be odd so that the camera aligns with the grid cells
        camera_cell_size: the factor by which a camera cell is larger than a world cell. if none is provided, will default to 1.
        printer_pen_size: the factor by which cell width is divided by to determine the distance moved by the printer in a single time unit
        recur: 0 if there should be no recurrance in the neural network
               1 for recurance from outputs to inputs
               2 for recurance from inputs to inputs
               3 for recurance from both
        time: how many time steps to recur for
        """
        super(CompPopulation, self).__init__(random_seed, printer_runtime, size, mutation_rate, mutation_range, crossover_rate, replacement_number, num_input, num_hidden, num_output, outputfolder, reward_for_correct, punishment_for_incorrect, goal, is_visual, dump_to_files, cell_size, camera_grid_dimension, camera_cell_size, printer_pen_size, recur, time)
        self.genotype_factory = CompGenotypeFactory(self, recur, time)
        self.runner = None
        self.nodes_per_coordinate = nodes_per_coordinate
        self.use_global_coordinates = use_global_coordinates
        self.world_dimension = world_dimension
        if use_global_coordinates:
            self.num_input += nodes_per_coordinate * 2

    def run_from_file(self, cell_size, printer_pen_size, camera_cell_size, camera_grid_dimension, outputfolder, printer_runtime):
        n = ann_io.load(outputfolder + '/curbest.ann')
        if not self.runner:
            self.runner = CompGuiAnnRunner(cell_size, printer_pen_size, camera_cell_size, camera_grid_dimension, self.use_global_coordinates, self.nodes_per_coordinate, self.world_dimension, draw_each=True, draw_full=False)
        else:
            self.runner.reset()
        self.runner.run(n, iterations=printer_runtime)

    def iteration(self):
        super(CompPopulation, self).iteration()
        thread.start_new_thread(self.run_from_file, (self.cell_size, self.printer_pen_size, self.camera_cell_size, self.camera_grid_dimension, self.outputfolder, self.printer_runtime))

class CompGenotypeFactory(object):
    def __init__(self, population, recur, time):
        """An GenotypeFactory for ANNs"""

        self.pop = population
        self.recur = recur
        self.time = time

    def new(self):
        return CompGenotype(self.pop, self.recur, self.time)

class CompGenotype(AnnGenotype):

    def __init__(self, population, recur, time):
        """Construct an ANN Genotype with the given population (and therefore the given properties of that population)
        
        recur: 0 if there should be no recurrance in the neural network
               1 for recurance from outputs to inputs
               2 for recurance from inputs to inputs
               3 for recurance from both
        time: how many time steps to recur for"""
        
        super(CompGenotype, self).__init__(population, recur, time)

    def calculate_fitness(self, q=None):
       phenotype = self.express() 
       self.fitness = modified_perimeter_to_area.evaluate(phenotype)
       print self.fitness

    def express(self):
        """Control the simulated 2d 3d-printer with this member of the population and evaluate the fitness of the output"""

        self.ann.allConnections = self.values
        if self.population.is_visual:
            runner = CompGuiAnnRunner(self.population.cell_size, self.population.printer_pen_size, self.population.camera_cell_size, self.population.camera_grid_dimension, self.population.use_global_coordinates, self.population.nodes_per_coordinate, self.population.world_dimension, draw_each=True, draw_full=False)
        else:
            runner = CompGuiAnnRunner(self.population.cell_size, self.population.printer_pen_size, self.population.camera_cell_size, self.population.camera_grid_dimension, self.population.use_global_coordinates, self.population.nodes_per_coordinate, self.population.world_dimension, draw_each=False)
        actual_grid = runner.run(self.ann, iterations=self.population.printer_runtime)
        return actual_grid.grid

    def randomize(self):
        """Randomize this member of the population"""
        lower, upper = self.population.mutation_range
        self.values = [ random.randrange(lower, upper) for x in self.values]
