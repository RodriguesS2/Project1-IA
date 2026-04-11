import pygame
import sys
from menu import run_main_menu, run_solver_menu, MenuOption, run_file_input_menu, run_grid_size_menu
from game import run_human_game, run_solver_game


def main():
    pygame.init()
    from constants import WINDOW_WIDTH, WINDOW_HEIGHT
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Lights Out")
    font = pygame.font.SysFont(None, 48)

    while True:
        choice = run_main_menu(screen, font)

        if choice == MenuOption.QUIT:
            break
        
        elif choice == MenuOption.PLAY:
            grid_size = run_grid_size_menu(screen, font)
            if grid_size is not None:
                run_human_game(screen, font, grid_size=grid_size)

        elif choice == MenuOption.FILE:
            board_from_file = run_file_input_menu(screen, font)

            if board_from_file:
                run_human_game(screen, font, file_board=board_from_file)
        
        elif choice == MenuOption.SOLVER:
            algorithm = run_solver_menu(screen, font)
            
            if algorithm != MenuOption.QUIT:
                grid_size = run_grid_size_menu(screen, font)
                if grid_size is not None:
                    run_solver_game(screen, font, algorithm, grid_size=grid_size)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()