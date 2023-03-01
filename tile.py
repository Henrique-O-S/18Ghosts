import pygame

class Tile:
    def __init__(self, color):
        self.color = color
    def __str__(self):
        return str(self.color) + " tile"

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(30, 30, 60, 60))
