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
        if self.clickInsideBoard(click):
            indexes = self.coordsToIndexBoard(click)
            rowIndex = indexes.x
            colIndex = indexes.y
            tile = self.board[rowIndex][colIndex]
            if not (tile.full or tile.portal):
                for ghost in self.ghosts:
                    if not ghost.chosen:
                        if compareGhostTileColor(ghost, tile) and ghost.player == self.currPlayer:
                            tile.full = True
                            ghost.setIndexandPos(Position(rowIndex, colIndex), Position(colIndex * TILEWIDTH + self.boardCoords.x, rowIndex * TILEHEIGHT + self.boardCoords.y))
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
                if self.currGhost and self.currGhost.index.y == col and self.currGhost.index.x == row:
                    self.board[row][col].draw(self.screen, True)
                else:
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
        row, col = ghost.position.y, ghost.position.x
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

    def coordsToIndexBoard(self, click : Position):
        if self.clickInsideBoard(click):
            indexY = int((click.y - self.boardCoords.y) // TILEHEIGHT)
            indexX = (int(click.x - self.boardCoords.x) // TILEWIDTH)
            return Position(indexY, indexX)

    def clickInsideBoard(self, click : Position):
        return click.x >= self.boardCoords.x and click.x <= self.boardCoords.x + self.dimention * TILEWIDTH and click.y >= self.boardCoords.y and click.y <= self.boardCoords.y + self.dimention * TILEHEIGHT

    def moveCurrGhost(self, index : Position):
        if [index.y, index.x] in self.possibleMoves(self.currGhost): # move is possible
            for ghost in self.ghosts:
                if ghost.index == index: # going to this (another) ghost's tile
                    if self.currGhost.winsFight(ghost):
                        ghost.inDungeon = True
                        self.currGhost.index = index
                        self.currGhost = 0
                    else:
                        self.currGhost.inDungeon = True
                        self.currGhost = 0
                    return

            self.currGhost.index = index
            self.currGhost = 0

    def selectGhost(self, click : Position):
        if self.clickInsideBoard(click):
            ghostIndexes = self.coordsToIndexBoard(click)
            if self.currGhost and self.currGhost.index == ghostIndexes: #clicked on selected ghost --> stop selecting it
                self.currGhost = 0
                return
            for ghost in self.ghosts:
                if ghost.index == ghostIndexes: # ghost that player clicked
                    if self.currGhost: # if another one is selected
                        self.moveCurrGhost(ghost.index)
                    elif ghost.player == self.currPlayer:
                        self.currGhost = ghost
                    return





