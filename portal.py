import pygame
from defines import *
from position import Position
class Portal:
    def __init__(self, color):
        self.color = color
        print(color)
        self.setDirection()
        self.image = self.loadImage()

    def __str__(self):
        return str(self.color) + " portal"

    def setPos(self, position : Position):
        self.position = position

    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y))

    def setDirection(self):
        if self.color == "red":
            self.direction = 0
        elif self.color == "blue":
            self.direction = 2
        else:
            self.direction = 1

    def rotate(self):
        self.direction = (self.direction + 1) % 4

    def loadImage(self):
        print(self.direction)
        return pygame.transform.scale(pygame.image.load('images/portal/' + self.color + '/' + PORTAL_DIR.get(self.direction) + '.png').convert_alpha(), (90, 90))