from enum import Enum
class Color(Enum):
    RED = 1
    BLUE = 2
    YELLOW = 3

Color = Enum('Color', ['RED', 'BLUE', 'YELLOW'])

class PlayerType(Enum):
    PLAYER = 1
    BOT = 2

PlayerType = Enum('PlayerType', ['PLAYER', 'BOT'])

REDCOLORTILE = (255, 0, 0)
REDCOLORGHOST = (255, 0, 0)
BLUECOLORTILE = (0, 0, 255)
BLUECOLORGHOST = (255, 0, 0)
YELLOWCOLORTILE = (255, 0, 0)
YELLOWCOLORGHOST = (255, 0, 0)
NEUTRALCOLORTILE = (100,100,100)