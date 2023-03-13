import pygame
from defines import *
from portal import Portal
from position import Position
class Tile:
    def __init__(self, color, portal : Portal | int = 0):
        self.color = color
        self.full = False
        self.portal = portal
    def __str__(self):
        return str(self.color) + " tile"

    def setPos(self, position : Position):
        self.position = position
        if self.portal:
            self.portal.setPos(position)
    def draw(self, screen, picked = False):
        x = self.position.x
        y = self.position.y
        pygame.draw.rect(screen, self.color, pygame.Rect(x, y, TILEWIDTH, TILEHEIGHT))
        if picked:
            pygame.draw.rect(screen, COLOR_TILE_BORDER, pygame.Rect(x, y, TILEWIDTH, TILEHEIGHT), 3 * TILEBORDERWIDTH)
        else:
            pygame.draw.rect(screen, COLOR_TILE_BORDER, pygame.Rect(x, y, TILEWIDTH, TILEHEIGHT), TILEBORDERWIDTH)

        if self.portal:
            self.portal.draw(screen)

