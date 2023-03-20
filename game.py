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
        self.dimension = 5
        self.boardCorners = [0, self.dimension - 1, self.dimension * self.dimension - self.dimension, self.dimension * self.dimension - 1]
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
        x = (self.screen.get_width() - self.dimension * TILEWIDTH) / 1.3
        y = (self.screen.get_height() - self.dimension * TILEHEIGHT) / 5

        self.boardCoords = Position(x,y)

        self.dungeon = Dungeon(Position(x - 7 * TILEWIDTH, y + TILEHEIGHT))


        for row in range(self.dimension):
            for col in range(self.dimension):
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

                            ghost.setIndexandPos(Position(indexes.x, indexes.y), self.boardCoords)

                            self.switchPlayers()
                            self.updateState()

                            return

    def drawGhosts(self):
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        for ghost in self.dungeon.ghosts:
            ghost.draw(self.screen)

    def drawPlayerTurn(self):
        picking = ""
        if self.state == GameState.PICKING:
            picking = " to pick a spot"
        self.currPlayer.draw(self.screen, self.font, picking)


    def drawBoard(self):
        for row in range(self.dimension):
            for col in range(self.dimension):
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
        row, col = ghost.index.y, ghost.index.x
        possible_moves = []
        for dcol, drow in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < self.dimension and 0 <= new_col < self.dimension:
                if self.checkTile(ghost, new_row, new_col):
                    possible_moves.append(Position(new_col, new_row))
        print("Possible moves:")
        for move in possible_moves:
            print("  ghost at index ({},{}) to index ({},{})".format(col, row, move.x, move.y))
        return possible_moves

    def checkTile(self, ghost: Ghost, new_row, new_col):
        if self.board[new_row][new_col].portal:
            return False
        for g in self.ghosts:
            if g.index.x == new_col and g.index.y == new_row and g.color == ghost.color:
                return False
        return True

    def coordsToIndexBoard(self, click : Position):
        if self.clickInsideBoard(click):
            indexY = int((click.y - self.boardCoords.y) // TILEHEIGHT)
            indexX = (int(click.x - self.boardCoords.x) // TILEWIDTH)
            return Position(indexX, indexY)

    def coordsToIndexDungeon(self, click: Position):
        if self.clickInsideDungeon(click):
            indexY = int((click.y - self.dungeon.dungeonCoords.y) // TILEHEIGHT)
            indexX = (int(click.x - self.dungeon.dungeonCoords.x) // TILEWIDTH)
            return Position(indexX, indexY)

    def clickInsideBoard(self, click : Position):
        return click.x >= self.boardCoords.x and click.x <= self.boardCoords.x + self.dimension * TILEWIDTH and click.y >= self.boardCoords.y and click.y <= self.boardCoords.y + self.dimension * TILEHEIGHT

    def clickInsideDungeon(self, click : Position):
        return click.x >= self.dungeon.dungeonCoords.x and click.x <= self.dungeon.dungeonCoords.x + 6 * TILEWIDTH and click.y >= self.dungeon.dungeonCoords.y and click.y <= self.dungeon.dungeonCoords.y + 3 * TILEHEIGHT

    def moveCurrGhost(self, index : Position):
        print(index.x, index.y)
        if index in self.possibleMoves(self.currGhost): # move is possible
            print("move is possible")
            for i in range(len(self.ghosts)):
                if self.ghosts[i] == self.currGhost:
                    for j in range(len(self.ghosts)):
                        if self.ghosts[j].index == index: # going to this (another) ghost's tile
                            if self.ghosts[i].winsFight(self.ghosts[j]):
                                print("ganhou")
                                self.dungeon.addGhost(self.ghosts[j])
                                self.ghosts[i].setIndexandPos(index, self.boardCoords)
                                print("novo index attGhost", index.x, index.y)
                                self.currGhost = 0
                                if self.ghosts[j].color == "red":
                                    self.board[RP_Y][RP_X].portal.rotate()
                                elif self.ghosts[j].color == "blue":
                                    self.board[BP_Y][BP_X].portal.rotate()
                                else:
                                    self.board[YP_Y][YP_X].portal.rotate()
                                self.ghosts.remove(self.ghosts[j])
                                self.ghostEscape()
                                self.switchPlayers()
                                return
                            else:
                                print("perdeu")
                                self.dungeon.addGhost(self.ghosts[i])
                                if self.ghosts[i].color == "red":
                                    self.board[RP_Y][RP_X].portal.rotate()
                                elif self.ghosts[i].color == "blue":
                                    self.board[BP_Y][BP_X].portal.rotate()
                                else:
                                    self.board[YP_Y][YP_X].portal.rotate()

                                self.ghosts.remove(self.ghosts[i])
                                self.currGhost = 0
                                self.ghostEscape()
                                self.switchPlayers()
                                return

            for i in range(len(self.ghosts)):
                if self.ghosts[i] == self.currGhost:
                    print("vazio")
                    self.ghosts[i].setIndexandPos(index, self.boardCoords)
                    print("novo index attGhost", self.ghosts[i].index.x, self.ghosts[i].index.y)
                    self.currGhost = 0
                    self.switchPlayers()
                    return

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
            self.moveCurrGhost(ghostIndexes)
            self.ghostEscape()

    def findGhostID(self, index : Position):
        for i in range(len(self.ghosts)):
            if self.ghosts[i].index.x == index.x and self.ghosts[i].index.y == index.y:
                return i
        return -1

    def ghostEscape(self):
        if (self.redEscape()):
            self.currPlayer.colors_cleared["red"] += 1
            return True
        elif (self.yellowEscape()):
            self.currPlayer.colors_cleared["yellow"] += 1
            return True
        elif (self.blueEscape()):
            self.currPlayer.colors_cleared["blue"] += 1
            return True   
        return False

    def redEscape(self):
        dir = self.board[RP_Y][RP_X].portal.direction
        if PORTAL_DIR[dir] == "LEFT":
            id = self.findGhostID(Position(RP_X - 1, RP_Y))
            if id != -1 and self.ghosts[id].color == "red":
                self.ghosts.remove(self.ghosts[id])
                return True
        elif PORTAL_DIR[dir] == "DOWN":
            id = self.findGhostID(Position(RP_X, RP_Y + 1))
            if id != -1 and self.ghosts[id].color == "red":
                self.ghosts.remove(self.ghosts[id])
                return True
        elif PORTAL_DIR[dir] == "RIGHT":
            id = self.findGhostID(Position(RP_X + 1, RP_Y))
            if id != -1 and self.ghosts[id].color == "red":
                self.ghosts.remove(self.ghosts[id])
                return True 
        return False
    
    def yellowEscape(self):
        dir = self.board[YP_Y][YP_X].portal.direction
        if PORTAL_DIR[dir] == "UP":
            id = self.findGhostID(Position(YP_X, YP_Y - 1))
            if id != -1 and self.ghosts[id].color == "yellow":
                self.ghosts.remove(self.ghosts[id])
                return True
        elif PORTAL_DIR[dir] == "LEFT":
            id = self.findGhostID(Position(YP_X - 1, YP_Y))
            if id != -1 and self.ghosts[id].color == "yellow":
                self.ghosts.remove(self.ghosts[id])
                return True
        elif PORTAL_DIR[dir] == "DOWN":
            id = self.findGhostID(Position(YP_X, YP_Y + 1))
            if id != -1 and self.ghosts[id].color == "yellow":
                self.ghosts.remove(self.ghosts[id])
                return True 
        return False
    
    def blueEscape(self):
        dir = self.board[BP_Y][BP_X].portal.direction
        if PORTAL_DIR[dir] == "LEFT":
            id = self.findGhostID(Position(BP_X - 1, BP_Y))
            if id != -1 and self.ghosts[id].color == "blue":
                self.ghosts.remove(self.ghosts[id])
                return True
        elif PORTAL_DIR[dir] == "UP":
            id = self.findGhostID(Position(BP_X, BP_Y - 1))
            if id != -1 and self.ghosts[id].color == "blue":
                self.ghosts.remove(self.ghosts[id])
                return True
        elif PORTAL_DIR[dir] == "RIGHT":
            id = self.findGhostID(Position(BP_X + 1, BP_Y))
            if id != -1 and self.ghosts[id].color == "blue":
                self.ghosts.remove(self.ghosts[id])
                return True 
        return False

    def manhattan_distances(self, player : Player):
        # returns the sum of manhattan distances from ghosts to their respective exits
        board = self.board

        total = 0

        for ghost in self.ghosts:
            if ghost.player == player:
                if ghost.color == 'red' and player.colors_cleared.get('red') == 0:
                    if self.board[RP_Y][RP_X].portal.direction == 0:
                        total += abs(ghost.index.x - self.board[RP_Y][RP_X].index.x + 1) + abs(ghost.index.y - self.board[RP_Y][RP_X].index.y)
                    elif self.board[RP_Y][RP_X].portal.direction == 1:
                        total += abs(ghost.index.x - self.board[RP_Y][RP_X].index.x + 1) + abs(ghost.index.y - self.board[RP_Y][RP_X].index.y)
                    elif self.board[RP_Y][RP_X].portal.direction == 2:
                        total += abs(ghost.index.x - self.board[RP_Y][RP_X].index.x) + abs(ghost.index.y - self.board[RP_Y][RP_X].index.y + 1)
                    else:
                        total += abs(ghost.index.x - self.board[RP_Y][RP_X].index.x - 1) + abs(ghost.index.y - self.board[RP_Y][RP_X].index.y)
                elif ghost.color == 'yellow' and player.colors_cleared.get('yellow') == 0:
                    if self.board[YP_Y][YP_X].portal.direction == 0:
                        total += abs(ghost.index.x - self.board[YP_Y][YP_X].index.x) + abs(ghost.index.y - self.board[YP_Y][YP_X].index.y - 1)
                    elif self.board[YP_Y][YP_X].portal.direction == 1:
                        total += abs(ghost.index.x - self.board[YP_Y][YP_X].index.x) + abs(ghost.index.y - self.board[YP_Y][YP_X].index.y + 1)
                    elif self.board[YP_Y][YP_X].portal.direction == 2:
                        total += abs(ghost.index.x - self.board[YP_Y][YP_X].index.x) + abs(ghost.index.y - self.board[YP_Y][YP_X].index.y + 1)
                    else:
                        total += abs(ghost.index.x - self.board[YP_Y][YP_X].index.x - 1) + abs(ghost.index.y - self.board[YP_Y][YP_X].index.y)
                elif ghost.color == 'blue' and player.colors_cleared.get('blue') == 0:
                    if self.board[BP_Y][BP_X].portal.direction == 0:
                        total += abs(ghost.index.x - self.board[BP_Y][BP_X].index.x) + abs(ghost.index.y - self.board[BP_Y][BP_X].index.y - 1)
                    elif self.board[BP_Y][BP_X].portal.direction == 1:
                        total += abs(ghost.index.x - self.board[BP_Y][BP_X].index.x + 1) + abs(ghost.index.y - self.board[BP_Y][BP_X].index.y)
                    elif self.board[BP_Y][BP_X].portal.direction == 2:
                        total += abs(ghost.index.x - self.board[BP_Y][BP_X].index.x - 1) + abs(ghost.index.y - self.board[BP_Y][BP_X].index.y)
                    else:
                        total += abs(ghost.index.x - self.board[BP_Y][BP_X].index.x - 1) + abs(ghost.index.y - self.board[BP_Y][BP_X].index.y)

        for ghost in self.dungeon():
            if ghost.player == player:
                if ghost.color == 'red' and player.colors_cleared.get('red') == 0:
                    total += 8
                elif ghost.color == 'yellow' and player.colors_cleared.get('yellow') == 0:
                    total += 8
                elif ghost.color == 'blue' and player.colors_cleared.get('blue') == 0:
                    total += 8

        return total

    def play_evaluation(self, player : Player):
        cost = self.manhattan_distances(self, player)
        for ghost in self.ghosts:
            if ghost.player != player:
                cost += 1
            elif ghost.player == player:
                cost += 1
                if ghost.player.colors_cleared.get(ghost.color) == 0:
                    for near_by_ghost in self.ghosts:
                        if near_by_ghost.player != player and near_by_ghost.winsFight(ghost) and (ghost.index.x - 1 <= near_by_ghost.index.x <= ghost.index.x + 1 and ghost.index.y - 1 <= near_by_ghost.index.y <= ghost.index.y + 1) and (near_by_ghost.index.x != ghost.index.x and near_by_ghost.index.y != ghost.index.y):
                            cost += 8
        for ghost in self.dungeon:
            if ghost.player == player:
                cost += 1

        return cost

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
