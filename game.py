import random

from pygame import SurfaceType, Surface

from defines import *
from ghost import Ghost
from portal import Portal
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
        self.currGhost : Ghost | int = 0
        self.font = font
        self.state = GameState.PICKING


    def generateBoard(self):
        board =  [
            [Tile(COLOR_BLUE_TILE), Tile(COLOR_RED_TILE), Tile(COLOR_RED_TILE, Portal("red")), Tile(COLOR_BLUE_TILE), Tile(COLOR_RED_TILE)],
            [Tile(COLOR_YELLOW_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_YELLOW_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_YELLOW_TILE)],
            [Tile(COLOR_RED_TILE), Tile(COLOR_BLUE_TILE), Tile(COLOR_RED_TILE), Tile(COLOR_BLUE_TILE),Tile(COLOR_YELLOW_TILE, Portal("yellow"))],
            [Tile(COLOR_BLUE_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_YELLOW_TILE), Tile(COLOR_NEUTRAL_TILE),Tile(COLOR_RED_TILE)],
            [Tile(COLOR_YELLOW_TILE), Tile(COLOR_RED_TILE), Tile(COLOR_BLUE_TILE, Portal("blue")), Tile(COLOR_BLUE_TILE),Tile(COLOR_YELLOW_TILE)]
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

        possibleColors= ["red"] * 3 + ["blue"] * 3 + ["yellow"] * 3
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
        picking = ""
        if self.state == GameState.PICKING:
            picking = " to pick a spot"
        self.currPlayer.draw(self.screen, self.font, picking)


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

    def possibleMoves(self, ghost : Ghost):
        row, col = ghost.position.x, ghost.position.y
        board_copy = [row[:] for row in self.board]
        possible_moves = []
        for drow, dcol in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < self.dimention and 0 <= new_col < self.dimention:
                new_tile = board_copy[new_row][new_col]
                if not new_tile.full and not new_tile.portal:
                    board_copy[row][col].full = False
                    board_copy[new_row][new_col].full = True
                    possible_moves.append((new_row, new_col))
        print("Possible moves:")
        for move in possible_moves:
            print("  ghost at index ({},{}) to index ({},{})".format(row, col, move[0], move[1]))
        return possible_moves
        '''
        print("Updated Board:")
        for row in board_copy:
            print([str(tile) for tile in row])
        print("\n")
        return board_copy
        '''

