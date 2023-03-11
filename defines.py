from enum import Enum



class Color(Enum):
    RED = 1
    BLUE = 2
    YELLOW = 3


class PlayerType(Enum):
    PLAYER = 1
    BOT = 2

class GameState(Enum):
    PICKING = 1
    PLAYING = 2
    OVER = 3

# COLOR
COLOR_RED_TILE = (251, 79, 79)
COLOR_RED_GHOST = (255, 0, 0)
COLOR_BLUE_TILE = (108, 192, 229)
COLOR_BLUE_GHOST = (0, 0, 255)
COLOR_YELLOW_TILE = (251, 201, 61)
COLOR_YELLOW_GHOST = (255, 255, 0)
COLOR_NEUTRAL_TILE = (100, 100, 100)

COLOR_BACKGROUND = (185, 180, 158)
COLOR_TILE_BORDER = (0, 0, 0)
TILEBORDERWIDTH = 1


fps = 60

WIDTH = 1400
HEIGHT = 1000
TILEWIDTH = 120
TILEHEIGHT = 120

COLOR_FONT = (0,0,0)
COLOR_FONT_BACKGROUND = (255,255,255)

def clickSquareColision(clickPosition, elPosition, width, height):
    return clickPosition.x > elPosition.x and clickPosition.x < elPosition.x + width and clickPosition.y > elPosition.y and clickPosition.y < elPosition.y + height

def compareGhostTileColor(ghost, tile):
    return (ghost.color == COLOR_BLUE_GHOST and tile.color == COLOR_BLUE_TILE) or (ghost.color == COLOR_YELLOW_GHOST and tile.color == COLOR_YELLOW_TILE) or (ghost.color == COLOR_RED_GHOST and tile.color == COLOR_RED_TILE)