import random

from pygame import SurfaceType, Surface

from defines import *
from dungeon import Dungeon
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
        x = (self.screen.get_width() - self.dimention * TILEWIDTH) / 1.3
        y = (self.screen.get_height() - self.dimention * TILEHEIGHT) / 5

        self.boardCoords = Position(x,y)
        self.dungeon = Dungeon(Position(x - 7 * TILEWIDTH, y))


        for row in range(self.dimention):
            for col in range(self.dimention):
                board[row][col].setPos(Position(x + TILEWIDTH * col, y + TILEHEIGHT * row))
                board[row][col].setIndex(Position(col, row))

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
            tile = self.board[indexes.y][indexes.x]
            if not (tile.full or tile.portal):
                for ghost in self.ghosts:
                    if not ghost.chosen:
                        if compareGhostTileColor(ghost, tile) and ghost.player == self.currPlayer:
                            tile.full = True
                            ghost.setIndexandPos(Position(indexes.x, indexes.y), Position(indexes.x * TILEWIDTH + self.boardCoords.x, indexes.y * TILEHEIGHT + self.boardCoords.y))
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
                if self.currGhost and self.currGhost.index.y == row and self.currGhost.index.x == col:
                    self.board[row][col].draw(self.screen, True)
                else:
                    self.board[row][col].draw(self.screen)

    def drawDungeon(self):
        self.dungeon.draw(self.screen)

    def draw(self):
        self.drawPlayerTurn()
        self.drawBoard()
        self.drawDungeon()
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
        row, col = ghost.index.x, ghost.index.y
        board_copy = [row[:] for row in self.board]
        possible_moves = []
        for drow, dcol in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < self.dimention and 0 <= new_col < self.dimention:
                if self.checkTile(ghost, new_row, new_col):
                    possible_moves.append((new_row, new_col))
        print("Possible moves:")
        for move in possible_moves:
            print("  ghost at index ({},{}) to index ({},{})".format(row, col, move[0], move[1]))
        return possible_moves

    def checkTile(self, ghost: Ghost, new_row, new_col):
        if self.board[new_row][new_col].portal:
            return False
        for g in self.ghosts:
            if g.index.x == new_col and g.index.y == new_row and g.color == ghost.color:
                return False
        return True

    def execute_random_move(self):
        playerGhosts = [ghost for ghost in self.ghosts if ghost.player == self.currPlayer]
        ghost = random.choice(playerGhosts)
        move = random.choice(self.possibleMoves(ghost))
        self.currGhost = ghost
        self.moveCurrGhost(Position(move[1], move[0]))

    def execute_minimax_move(evaluate_func, depth):
        return True

    def minimax(state, depth, alpha, beta, maximizing, player, evaluate_func):
        return True


    def coordsToIndexBoard(self, click : Position):
        if self.clickInsideBoard(click):
            indexY = int((click.y - self.boardCoords.y) // TILEHEIGHT)
            indexX = (int(click.x - self.boardCoords.x) // TILEWIDTH)
            return Position(indexX, indexY)

    def clickInsideBoard(self, click : Position):
        return click.x >= self.boardCoords.x and click.x <= self.boardCoords.x + self.dimention * TILEWIDTH and click.y >= self.boardCoords.y and click.y <= self.boardCoords.y + self.dimention * TILEHEIGHT

    def moveCurrGhost(self, index : Position):
        print(index.x, index.y)
        if [index.x, index.y] in self.possibleMoves(self.currGhost): # move is possible
            for ghost in self.ghosts:
                if ghost.index == index and not ghost.inDungeon: # going to this (another) ghost's tile
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
                    print(ghost.index.x, ghost.index.y)
                    if self.currGhost: # if another one is selected
                        self.moveCurrGhost(ghost.index)
                    elif ghost.player == self.currPlayer:
                        self.currGhost = ghost
                    return

    def manhattan_distances(self, player : Player):
        # returns the sum of manhattan distances from ghosts to their respective exits
        board = self.board
        side = len(board)  # the size of the side of the board (only for square boards)

        total = 0

        for ghost in self.ghosts:
            if ghost.player == player:
                if ghost.color == 'red' and player.colors_cleared.get('red') == 0:
                    if self.portals.get('red').direction == 0:
                        total += abs(ghost.index.x - self.board[RP_Y][RP_X].index.x + 1) + abs(ghost.index.y - self.board[RP_Y][RP_X].index.y)
                    elif self.portals.get('red').direction == 1:
                        total += abs(ghost.index.x - self.board[RP_Y][RP_X].index.x + 1) + abs(ghost.index.y - self.board[RP_Y][RP_X].index.y)
                    elif self.portals.get('red').direction == 2:
                        total += abs(ghost.index.x - self.board[RP_Y][RP_X].index.x) + abs(ghost.index.y - self.board[RP_Y][RP_X].index.y + 1)
                    else:
                        total += abs(ghost.index.x - self.board[RP_Y][RP_X].index.x - 1) + abs(ghost.index.y - self.board[RP_Y][RP_X].index.y)
                elif ghost.color == 'yellow' and player.colors_cleared.get('yellow') == 0:
                    if self.portals.get('yellow').direction == 0:
                        total += abs(ghost.index.x - self.board[YP_Y][YP_X].index.x) + abs(ghost.index.y - self.board[YP_Y][YP_X].index.y - 1)
                    elif self.portals.get('yellow').direction == 1:
                        total += abs(ghost.index.x - self.board[YP_Y][YP_X].index.x) + abs(ghost.index.y - self.board[YP_Y][YP_X].index.y + 1)
                    elif self.portals.get('yellow').direction == 2:
                        total += abs(ghost.index.x - self.board[YP_Y][YP_X].index.x) + abs(ghost.index.y - self.board[YP_Y][YP_X].index.y + 1)
                    else:
                        total += abs(ghost.index.x - self.board[YP_Y][YP_X].index.x - 1) + abs(ghost.index.y - self.board[YP_Y][YP_X].index.y)
                elif ghost.color == 'blue' and player.colors_cleared.get('blue') == 0:
                    if self.portals.get('blue').direction == 0:
                        total += abs(ghost.index.x - self.board[BP_Y][BP_X].index.x) + abs(ghost.index.y - self.board[BP_Y][BP_X].index.y - 1)
                    elif self.portals.get('blue').direction == 1:
                        total += abs(ghost.index.x - self.board[BP_Y][BP_X].index.x + 1) + abs(ghost.index.y - self.board[BP_Y][BP_X].index.y)
                    elif self.portals.get('blue').direction == 2:
                        total += abs(ghost.index.x - self.board[BP_Y][BP_X].index.x - 1) + abs(ghost.index.y - self.board[BP_Y][BP_X].index.y)
                    else:
                        total += abs(ghost.index.x - self.board[BP_Y][BP_X].index.x - 1) + abs(ghost.index.y - self.board[BP_Y][BP_X].index.y)

        return total

    def play_evaluation(self, player : Player):
        cost = self.manhattan_distances(self, player)
        for ghost in self.ghosts():
            if ghost.player != player:
                cost += 1;
            else:
                for near_by_ghost in self.ghosts():
                    if near_by_ghost.player != player and near_by_ghost.winsFight(ghost) and (ghost.index.x - 1 <= near_by_ghost.index.x <= ghost.index.x + 1 and ghost.index.y - 1 <= near_by_ghost.index.y <= ghost.index.y + 1) and (near_by_ghost.index.x != ghost.index.x and near_by_ghost.index.y != ghost.index.y):
                        cost += 8

        return cost;
