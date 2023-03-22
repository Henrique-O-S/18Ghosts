import pygame

from defines import *
from position import Position

class Ghost:
    def __init__(self, color, player):
        self.color = color
        self.player = player
        self.chosen = False
        self.placed = False

    def __eq__(self, other):
        return self.color == other.color and self.player == other.player and self.index == other.index and self.position == other.position
    
    def __str__(self):
        return "player = " + str(self.player) + " | color = " + str(self.color)

    def draw(self, screen):
        image = pygame.transform.scale(pygame.image.load('images/' + self.color + '_ghost_' + self.player.name[-1] + '.png').convert_alpha(), (80, 80))
        if self.chosen:
            screen.blit(image, (self.position.x, self.position.y))

    def setIndex(self, index : Position):
        self.index = index
        self.chosen = True

    def setPos(self, coords: Position):
        self.position = Position(coords.x + self.index.x * TILEWIDTH, coords.y + self.index.y * TILEHEIGHT)

    def winsFight(self, defGhost):
        if self.color == "red":
            return defGhost.color == "blue"
        if self.color == "blue":
            return defGhost.color == "yellow"
        if self.color == "yellow":
            return defGhost.color == "red"
