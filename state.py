from copy import deepcopy

from defines import *
from tile import Tile
from portal import Portal
from position import Position
from dungeon import Dungeon
from ghost import Ghost
from player import Player

class State:
    def __init__(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.dimension = 5
        self.board = self.generate_board()
        self.ghosts = self.generate_ghosts()
        self.dungeon = Dungeon()
        self.currPlayer = self.player1
        self.currGhost : Ghost | int = 0
        self.gameState = GameState.PICKING
        
    def generate_board(self):
        board =  [
            [Tile(COLOR_BLUE_TILE), Tile(COLOR_RED_TILE), Tile(COLOR_RED_TILE, Portal("red")), Tile(COLOR_BLUE_TILE), Tile(COLOR_RED_TILE)],
            [Tile(COLOR_YELLOW_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_YELLOW_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_YELLOW_TILE)],
            [Tile(COLOR_RED_TILE), Tile(COLOR_BLUE_TILE), Tile(COLOR_RED_TILE), Tile(COLOR_BLUE_TILE), Tile(COLOR_YELLOW_TILE, Portal("yellow"))],
            [Tile(COLOR_BLUE_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_YELLOW_TILE), Tile(COLOR_NEUTRAL_TILE), Tile(COLOR_RED_TILE)],
            [Tile(COLOR_YELLOW_TILE), Tile(COLOR_RED_TILE), Tile(COLOR_BLUE_TILE, Portal("blue")), Tile(COLOR_BLUE_TILE), Tile(COLOR_YELLOW_TILE)]
        ]
        for row in range(self.dimension):
            for col in range(self.dimension):
                board[row][col].setIndex(Position(col, row))
        return board
    
    def generate_ghosts(self):
        ghosts = []
        possibleColors= ["red"] * 3 + ["blue"] * 3 + ["yellow"] * 3
        for player in [self.player1, self.player2]:
            for color in possibleColors:
                ghosts.append(Ghost(color, player))
        return ghosts
    
    def switchPlayers(self):
        if self.currPlayer == self.player1:
            self.currPlayer = self.player2
        else:
            self.currPlayer = self.player1

    def updateState(self):
        if self.gameState == GameState.PICKING:
            for ghost in self.ghosts:
                if not ghost.placed:
                    return
            self.gameState = GameState.PLAYING

    def checkWinner(self):
        victory = True
        for color in self.player1.colors_cleared:
            if self.player1.colors_cleared[color] == 0:
                victory = False
        if victory:
            return True
        for color in self.player2.colors_cleared:
            if self.player2.colors_cleared[color] == 0:
                victory = False
        return victory

    def possibleMoves(self, ghost : Ghost):
        row, col = ghost.index.y, ghost.index.x
        possible_moves = []
        for dcol, drow in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < self.dimension and 0 <= new_col < self.dimension:
                if self.checkTile(ghost, new_row, new_col):
                    possible_moves.append(Position(new_col, new_row))
        return possible_moves
    
    def possiblePlacements(self):
        possible_placements = []
        for row in range(self.dimension):
            for col in range(self.dimension):
                tile = self.board[row][col]
                if not (tile.full or tile.portal):
                    for ghost in self.ghosts:
                        if not ghost.placed:
                            if compareGhostTileColor(ghost, tile) and ghost.player == self.currPlayer:
                                possible_placements.append(Position(col, row))
        return possible_placements
    
    def playerGhostIDs(self):
        return [i for i in range(len(self.ghosts)) if self.ghosts[i].player == self.currPlayer]

    def move(self, ghostID, index : Position):
        state_copy = deepcopy(self)
        state_copy.currGhost = state_copy.ghosts[ghostID]
        state_copy.moveGhost(index)
        return state_copy
    
    def place(self, index : Position):
        state_copy = deepcopy(self)
        tile = state_copy.board[index.y][index.x]
        if index in state_copy.possiblePlacements():
            for ghost in state_copy.ghosts:
                if not ghost.placed:
                    if compareGhostTileColor(ghost, tile) and ghost.player == state_copy.currPlayer:
                        tile.full = True
                        ghost.setIndex(Position(index.x, index.y))
                        ghost.placed = True
                        state_copy.switchPlayers()
                        state_copy.updateState()
                        break
        return state_copy
    
    def checkTile(self, ghost: Ghost, new_row, new_col):
        if self.board[new_row][new_col].portal:
            return False
        for g in self.ghosts:
            if g.index.x == new_col and g.index.y == new_row and g.color == ghost.color:
                return False
        return True
    
    def moveGhost(self, index : Position):
        if index in self.possibleMoves(self.currGhost): # move is possible
            for i in range(len(self.ghosts)):
                if self.ghosts[i] == self.currGhost:
                    for j in range(len(self.ghosts)):
                        if self.ghosts[j].index == index: # going to this (another) ghost's tile
                            if self.ghosts[i].winsFight(self.ghosts[j]):
                                freeSpaceIndex = self.ghosts[i].index
                                self.board[freeSpaceIndex.y][freeSpaceIndex.x].full = False
                                self.dungeon.addGhost(self.ghosts[j])
                                self.ghosts[i].setIndex(index)
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
                                freeSpaceIndex = self.ghosts[i].index
                                self.dungeon.addGhost(self.ghosts[i])
                                self.board[freeSpaceIndex.y][freeSpaceIndex.x].full = False
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
                    freeSpaceIndex = self.ghosts[i].index
                    self.board[freeSpaceIndex.y][freeSpaceIndex.x].full = False
                    self.ghosts[i].setIndex(index)
                    self.board[index.y][index.x].full = True
                    self.currGhost = 0
                    self.ghostEscape()
                    self.switchPlayers()
                    return
                
    def saveGhost(self):
        if self.currGhost.color == "red":
            newIndex = Position(RS_X, RS_Y)
        elif self.currGhost.color == "blue":
            newIndex = Position(BS_X, BS_Y)
        else:
            newIndex = Position(YS_X, YS_Y)
        tile = self.board[newIndex.y][newIndex.x]
        if not tile.full:
            self.currGhost.setIndex(newIndex)
            self.ghosts.append(self.currGhost)
            self.dungeon.removeGhost(self.currGhost)
            tile.full = True
            self.currGhost = 0
            self.switchPlayers()
                
    def findGhostID(self, index : Position):
        for i in range(len(self.ghosts)):
            if self.ghosts[i].index.x == index.x and self.ghosts[i].index.y == index.y:
                return i
        return -1

    def ghostEscape(self):
        ghostPlayer = self.redEscape()
        if ghostPlayer == "Player 1":
            self.player1.colors_cleared["red"] += 1
            return True
        elif ghostPlayer == "Player 2":
            self.player2.colors_cleared["red"] += 1
            return True
        ghostPlayer = self.yellowEscape()
        if ghostPlayer == "Player 1":
            self.player1.colors_cleared["yellow"] += 1
            return True
        elif ghostPlayer == "Player 2":
            self.player2.colors_cleared["yellow"] += 1
            return True
        ghostPlayer = self.blueEscape()
        if ghostPlayer == "Player 1":
            self.player1.colors_cleared["blue"] += 1
            return True
        elif ghostPlayer == "Player 2":
            self.player2.colors_cleared["blue"] += 1
            return True   
        return False

    def redEscape(self):
        dir = self.board[RP_Y][RP_X].portal.direction
        if PORTAL_DIR[dir] == "LEFT":
            id = self.findGhostID(Position(RP_X - 1, RP_Y))
            if id != -1 and self.ghosts[id].color == "red":
                ghostPlayer = self.ghosts[id].player.name
                self.ghosts.remove(self.ghosts[id])
                return ghostPlayer
        elif PORTAL_DIR[dir] == "DOWN":
            id = self.findGhostID(Position(RP_X, RP_Y + 1))
            if id != -1 and self.ghosts[id].color == "red":
                ghostPlayer = self.ghosts[id].player.name
                self.ghosts.remove(self.ghosts[id])
                return ghostPlayer
        elif PORTAL_DIR[dir] == "RIGHT":
            id = self.findGhostID(Position(RP_X + 1, RP_Y))
            if id != -1 and self.ghosts[id].color == "red":
                ghostPlayer = self.ghosts[id].player.name
                self.ghosts.remove(self.ghosts[id])
                return ghostPlayer 
        return ""
    
    def yellowEscape(self):
        dir = self.board[YP_Y][YP_X].portal.direction
        if PORTAL_DIR[dir] == "UP":
            id = self.findGhostID(Position(YP_X, YP_Y - 1))
            if id != -1 and self.ghosts[id].color == "yellow":
                ghostPlayer = self.ghosts[id].player.name
                self.ghosts.remove(self.ghosts[id])
                return ghostPlayer
        elif PORTAL_DIR[dir] == "LEFT":
            id = self.findGhostID(Position(YP_X - 1, YP_Y))
            if id != -1 and self.ghosts[id].color == "yellow":
                ghostPlayer = self.ghosts[id].player.name
                self.ghosts.remove(self.ghosts[id])
                return ghostPlayer
        elif PORTAL_DIR[dir] == "DOWN":
            id = self.findGhostID(Position(YP_X, YP_Y + 1))
            if id != -1 and self.ghosts[id].color == "yellow":
                ghostPlayer = self.ghosts[id].player.name
                self.ghosts.remove(self.ghosts[id])
                return ghostPlayer 
        return ""
    
    def blueEscape(self):
        dir = self.board[BP_Y][BP_X].portal.direction
        if PORTAL_DIR[dir] == "LEFT":
            id = self.findGhostID(Position(BP_X - 1, BP_Y))
            if id != -1 and self.ghosts[id].color == "blue":
                ghostPlayer = self.ghosts[id].player.name
                self.ghosts.remove(self.ghosts[id])
                return ghostPlayer
        elif PORTAL_DIR[dir] == "UP":
            id = self.findGhostID(Position(BP_X, BP_Y - 1))
            if id != -1 and self.ghosts[id].color == "blue":
                ghostPlayer = self.ghosts[id].player.name
                self.ghosts.remove(self.ghosts[id])
                return ghostPlayer
        elif PORTAL_DIR[dir] == "RIGHT":
            id = self.findGhostID(Position(BP_X + 1, BP_Y))
            if id != -1 and self.ghosts[id].color == "blue":
                ghostPlayer = self.ghosts[id].player.name
                self.ghosts.remove(self.ghosts[id])
                return ghostPlayer
        return ""
