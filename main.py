import pygame

from defines import *
from game import Game
from logic import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('18 Ghosts')
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    game = Game(execute_real_move, execute_minimax_move, screen, my_font)
    game.play()

if __name__ == "__main__":
    main()
