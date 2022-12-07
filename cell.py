import pygame
from constants import *

class Cell():
    # object created for each cell in the grid
    def __init__(self, x_coord, y_coord, row,column):
        self.y_coord = y_coord
        self.x_coord = x_coord
        self.row = row
        self.column = column
        self.rect = pygame.Rect(self.x_coord, self.y_coord, CELL_SIZE, CELL_SIZE)
        self.is_clicked = None
        self.ship = None

    def cell_clicked(self):
        self.is_clicked = True
        return self.rect.center, self.ship



