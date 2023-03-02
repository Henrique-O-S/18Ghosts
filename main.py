from defines import *
from game import Game
from player import Player
import pygame
from position import Position
from ghost import Ghost

def main():

    pygame.init()
    timer = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('18 Ghosts')
    my_font = pygame.font.SysFont('Comic Sans MS', 30)

    running = True
    game = Game(screen, my_font, Player("Player 1", PlayerType.PLAYER), Player("Player 2", PlayerType.BOT))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(COLOR_BACKGROUND)
        game.draw()
        Ghost(COLOR_RED_GHOST, Player("Player 1", PlayerType.PLAYER), Position(10,10)).draw(screen)

        pygame.display.flip()
        timer.tick(fps)

if __name__ == "__main__":
    main()

