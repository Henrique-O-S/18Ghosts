import random

from defines import *
from ghost import Ghost
from tile import Tile
from player import Player


class Game:
    def __init__(self, screen, player1 : Player, player2 : Player):
        self.player1 = player1
        self.player2 = player2
        self.dimention = 5
        self.boardCorners = [0, self.dimention, self.dimention * self.dimention - self.dimention, self.dimention * self.dimention - 1]
        self.board = self.generateBoard()
        self.screen = screen
        self.currPlayer = player1


    def generateBoard(self):
        auxBoard = []
        possibleColors= [REDCOLORTILE] * 6 + [BLUECOLORTILE] * 6 + [YELLOWCOLORTILE] * 6 + [NEUTRALCOLORTILE] * 3
        for tile in range(self.dimention * self.dimention):
            if tile in self.boardCorners:
                auxBoard += [Tile(NEUTRALCOLORTILE)]
            else:
                selectedColor = random.choice(possibleColors)
                auxBoard += [Tile(selectedColor)]
                possibleColors.remove(selectedColor)
        board = [auxBoard[i * self.dimention:(i + 1) * self.dimention] for i in range((len(auxBoard) + self.dimention - 1) // self.dimention)]

        #for row in board:
         #   print("-----")
          #  for col in row:
           #     print(col)
            #print("-----")
    def drawPlayerTurn(self):
        self.currPlayer.draw(self.screen)
