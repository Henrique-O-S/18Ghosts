from enum import Enum

# --------------------------------------Game Definitions----------------------------------------

PLAYER_1_BOT_TYPE = 0  # 0 for minimax, 1 for mcts
PLAYER_2_BOT_TYPE = 0  # 0 for minimax, 1 for mcts

PLAYER_1_DEPTH = 2
PLAYER_2_DEPTH = 2

PLAYER_1_DIFFICULTY = 3  # 3 for hard, 2 for medium, 1 for easy
PLAYER_2_DIFFICULTY = 3  # 3 for hard, 2 for medium, 1 for easy

MCTS_N_ITERATIONS = 6

# ----------------------------------------------------------------------------------------------

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


PORTAL_DIR = {0: "UP", 1: "RIGHT", 2: "DOWN", 3: "LEFT"}

# COLOR
COLOR_RED_TILE = (251, 79, 79)
# COLOR_RED_GHOST = (255, 0, 0)
COLOR_BLUE_TILE = (108, 192, 229)
# COLOR_BLUE_GHOST = (0, 0, 255)
COLOR_YELLOW_TILE = (251, 201, 61)
# COLOR_YELLOW_GHOST = (255, 255, 0)
COLOR_NEUTRAL_TILE = (100, 100, 100)

COLOR_DUNGEON_TILE = (165, 42, 42)

COLOR_BACKGROUND = (185, 180, 158)
COLOR_TILE_BORDER = (0, 0, 0)
TILEBORDERWIDTH = 1

RP_X = 2
RP_Y = 0
YP_X = 4
YP_Y = 2
BP_X = 2
BP_Y = 4

RS_X = 1
RS_Y = 4
BS_X = 0
BS_Y = 0
YS_X = 0
YS_Y = 4

fps = 60

WIDTH = 1300
HEIGHT = 600
TILEWIDTH = 90
TILEHEIGHT = 90

COLOR_FONT = (0, 0, 0)
COLOR_FONT_BACKGROUND = (255, 255, 255)

def clickSquareColision(clickPosition, elPosition, width, height):
    return clickPosition.x > elPosition.x and clickPosition.x < elPosition.x + width and clickPosition.y > elPosition.y and clickPosition.y < elPosition.y + height


def compareGhostTileColor(ghost, tile):
    return (ghost.color == "blue" and tile.color == COLOR_BLUE_TILE) or (
                ghost.color == "yellow" and tile.color == COLOR_YELLOW_TILE) or (
                ghost.color == "red" and tile.color == COLOR_RED_TILE)
