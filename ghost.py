import pygame


class Ghost:
    def __init__(self, color, player):
        self.color = color
        self.player = player

    def __str__(self):
        return "player = " + str(self.player) + " | color = " + str(self.color)

    def draw(self, screen):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(30, 30, 60, 60))
