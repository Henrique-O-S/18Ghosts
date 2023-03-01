import pygame
from defines import *

class Player:
    def __init__(self, name, playerType):
        self.name = name
        self.playerType = playerType
        self.color = NEUTRALCOLORTILE
    def __str__(self):
        return str(self.name)
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(30, 30, 60, 60))