from ann import *
import ann_io
import random
from multiprocessing import Process, Queue

class Hat(object):

    def __init__(self, population):
        self.population = population
        self.ranges = []
        self.ranges.append(population[0].fitness) 
        for member in population[1:]:
            self.ranges.append(self.ranges[-1] + member.fitness)

    def pull(self):
        choice = random.randint(0, len(self.ranges) -1)
        i = 0
        while (choice - self.ranges[i]) >= 0:
            choice -= self.ranges[i]
            i += 1
        return self.population[i]

    def size(self):
        return sum(self.ranges)

class GenericGenotypeFactory(object):
    def __init__(self, population):
        self.pop = population

    def new(self):
        return Genotype(self.pop)

class Population(object):

    def __init__(self, random_seed, size, mutation_rate, mutation_range, crossover_rate, replacement_number, num_input, num_hidden, num_output, goal, outputfolder='gens/'):
        random.seed(random_seed)
        self.genotype_factory = GenericGenotypeFactory(self)
        self.outputfolder = outputfolder
        self.crossover_rate = crossover_rate
        self.size = size
        self.replacement_number = replacement_number
        self.mutation_rate = mutation_rate
        self.mutation_range = mutation_range
        self.goal = goal
        self.num_input = num_input
        self.num_hidden = num_hidden
        self.num_output = num_output
        self.members = []

    def create_initial_population(self):
        for i in range(self.size):
            new_member = self.genotype_factory.new()
            new_member.randomize()
            self.members.append(new_member)

    def write_stats(self, gen):
        return

    def iterate(self, num_iterations=10, threadnum=5):
        self.create_initial_population()
        print "evaluating initial population"
        self.eval_fitness(self.members, threadnum)
        self.print_fitnesses()
        self.output(0)
        for i in xrange(num_iterations):
            print "evaluating generation %d" % (i + 1)
            self.cull()
            self.write_stats(i)
            children = self.breed()
            self.eval_fitness(children, threadnum)
            self.print_fitnesses()
            self.output(i)

    def print_fitnesses(self):
        fitnesses = [member.fitness for member in self.members]
        fitnesses.sort()
        print fitnesses

    def output(self, gen):
        return
                    
    def eval_fitness(self, members, threadnum):
        q = Queue()
        counter = 0
        for iteration in range(0, len(members), threadnum):
            processes = []
            print 'evaluating members %d - %d of %d' % (counter + 1, counter + threadnum, len(members))
            while len(processes) < threadnum and counter + len(processes) < len(members):
                member = members[iteration + len(processes)]
                p = Process(target=member.calculate_fitness, args=(q,))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
            while not q.empty():
                actual_vals, fitness = q.get()
                possible_members = members[counter:counter + threadnum]
                member_num = 0
                found = False
                while member_num < threadnum and not found:
                    if actual_vals == possible_members[member_num].values:
                        found = True
                        possible_members[member_num].fitness = fitness
                    member_num += 1
                members[counter].fitness 
            counter += threadnum

    def cull(self):
        self.sort_by_fitness()
        self.members = self.members[self.replacement_number:] #cull the population

    def sort_by_fitness(self):
        self.members.sort(key=lambda x: x.fitness)

    def breed(self):
        hat = Hat(self.members)
        children = []
        num_crossover = int(self.replacement_number * self.crossover_rate)
        print num_crossover
        print self.replacement_number - num_crossover
        print num_crossover + (self.replacement_number - num_crossover)
        for i in range(num_crossover):
            current_member = hat.pull()
            child = self.genotype_factory.new()
            child.crossover(current_member, self.get_random_other_member(current_member))
            children.append(child)
        for i in range(self.replacement_number - num_crossover):
            current_member = hat.pull()
            child = self.genotype_factory.new()
            child.values = [x for x in current_member.values]
            child.mutate()
            children.append(child)
        self.members = children + self.members
        return children

    def get_random_other_member(self, to_ignore):
        """ returns a random member of the population other than the member specified
        """
        members = [member for member in self.members if member != to_ignore]
        choice = random.choice(members)
        return choice
        
class Genotype(object):
    """ Generic genotype for GAs """

    def __init__(self, population, size=0):
        self.population = population
        self.values = [ 0 for x in range(size)]
        self.fitness = None

    def crossover(self, p1, p2):
        location1 = random.randint(0, len(self.values))
        location2 = random.randint(0, len(self.values))
        while location2 == location1:
            location2 = random.randint(0, len(self.values))
        location1, location2 = min(location1, location2), max(location1, location2)
        self.values = p1.values[:location1] + p2.values[location1:location2] + p1.values[location2:]

    def randomize(self):
        self.values = [ random.randrange(-10, 10) for x in self.values]
