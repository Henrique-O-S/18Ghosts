import pygame
from defines import *
from pygame.font import Font


class Player:
    def __init__(self, name, playerType):
        self.name = name
        self.playerType = playerType
        self.color = COLOR_NEUTRAL_TILE
    def __str__(self):
        return str(self.name)
    def draw(self, screen, font : Font):

        (textWidth, textHeight) = font.size(self.name)
        x = (WIDTH - textWidth) / 2
        y = HEIGHT / 9
        text_surface = font.render(self.name + '\'s turn', False, COLOR_FONT, COLOR_FONT_BACKGROUND)
        screen.blit(text_surface, (x, y))