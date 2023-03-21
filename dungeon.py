import pygame
from defines import *
from ghost import Ghost
from position import Position
from tile import Tile


class Dungeon:
    def __init__(self, position: Position):
        self.ghosts = []
        self.dungeonCoords = position
        self.generateTiles()

    def updateGhostPlace(self):
        for i in range(len(self.ghosts)):
            row = i // 6
            col = i % 6
            self.ghosts[i].setIndexandPos(Position(col, row), self.dungeonCoords)

    def addGhost(self, ghost: Ghost):
        self.ghosts.append(ghost)
        self.updateGhostPlace()

    def removeGhost(self, ghost: Ghost):
        self.ghosts.remove(ghost)
        self.updateGhostPlace()

    def draw(self, screen, index : Position | int = 0):
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                if index and index.y == row and index.x == col:
                    self.tiles[row][col].draw(screen, True)
                else:
                    self.tiles[row][col].draw(screen)


    def generateTiles(self):
        self.tiles = []
        for i in range(3):
            tileRow = []
            for j in range(6):
                tile = Tile(COLOR_DUNGEON_TILE)
                tile.setPos(
                    Position(self.dungeonCoords.x + j * TILEWIDTH, self.dungeonCoords.y + i * TILEHEIGHT))
                tileRow.append(tile)
            self.tiles.append(tileRow)
