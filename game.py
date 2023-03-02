import random

from pygame import SurfaceType, Surface

from defines import *
from ghost import Ghost
from position import Position
from tile import Tile
from player import Player


class Game:
    def __init__(self, screen : Surface | SurfaceType, font, player1 : Player, player2 : Player):
        self.player1 = player1
        self.player2 = player2
        self.screen = screen
        self.ghosts = self.generateGhosts()
        self.dimention = 5
        self.boardCorners = [0, self.dimention - 1, self.dimention * self.dimention - self.dimention, self.dimention * self.dimention - 1]
        self.board = self.generateBoard()
        self.currPlayer = player1
        self.font = font


    def generateBoard(self):
        board =  [
            [Tile(COLOR_BLUE_TILE), Tile(COLOR_RED_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_BLUE_TILE), Tile(COLOR_RED_TILE)],
            [Tile(COLOR_YELLOW_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_YELLOW_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_YELLOW_TILE)],
            [Tile(COLOR_RED_TILE), Tile(COLOR_BLUE_TILE), Tile(COLOR_RED_TILE), Tile(COLOR_BLUE_TILE),Tile(COLOR_NEUTRAL_TILE)],
            [Tile(COLOR_BLUE_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_YELLOW_TILE), Tile(COLOR_NEUTRAL_TILE),Tile(COLOR_RED_TILE)],
            [Tile(COLOR_YELLOW_TILE), Tile(COLOR_RED_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_BLUE_TILE),Tile(COLOR_YELLOW_TILE)]
        ]
        x = (self.screen.get_width() - self.dimention * TILEWIDTH) / 2
        y = (self.screen.get_height() - self.dimention * TILEHEIGHT) / 2
        for row in range(self.dimention):
            for col in range(self.dimention):
                board[row][col].setPos(Position(x + TILEWIDTH * col, y + TILEHEIGHT * row))
        return board
    def generateGhosts(self):
        ghosts = []
        i = 1
        j = 1
        possibleColors= [COLOR_RED_GHOST] * 3 + [COLOR_BLUE_GHOST] * 3 + [COLOR_YELLOW_GHOST] * 3
        for player in [self.player1, self.player2]:
            for color in possibleColors:
                ghosts.append(Ghost(color, player, Position(i,j)))
                i += 20
                j += 30
        return ghosts

    def drawGhosts(self):
        for ghost in self.ghosts:
            ghost.draw(self.screen)

    def drawPlayerTurn(self):
        self.currPlayer.draw(self.screen, self.font)

    def drawBoard(self):
        for row in range(self.dimention):
            for col in range(self.dimention):
                self.board[row][col].draw(self.screen)

    def draw(self):
        self.drawPlayerTurn()
        self.drawBoard()
        self.drawGhosts()
