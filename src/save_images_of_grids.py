import os
from grid import Grid
from gui_gridworld import GuiGridWorld
import pygame
import time

def view():
    for f in os.listdir("worlds/canonical_inputs"):
        if f.endswith(".test"):
            f = "worlds/canonical_inputs/" + f
            grid = Grid(scale = 15, path = f)
            gridworld = GuiGridWorld(grid.width, grid.height, grid.gridsize)
            gridworld.grid = grid

            #some pygame trash to get an image of the input grid
            width = gridworld.width() * gridworld.gridsize()
            height = gridworld.height() * gridworld.gridsize()
            window = pygame.display.set_mode((width, height))
            pygame.init()

            gridworld.draw(window)
            pygame.display.update()
            pygame.image.save(window, f.split(".")[0]+".png")

if __name__ == "__main__":
    view()
