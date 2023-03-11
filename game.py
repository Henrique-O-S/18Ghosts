import random

from pygame import SurfaceType, Surface

from defines import *
from ghost import Ghost
from position import Position
from tile import Tile
from player import Player
import time


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
        self.state = GameState.PICKING


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

        self.boardCoords = Position(x,y)


        for row in range(self.dimention):
            for col in range(self.dimention):
                board[row][col].setPos(Position(x + TILEWIDTH * col, y + TILEHEIGHT * row))
        return board
    def generateGhosts(self):
        ghosts = []

        possibleColors= [COLOR_RED_GHOST] * 3 + [COLOR_BLUE_GHOST] * 3 + [COLOR_YELLOW_GHOST] * 3
        for player in [self.player1, self.player2]:
            for color in possibleColors:
                ghosts.append(Ghost(color, player))

        return ghosts

    def chooseGhostTile(self, click : Position):
        if click.x >= self.boardCoords.x and click.x <= self.boardCoords.x + self.dimention * TILEWIDTH and click.y >= self.boardCoords.y and click.y <= self.boardCoords.y + self.dimention * TILEHEIGHT:
            indexY = int((click.y - self.boardCoords.y) // TILEHEIGHT)
            indexX = (int(click.x - self.boardCoords.x) // TILEWIDTH)
            tile = self.board[indexY][indexX]
            if not tile.full:
                for ghost in self.ghosts:
                    if not ghost.chosen:
                        if compareGhostTileColor(ghost, tile) and ghost.player == self.currPlayer:
                            tile.full = True
                            ghost.setIndexandPos(Position(indexY, indexX), Position(indexX * TILEWIDTH + self.boardCoords.x, indexY * TILEHEIGHT + self.boardCoords.y))
                            self.switchPlayers()
                            self.updateState()

                            return

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

    def switchPlayers(self):
        if self.currPlayer == self.player1:
            self.currPlayer = self.player2
        else:
            self.currPlayer = self.player1

    def updateState(self):
        if self.state == GameState.PICKING:
            for ghost in self.ghosts:
                if not ghost.chosen:
                    return
            self.state = GameState.PLAYING
