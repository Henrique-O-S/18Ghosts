import pygame
from pygame import Surface, SurfaceType
from pygame.time import get_ticks

from defines import *
from state import State
from position import Position
from logic import *

class Game:
    def __init__(self, player1_logic, player2_logic, screen : Surface | SurfaceType, font):
        self.state = State()
        self.player1_logic = player1_logic
        self.player2_logic = player2_logic
        self.screen = screen
        self.font = font
        x = (self.screen.get_width() - self.state.dimension * TILEWIDTH) / 1.3
        y = (self.screen.get_height() - self.state.dimension * TILEHEIGHT) / 5
        self.boardCoords = Position(x,y)
        x = (screen.get_width() - self.state.dimension * TILEWIDTH) / 1.3
        y = (screen.get_height() - self.state.dimension * TILEHEIGHT) / 5
        self.dungeonCoords = Position(x - 7 * TILEWIDTH, y + TILEHEIGHT)

    def play(self):
        timer = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN: # CLOSE WITH ESC KEY
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        if self.state.currPlayer.name == "Player 1":
                            if self.player1_logic.__name__ == "execute_random_move":
                                self.player1_logic(self)
                            elif self.player1_logic.__name__ == "execute_minimax_move":
                                start_time = get_ticks()
                                if PLAYER_1_DIFFICULTY == 1:
                                    self.player1_logic(self, evaluate_easy, PLAYER_1_DEPTH)
                                elif PLAYER_1_DIFFICULTY == 2:
                                    self.player1_logic(self, evaluate_medium, PLAYER_1_DEPTH)
                                elif PLAYER_1_DIFFICULTY == 3:
                                    self.player1_logic(self, evaluate_hard, PLAYER_1_DEPTH)
                                else:
                                    print("Choose a valid difficulty")
                                    running = False
                                    break
                                end_time = get_ticks()
                                elapsed_time = end_time - start_time
                                print("Player 1 Bot Play Time:", elapsed_time, "ms")
                            elif self.player1_logic.__name__ == "mcts":
                                self.player1_logic(self, evaluate_hard, MCTS_N_ITERATIONS)
                        elif self.state.currPlayer.name == "Player 2":
                            if self.player2_logic.__name__ == "execute_random_move":
                                self.player2_logic(self)
                            elif self.player2_logic.__name__ == "execute_minimax_move":
                                start_time = get_ticks()
                                if PLAYER_1_DIFFICULTY == 1:
                                    self.player2_logic(self, evaluate_easy, PLAYER_2_DEPTH)
                                elif PLAYER_1_DIFFICULTY == 2:
                                    self.player2_logic(self, evaluate_medium, PLAYER_2_DEPTH)
                                elif PLAYER_1_DIFFICULTY == 3:
                                    self.player2_logic(self, evaluate_hard, PLAYER_2_DEPTH)
                                else:
                                    print("Choose a valid difficulty")
                                    running = False
                                    break
                                end_time = get_ticks()
                                elapsed_time = end_time - start_time
                                print("Player 2 Bot Play Time:", elapsed_time, "ms")
                            elif self.player2_logic.__name__ == "mcts":
                                self.player2_logic(self, evaluate_hard, MCTS_N_ITERATIONS)
                        if self.state.gameState == GameState.PLAYING and self.state.checkWinner():
                            self.state.gameState = GameState.OVER
                            running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.state.currPlayer.name == "Player 1" and self.player1_logic.__name__ == "execute_real_move":
                        self.player1_logic(self, Position(x,y))
                    elif self.state.currPlayer.name == "Player 2" and self.player2_logic.__name__ == "execute_real_move":
                        self.player2_logic(self, Position(x,y))
                    if self.state.gameState == GameState.PLAYING and self.state.checkWinner():
                        self.state.gameState = GameState.OVER
                        running = False
            self.screen.fill(COLOR_BACKGROUND)
            self.draw()
            pygame.display.flip()
            timer.tick(fps)

    def drawPlayerTurn(self):
        picking = ""
        if self.state.gameState == GameState.PICKING:
            picking = " to pick a spot"
        self.state.currPlayer.draw(self.screen, self.font, picking)

    def drawBoard(self):
        for row in range(self.state.dimension):
            for col in range(self.state.dimension):
                self.state.board[row][col].setPos(Position(self.boardCoords.x + TILEWIDTH * col, self.boardCoords.y + TILEHEIGHT * row))
                if self.state.currGhost and self.state.currGhost.index.y == row and self.state.currGhost.index.x == col and self.state.currGhost in self.state.ghosts:
                    self.state.board[row][col].draw(self.screen, True)
                else:
                    self.state.board[row][col].draw(self.screen)

    def drawDungeon(self):
        for i in range(3):
            for j in range(6):
                self.state.dungeon.tiles[i][j].setPos(Position(self.dungeonCoords.x + j * TILEWIDTH, self.dungeonCoords.y + i * TILEHEIGHT))
        if self.state.currGhost and self.state.currGhost in self.state.dungeon.ghosts:
            self.state.dungeon.draw(self.screen, self.state.currGhost.index)
        else:
            self.state.dungeon.draw(self.screen)

    def drawGhosts(self):
        for ghost in self.state.ghosts:
            if ghost.placed:
                ghost.setPos(self.boardCoords)
                ghost.draw(self.screen)
        for ghost in self.state.dungeon.ghosts:
            ghost.setPos(self.dungeonCoords)
            ghost.draw(self.screen)

    def draw(self):
        self.drawPlayerTurn()
        self.drawBoard()
        self.drawDungeon()
        self.drawGhosts()

    def chooseGhostTile(self, click : Position):
        if self.clickInsideBoard(click):
            indexes = self.coordsToIndexBoard(click)
            tile = self.state.board[indexes.y][indexes.x]
            if not (tile.full or tile.portal):
                for ghost in self.state.ghosts:
                    if not ghost.placed:
                        if compareGhostTileColor(ghost, tile) and ghost.player == self.state.currPlayer:
                            tile.full = True
                            ghost.setIndex(Position(indexes.x, indexes.y))
                            ghost.placed = True
                            self.state.switchPlayers()
                            self.state.updateState()
                            return
                        
    def coordsToIndexBoard(self, click : Position):
        if self.clickInsideBoard(click):
            indexY = int((click.y - self.boardCoords.y) // TILEHEIGHT)
            indexX = (int(click.x - self.boardCoords.x) // TILEWIDTH)
            return Position(indexX, indexY)

    def coordsToIndexDungeon(self, click: Position):
        if self.clickInsideDungeon(click):
            indexY = int((click.y - self.dungeonCoords.y) // TILEHEIGHT)
            indexX = (int(click.x - self.dungeonCoords.x) // TILEWIDTH)
            return Position(indexX, indexY)

    def clickInsideBoard(self, click : Position):
        return click.x >= self.boardCoords.x and click.x <= self.boardCoords.x + self.state.dimension * TILEWIDTH and click.y >= self.boardCoords.y and click.y <= self.boardCoords.y + self.state.dimension * TILEHEIGHT

    def clickInsideDungeon(self, click : Position):
        return click.x >= self.dungeonCoords.x and click.x <= self.dungeonCoords.x + 6 * TILEWIDTH and click.y >= self.dungeonCoords.y and click.y <= self.dungeonCoords.y + 3 * TILEHEIGHT

    def selectGhost(self, click: Position):
        if self.clickInsideBoard(click):
            ghostIndexes = self.coordsToIndexBoard(click)
            if self.state.currGhost and self.state.currGhost.index == ghostIndexes and self.state.currGhost in self.state.ghosts:  # clicked on selected ghost in board--> stop selecting it
                self.state.currGhost = 0
                return
            for ghost in self.state.ghosts:
                if ghost.index == ghostIndexes:  # board ghost that player clicked
                    if self.state.currGhost:  # if another one in board is selected
                        if self.state.currGhost in self.state.ghosts:
                            self.state.moveGhost(ghost.index)
                    elif ghost.player == self.state.currPlayer:
                        self.state.currGhost = ghost
                        return
            if self.state.currGhost:
                self.state.moveGhost(ghostIndexes)
        elif self.clickInsideDungeon(click):
            ghostIndexes = self.coordsToIndexDungeon(click)
            if self.state.currGhost and self.state.currGhost.index == ghostIndexes and self.state.currGhost in self.state.dungeon.ghosts:  # clicked on selected ghost in dungeon --> stop selecting it
                self.state.currGhost = 0
                return
            for ghost in self.state.dungeon.ghosts:
                if ghost.index == ghostIndexes and ghost.player == self.state.currPlayer:
                    self.state.currGhost = ghost
                    self.state.saveGhost()
                    return
