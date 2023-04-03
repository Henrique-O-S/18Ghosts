from pygame.font import Font

from defines import *

class Player:
    def __init__(self, name):
        self.name = name
        self.color = COLOR_NEUTRAL_TILE
        self.colors_cleared = {'red': 0, 'yellow': 0, 'blue': 0}
        
    def __str__(self):
        return str(self.name)
        