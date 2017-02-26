from complexity_ann_ga import CompPopulation 
#from phys_printer_genetic_algorithms import PhysPopulation
from grid import Grid
import datetime
import getopt
import sys
import os
import errno
import threading

helptext = 'ga_runner.py -v -d -t threadnum -o outputfolder -p serial_port -s sensor_port'

try:
    opts, args = getopt.getopt(sys.argv[1:], "vdt:o:p:s:k:z:c:", ["visual", "dumping", "threadnum=", "outputfolder=", "port=", "sensor_port=", "conveyor_port=", "z_port=", "camera=",]) 
except getopt.GetoptError:
    print helptext
    sys.exit()

is_visual = False
is_dumping = False
num_threads = 1
outputfolder = 'data/'
port = ''
sensor_port = ''
conveyor_port = ''
z_port = ''
camera = 0

for opt, arg in opts:
    if opt in ('-v', '--visual'):
        is_visual = True
    elif opt in ('-d', '--dumping'):
        is_dumping = True
    elif opt in ('-t', '--threadnum'):
        num_threads = int(arg)
    elif opt in ('-o', '--outputfolder'):
        outputfolder = arg
    elif opt in ('-p', '--port'):
        port = arg.strip()
    elif opt in ('-s', '--sensor_port'):
        sensor_port = arg.strip()
    elif opt in ('-k', '--conveyor_port'):
        conveyor_port = arg.strip()
    elif opt in ('-z', '--z_port'):
        z_port = arg.strip()
    elif opt in ('-c', '--camera'):
        camera = int(arg)

current_time = datetime.datetime.now()

param = {
        'pop_size' : 100,
        'mutation_rate' : 0.15,
        'mutation_range' : (-30, 30),
        'cull_num' : 80,
        'ann_input' : 9,
        'ann_hidden' : 75,
        'ann_output' : 5,
        'use_global_coordinates' : True,
        'nodes_per_coordinate' : 4,
        'cell_scale' : 5,
        'camera_grid_dimension': 3, #factor by which camera cells are bigger than grid cells. must be odd so that the camera aligns to the grid cells
        'camera_cell_scale': 13,
        'inputs' : ['worlds/v_big_BIG.test'],
        'world_dimension': 100,
        'random_seed' : int(current_time.strftime('%s')),
        'time' : current_time,
        'num_gens' : 100,
        'printer_runtime' : 50,
        'printer_pen_size' : 5,
#        'reward_for_correct' : 100,
#        'punishment_for_incorrect': 30,
        'crossover_rate': .5,
        'recur_mode': 3,
        'time_to_recur': 10
        }

if is_dumping:
    outputfolder = outputfolder.strip()
    o_outputfolder = outputfolder
    if num_threads > 1:
        outputfolder = outputfolder + '_!'
        for x in range(num_threads):
            outputfolder = outputfolder[:-2] + str(x) + '/'
            if not os.path.isdir(outputfolder):
                try:
                    os.makedirs(outputfolder)
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(outputfolder + 'TEST_INFO', 'w') as outputfile:
                for key, val in param.items():
                    outputfile.write(key + ' : ' + str(val) + '\n')
                for gridfile in param['inputs']:
                    outputfile.write('\n========================\n')
                    outputfile.write(gridfile + '\n\n')
                    with open(gridfile, 'r') as to_read:
                        for line in to_read:
                            outputfile.write(line)
                    outputfile.write('\n========================\n')
    else:
        if outputfolder[-1] != "/":
            outputfolder = outputfolder + "/"
        if not os.path.isdir(outputfolder):
            try:
                os.makedirs(outputfolder)
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(outputfolder + 'TEST_INFO', 'w') as outputfile:
            for key, val in param.items():
                outputfile.write(key + ' : ' + str(val) + '\n')
            for gridfile in param['inputs']:
                outputfile.write('\n========================\n')
                outputfile.write(gridfile + '\n\n')
                with open(gridfile, 'r') as to_read:
                    for line in to_read:
                        outputfile.write(line)
                outputfile.write('\n========================\n')



if port:
    pass
    #population = PhysPopulation(
    #        param['random_seed'],
    #        param['printer_runtime'],
    #        param['pop_size'],
    #        param['mutation_rate'],
    #        param['mutation_range'],
    #        param['crossover_rate'],
    #        param['cull_num'],
    #        param['ann_input'],
    #        param['ann_hidden'],
    #        param['ann_output'],
    #        port,
    #        sensor_port,
    #        conveyor_port,
    #        z_port,
    #        camera,
    #        outputfolder=outputfolder,
    #        is_visual=is_visual,
    #        dump_to_files=is_dumping,
    #        )
else:
    if num_threads > 1:
        class myThread(threading.Thread):
            def __init__(self, threadID, name):
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
            def run(self):
                print "Starting " + self.name
                population = CompPopulation(
                        param['random_seed'],
                        param['printer_runtime'],
                        param['pop_size'],
                        param['mutation_rate'],
                        param['mutation_range'],
                        param['crossover_rate'],
                        param['cull_num'],
                        param['ann_input'],
                        param['ann_hidden'],
                        param['ann_output'],
                        use_global_coordinates = param['use_global_coordinates'],
                        nodes_per_coordinate = param['nodes_per_coordinate'],
                        world_dimension = param['world_dimension'],
                        outputfolder=o_outputfolder + str(self.threadID) + '/',
                        is_visual=is_visual,
                        dump_to_files=is_dumping,
                        cell_size = param['cell_scale'],
                        camera_grid_dimension = param['camera_grid_dimension'],
                        camera_cell_size = param['camera_cell_scale'],
                        printer_pen_size=param['printer_pen_size'],
                        recur = param['recur_mode'],
                        )
                print cur_thread
                population.iterate(param['num_gens'])
                print "Exiting " + self.name
        threads = []
        for cur_thread in range(num_threads):
            threads.append(myThread(cur_thread, "Thread " + str(cur_thread)))
        for thread in threads:
            thread.start()
        print 'exiting main thread'
    else:
        population = CompPopulation(
                param['random_seed'],
                param['printer_runtime'],
                param['pop_size'],
                param['mutation_rate'],
                param['mutation_range'],
                param['crossover_rate'],
                param['cull_num'],
                param['ann_input'],
                param['ann_hidden'],
                param['ann_output'],
                use_global_coordinates = param['use_global_coordinates'],
                nodes_per_coordinate = param['nodes_per_coordinate'],
                world_dimension = param['world_dimension'],
                outputfolder=outputfolder,
                is_visual=is_visual,
                dump_to_files=is_dumping,
                cell_size = param['cell_scale'],
                camera_grid_dimension = param['camera_grid_dimension'],
                camera_cell_size = param['camera_cell_scale'],
                printer_pen_size=param['printer_pen_size'],
                recur = param['recur_mode'],
                )
        population.iterate(param['num_gens'], num_threads)
