from ann import *
import ann_io
from clean_ann_runner import AnnRunner
import random
from multiprocessing import Process, Queue

"""
    Doesn't work if the neural network achieves sufficient intelligence to modify its source code

        -- Johnny Depp
"""

class Hat:

    def __init__(self, population):
        self.tickets = []
        for member in population:
            for i in range(member.fitness):
                self.tickets.append(member)

    def pull(self):
        return self.tickets[random.randint(0, len(self.tickets) -1)]

    def size(self):
        return len(self.tickets)

class Population:

    def __init__(self, size, mutation_rate, replacement_number, num_input, num_hidden, num_output, goal, outputfolder='gens/'):
        self.outputfolder = outputfolder
        self.size = size
        self.replacement_number = replacement_number
        self.mutation_rate = mutation_rate
        self.goal = goal
        self.num_input = num_input
        self.num_hidden = num_hidden
        self.num_output = num_output
        self.members = []

    def random_seed(self):
        for i in range(self.size):
            new_member = Member(self)
            new_member.randomize()
            self.members.append(new_member)

    def CalcDiversityOfPop(self):

        for member in self.members:
            curdiv = 0.0
            for other in self.members:
                if other is not member:
                    curdiv += member.distanceToOtherGenotype(other)
            member.diversity = curdiv


    def iterate(self, num_iterations=10):
        self.random_seed()
        for i in xrange(num_iterations):
            print "evaluating generation %d" % (i + 1)
            fitvals = self.eval_fitness()
          
            self.cull()
            print [x.fitness for x in self.members]

            self.CalcDiversityOfPop()

            print 'diversity = '+ str(sum([m.diversity for m in self.members]))

            self.breed()
            for member_num, member in enumerate(self.members):
                filename = self.outputfolder + 'g%d_m%d' % (i, member_num)
                ann_io.save(member.ann, filename)
                    
    def eval_fitness(self):
        q = Queue()
        counter = 0
        for member in self.members:
            member.calculate_fitness()

#        for iteration in range(0, len(self.members), 12):
#            processes = []
#            while len(processes) < 12 and counter + len(processes) + 1 < len(self.members):
#                member = self.members[iteration + len(processes)]
#                p = Process(target=member.calculate_fitness, args=(q,))
#                p.start()
#                processes.append(p)
#            for p in processes:
#                p.join()
#            while not q.empty():
#                self.members[counter].fitness = q.get()
#                counter += 1
        fitnesses = [member.fitness for member in self.members]
        fitnesses.sort()
        return fitnesses

    def cull(self):
        self.members.sort(key=lambda x: x.fitness)
        self.members = self.members[self.replacement_number:] #cull the population

    def breed(self):
        hat = Hat(self.members)
        children = []
        for i in range(self.replacement_number):
            current_member = hat.pull()
            child = Member(self)
            child.crossover(current_member, self.get_random_other_member(current_member))
            child.mutate()
            children.append(child)
        #print len(children)
        self.members += children

    def get_random_other_member(self, to_ignore):
        """ returns a random member of the population other than the member specified
        """
        members = [member for member in self.members if member != to_ignore]
        choice = random.choice(members)
        return choice
        
class Member:

    def RandomWeight(self):
        return random.random()*10 - 5

    def __init__(self, population):
        self.population = population
        self.ann = Network(population.num_input, population.num_hidden, population.num_output)
        self.weights = [ 0 for x in self.ann.allConnections ]
        self.fitness = 0

    def randomize(self):
        self.weights = [ self.RandomWeight()  for _ in self.weights]

    def crossover(self, p1, p2):
        location1 = random.randint(0, len(self.weights)/2)
        location2 = location1 + len(self.weights)/2
        self.weights = p1.weights[:location1] + p2.weights[location1:location2] + p1.weights[location2:]

    def mutate(self):
        rate = self.population.mutation_rate * 100
        for i in range(len(self.weights)):
            rand_num = random.randint(0, 99)
            if rand_num < rate:
                self.weights[i] = self.RandomWeight()#TODO: this is gonna break. Decide weight range

    def calculate_fitness(self):#, q):
        phenotype = self.express()
        fitness = phenotype.width * phenotype.height #init fitness to max fitness
        for ideal_row, actual_row in zip(self.population.goal.grid, phenotype.grid):
            for ideal, actual in zip(ideal_row, actual_row):
                if ideal == 1 and actual == 0:
                    fitness -= 2
                elif ideal == 0 and actual == 1:
                    fitness -= 1
        self.fitness = fitness
        #q.put(fitness)

    def distanceToOtherGenotype(self,otherGenotype):
        '''return a metric of diversity based upon edit distance'''
        distance = 0
        for my,your in zip(self.weights,otherGenotype.weights):
            #print my,your
            distance += (my - your) ** 2
        return distance


    def express(self):
        self.ann.allConnections = self.weights
        runner = AnnRunner(self.population.goal)
        return runner.run(self.ann, iterations=600, x=325, y=175)