import pygame
from defines import *
class Tile:
    def __init__(self, color):
        self.color = color
    def __str__(self):
        return str(self.color) + " tile"

    def draw(self, screen, x, y):
        pygame.draw.rect(screen, self.color, pygame.Rect(x, y, TILEWIDTH, TILEHEIGHT))
        pygame.draw.rect(screen, COLOR_TILE_BORDER, pygame.Rect(x, y, TILEWIDTH, TILEHEIGHT), TILEBORDERWIDTH)

