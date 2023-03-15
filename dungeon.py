import pygame
from defines import *
from ghost import Ghost
from position import Position
from tile import Tile


class Dungeon:
    def __init__(self, position : Position):
        self.ghosts = []
        self.generateTiles(position)


    def addGhost(self, ghost : Ghost):
        self.ghosts.append(ghost)

    def removeGhost(self, ghost : Ghost):
        self.ghosts.remove(ghost)

    def draw(self, screen):
        for row in self.tiles:
            for tile in row:
                tile.draw(screen)

    def generateTiles(self, position : Position):
        self.tiles = []
        for i in range(3):
            tileRow = []
            for j in range(6):
                tile = Tile(COLOR_DUNGEON_TILE)
                tile.setPos(Position(position.x + j * TILEWIDTH, position.y + TILEHEIGHT + i * TILEHEIGHT))
                tileRow.append(tile)
            self.tiles.append(tileRow)