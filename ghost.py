import pygame
from defines import *
from position import Position


class Ghost:
    def __init__(self, color, player, position : Position):
        self.color = color
        self.player = player
        self.image = self.loadImage()
        self.position = position

    def __str__(self):
        return "player = " + str(self.player) + " | color = " + str(self.color)

    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y))

    def loadImage(self):
        if self.color == COLOR_RED_GHOST:
            color = "red"
        elif self.color == COLOR_BLUE_GHOST:
            color = "blue"
        else:
            color = "yellow"
        return pygame.transform.scale(pygame.image.load('images/' + color + '_ghost_' + self.player.name[-1] + '.png').convert_alpha(), (90, 90))
