import random

from pygame import SurfaceType, Surface

from defines import *
from ghost import Ghost
from tile import Tile
from player import Player


class Game:
    def __init__(self, screen : Surface | SurfaceType, font, player1 : Player, player2 : Player):
        self.player1 = player1
        self.player2 = player2
        self.dimention = 5
        self.boardCorners = [0, self.dimention - 1, self.dimention * self.dimention - self.dimention, self.dimention * self.dimention - 1]
        self.board = self.generateBoard()
        self.screen = screen
        self.currPlayer = player1
        self.font = font


    def generateBoard(self):
        '''auxBoard = []
        possibleColors= [COLOR_RED_TILE] * 6 + [COLOR_BLUE_TILE] * 6 + [COLOR_YELLOW_TILE] * 6 + [COLOR_NEUTRAL_TILE] * 3
        for tile in range(self.dimention * self.dimention):
            if tile in self.boardCorners:
                auxBoard += [Tile(COLOR_NEUTRAL_TILE)]
            else:
                selectedColor = random.choice(possibleColors)
                auxBoard += [Tile(selectedColor)]
                possibleColors.remove(selectedColor)
        return [auxBoard[i * self.dimention:(i + 1) * self.dimention] for i in range((len(auxBoard) + self.dimention - 1) // self.dimention)]
    '''
        return [
            [Tile(COLOR_BLUE_TILE), Tile(COLOR_RED_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_BLUE_TILE), Tile(COLOR_RED_TILE)],
            [Tile(COLOR_YELLOW_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_YELLOW_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_YELLOW_TILE)],
            [Tile(COLOR_RED_TILE), Tile(COLOR_BLUE_TILE), Tile(COLOR_RED_TILE), Tile(COLOR_BLUE_TILE),Tile(COLOR_NEUTRAL_TILE)],
            [Tile(COLOR_BLUE_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_YELLOW_TILE), Tile(COLOR_NEUTRAL_TILE),Tile(COLOR_RED_TILE)],
            [Tile(COLOR_YELLOW_TILE), Tile(COLOR_RED_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_BLUE_TILE),Tile(COLOR_YELLOW_TILE)]
        ]
    def drawPlayerTurn(self):
        self.currPlayer.draw(self.screen, self.font)

    def drawBoard(self):
        x = (self.screen.get_width() - self.dimention * TILEWIDTH) / 2
        y = (self.screen.get_height() - self.dimention * TILEHEIGHT) / 2
        for row in range(self.dimention):
            for col in range(self.dimention):
                self.board[row][col].draw(self.screen, x + TILEWIDTH * col, y + TILEHEIGHT * row)

    def draw(self):
        self.drawPlayerTurn()
        self.drawBoard()
