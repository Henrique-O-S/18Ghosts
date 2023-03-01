from defines import *
from game import Game
from player import Player
import pygame

def main():

    pygame.init()
    timer = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('18 Ghosts')
    my_font = pygame.font.SysFont('Comic Sans MS', 30)

    running = True
    game = Game(screen, my_font, Player("um", PlayerType.PLAYER), Player("dois", PlayerType.BOT))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(COLOR_BACKGROUND)
        game.draw()

        pygame.display.flip()
        timer.tick(fps)

if __name__ == "__main__":
    main()

