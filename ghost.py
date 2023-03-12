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

    def __str__(self):
        return "player = " + str(self.player) + " | color = " + str(self.color)

    def draw(self, screen):
        if self.chosen:
            screen.blit(self.image, (self.position.x, self.position.y))

    def setIndexandPos(self, index : Position, position : Position):
        self.index = index
        self.position = position
        self.chosen = True

    def loadImage(self):
        return pygame.transform.scale(pygame.image.load('images/' + self.color + '_ghost_' + self.player.name[-1] + '.png').convert_alpha(), (90, 90))
