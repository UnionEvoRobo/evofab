from virtualprinter import VirtualPrinter
from camera import VisualCamera, Camera
from grid import Grid
from gridworld import GridWorld
from ann import Network
import pygame

import csv

camera_headers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
output_headers = ['x velocity', 'y velocity']

graycode = {
       0  : "00000",
       1  : "00001",
       2  : "00010",
       3  : "00011",
       4  : "00100",
       5  : "00101",
       6  : "00110",
       7  : "00111",
       8  : "01000",
       9  : "01001",
       10 : "01010",
       11 : "01011",
       12 : "01100",
       13 : "01101",
       14 : "01110",
       15 : "01111",
       16 : "10000",
       17 : "10001",
       18 : "10010",
       19 : "10011",
       20 : "10100",
       21 : "10101",
       22 : "10110",
       23 : "10111",
       24 : "11000",
       25 : "11001",
       26 : "11010",
       27 : "11011",
       28 : "11100",
       29 : "11101",
       30 : "11110",
       31 : "11111",
    }

class training_set_loader:

    def __init__(self, path):
        self.path = path

    def read(self):
        """ returns (camera_vals, x,y velocities) """

        with open(self.path, 'r') as to_read:
            reader = csv.reader(to_read)
            _ = reader.next()
            camera_vals = []
            velocities = []
            for row in reader:
                camera_vals.append(row[:len(camera_headers)])
                velocities.append(row[len(camera_headers):][0])
                velocities = [[int(x) for x in string] for string in velocities]
        return (
                [[float(x) for x in row] for row in camera_vals],
                velocities
                )

class ann_trainer:

    def __init__(self, ideal_grid):
        self.gridworld = GridWorld(ideal_grid.width, ideal_grid.height, ideal_grid.gridsize)
        self.gridworld.set_ideal_grid(ideal_grid)
        self.printer = VirtualPrinter(10, 10, 9, 1, pygame.color.Color("darkorange"), self.gridworld)
        self.camera = VisualCamera(self.gridworld, self.printer, 3)

        #gui stuff
        #pygame.init()
        #width = self.gridworld.width() * self.gridworld.gridsize()
        #height = self.gridworld.height() * self.gridworld.gridsize()
        #self.window = pygame.display.set_mode((width, height))

    def train(self, path_to_training_set):
        n = Network(9, 6, 10)
        loader = training_set_loader(path_to_training_set)
        n.inputs, n.targets = loader.read()
        n.test()
        n.train()
        n.test()

ideal_grid = Grid(scale=60, path='square.test')
trainer = ann_trainer(ideal_grid)
trainer.train('output.out')