import pygame
from defines import *
from position import Position
from tile import Tile


class Ghost:
    def __init__(self, color, player):
        self.color = color
        self.player = player
        self.image = self.loadImage()
        self.chosen = False

    def __eq__(self, other):
        return self.color == other.color and self.player == other.player and self.index == other.index and self.position == other.position
    def __str__(self):
        return "player = " + str(self.player) + " | color = " + str(self.color)

    def draw(self, screen):
        if self.chosen:
            screen.blit(self.image, (self.position.x, self.position.y))

    def setIndexandPos(self, index : Position, coords: Position):
        self.index = index
        self.position = Position(coords.x + index.x * TILEWIDTH, coords.y + index.y * TILEHEIGHT)
        self.chosen = True

    def loadImage(self):
        return pygame.transform.scale(pygame.image.load('images/' + self.color + '_ghost_' + self.player.name[-1] + '.png').convert_alpha(), (80, 80))

    def winsFight(self, defGhost):
        if self.color == "red":
            return defGhost.color == "blue"
        if self.color == "blue":
            return defGhost.color == "yellow"
        if self.color == "yellow":
            return defGhost.color == "red"
