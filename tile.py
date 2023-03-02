import pygame
from defines import *
from position import Position
class Tile:
    def __init__(self, color):
        self.color = color
        self.full = False
    def __str__(self):
        return str(self.color) + " tile"

    def setPos(self, position : Position):
        self.position = position
    def draw(self, screen):
        x = self.position.x
        y = self.position.y
        pygame.draw.rect(screen, self.color, pygame.Rect(x, y, TILEWIDTH, TILEHEIGHT))
        pygame.draw.rect(screen, COLOR_TILE_BORDER, pygame.Rect(x, y, TILEWIDTH, TILEHEIGHT), TILEBORDERWIDTH)

