from defines import *
from game import Game
from player import Player
import pygame

def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 1000))
    done = False
    game = Game(screen, Player("um", PlayerType.PLAYER), Player("dois", PlayerType.BOT))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        game.currPlayer.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()

