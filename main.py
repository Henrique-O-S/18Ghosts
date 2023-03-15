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
    player1 = Player("Player 1", PlayerType.PLAYER)
    player2 = Player("Player 2", PlayerType.BOT)

    game = Game(screen, my_font, player1, player2)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN: # CLOSE WITH ESC KEY
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: #choose tile for ghost in initial phase
                x, y = pygame.mouse.get_pos()
                if game.state == GameState.PICKING:
                    game.chooseGhostTile(Position(x,y))
                elif game.state == GameState.PLAYING:    #play
                    game.selectGhost(Position(x,y))
        screen.fill(COLOR_BACKGROUND)
        game.draw()

        pygame.display.flip()
        timer.tick(fps)

if __name__ == "__main__":
    main()

