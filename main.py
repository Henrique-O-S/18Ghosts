import pygame

from defines import *
from game import Game
from logic import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    title_font = pygame.font.SysFont(None, 100)
    title = title_font.render("18 Ghosts", True, (COLOR_FONT))

    # Define Font
    font = pygame.font.Font(None, 60)

    # Define Text
    text1 = font.render("Play Game", True, (255,0,0))
    text2 = font.render("Options", True, (255,255,0))
    text3 = font.render("Exit", True, (0,0,255))

    text4 = font.render("Player vs Player", True, (255, 0, 0))
    text5 = font.render("Player vs Bot", True, (255, 255, 0))
    text6 = font.render("Bot vs Bot", True, (0, 0, 255))

    # Define Rectangles
    rect1 = pygame.Rect((WIDTH / 2) - 150, (HEIGHT / 2) - 100, 300, 100)
    rect2 = pygame.Rect((WIDTH / 2) - 150, (HEIGHT / 2), 300, 100)
    rect3 = pygame.Rect((WIDTH / 2) - 150, (HEIGHT / 2) + 100, 300, 100)

    rect4 = pygame.Rect(0,0,0,0)
    rect5 = pygame.Rect(0,0,0,0)
    rect6 = pygame.Rect(0,0,0,0)

    # Main Game Loop
    player_player = True
    player_bot = False
    bot_bot = False
    main_menu = True
    options_menu = False
    while main_menu:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu = False
            elif event.type == pygame.KEYDOWN:  # CLOSE WITH ESC KEY
                if event.key == pygame.K_ESCAPE:
                    main_menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if Play Game button is clicked
                if rect1.collidepoint(event.pos):
                    print("Play Game!")
                    if player_player:
                        game = Game(execute_real_move, execute_real_move, screen, font)
                    elif player_bot:
                        if PLAYER_2_BOT_TYPE == 0:
                            game = Game(execute_real_move, execute_minimax_move, screen, font)
                        elif PLAYER_2_BOT_TYPE == 1:
                            game = Game(execute_real_move, mcts, screen, font)
                        else:
                            print("Choose a valid bot type")
                            break
                    elif bot_bot:
                        if PLAYER_1_BOT_TYPE == 0 and PLAYER_2_BOT_TYPE == 0:
                            game = Game(execute_minimax_move, execute_minimax_move, screen, font)
                        elif PLAYER_1_BOT_TYPE == 0 and PLAYER_2_BOT_TYPE == 1:
                            game = Game(execute_minimax_move, mcts, screen, font)
                        elif PLAYER_1_BOT_TYPE == 1 and PLAYER_2_BOT_TYPE == 0:
                            game = Game(mcts, execute_minimax_move, screen, font)
                        elif PLAYER_1_BOT_TYPE == 1 and PLAYER_2_BOT_TYPE == 1:
                            game = Game(mcts, mcts, screen, font)
                        else:
                            print("Choose a valid bot type")
                            main_menu = False
                            break
                    game.play()
                # Check if Options button is clicked
                elif rect2.collidepoint(event.pos):
                    print("Options!")
                    options_menu = True
                    rect4 = pygame.Rect((WIDTH / 2) - 150, (HEIGHT / 2) - 100, 300, 100)
                    rect5 = pygame.Rect((WIDTH / 2) - 150, (HEIGHT / 2), 300, 100)
                    rect6 = pygame.Rect((WIDTH / 2) - 150, (HEIGHT / 2) + 100, 300, 100)
                    while options_menu:
                        # Event Loop
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                options_menu = False
                            elif event.type == pygame.KEYDOWN:  # CLOSE WITH ESC KEY
                                if event.key == pygame.K_ESCAPE:
                                    options_menu = False
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                # Check if Play Game button is clicked
                                if rect4.collidepoint(event.pos):
                                    print("Player vs Player!")
                                    player_player = True
                                    player_bot = False
                                    bot_bot = False
                                    options_menu = False
                                # Check if Options button is clicked
                                if rect5.collidepoint(event.pos):
                                    print("Player vs Bot!")
                                    player_player = False
                                    player_bot = True
                                    bot_bot = False
                                    options_menu = False
                                # Check if Exit button is clicked
                                if rect6.collidepoint(event.pos):
                                    print("Bot vs Bot!")
                                    player_player = False
                                    player_bot = False
                                    bot_bot = True
                                    options_menu = False

                        # Draw Screen
                        screen.fill(COLOR_BACKGROUND)

                        screen.blit(title, (485, 50))
                        screen.blit(text4, (rect4.x + 0, rect4.y + 30))
                        screen.blit(text5, (rect5.x + 18, rect5.y + 30))
                        screen.blit(text6, (rect6.x + 54, rect6.y + 30))

                        # Update Screen
                        pygame.display.update()

                # Check if Exit button is clicked
                elif rect3.collidepoint(event.pos):
                    main_menu = False

        # Draw Screen
        screen.fill(COLOR_BACKGROUND)
        #pygame.draw.rect(screen, COLOR_FONT_RECT, rect1)
        #pygame.draw.rect(screen, COLOR_FONT_RECT, rect2)
        #pygame.draw.rect(screen, COLOR_FONT_RECT, rect3)
        screen.blit(title, (485, 50))
        screen.blit(text1, (rect1.x + 45, rect1.y + 30))
        screen.blit(text2, (rect2.x + 63, rect2.y + 30))
        screen.blit(text3, (rect3.x + 99, rect3.y + 30))

        # Update Screen
        pygame.display.update()
    #game = Game(execute_real_move, execute_minimax_move, screen, my_font)
    #game.play()

if __name__ == "__main__":
    main()
