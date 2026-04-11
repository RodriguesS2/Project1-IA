import pygame
import sys
from menu import run_main_menu, run_mode_menu, run_solver_menu, MenuOption, run_file_input_menu, run_grid_size_menu, run_difficulty_menu
from game import run_human_game, run_solver_game

from constants import WINDOW_WIDTH, WINDOW_HEIGHT


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Lights Out")
    font = pygame.font.SysFont(None, 48)

    while True:
        choice = run_main_menu(screen, font)

        if choice == MenuOption.QUIT:
            break

        file_board_aux = None
        grid_size_aux = None
        num_moves_aux = None

        if choice == MenuOption.FILE:
            file_board_aux = run_file_input_menu(screen, font)
            if file_board_aux is None:
                continue  #volta para o menu
        
        #board aleatorio
        else:
            grid_size_aux = run_grid_size_menu(screen, font)
            
            if grid_size_aux is None:
                continue
            
            num_moves_aux = run_difficulty_menu(screen, font)
            
            if num_moves_aux is None:
                continue

        # human ou solver
        mode = run_mode_menu(screen, font)

        if mode is None or mode == MenuOption.QUIT:
            if mode == MenuOption.QUIT:
                break
            continue

        if mode == MenuOption.PLAY:
            if file_board_aux:
                run_human_game(screen, font, file_board=file_board_aux)
            
            else:
                run_human_game(screen, font, grid_size=grid_size_aux, num_moves=num_moves_aux)

        elif mode == MenuOption.SOLVER:
            algorithm = run_solver_menu(screen, font)

            if algorithm is None:
                continue
            
            if algorithm == MenuOption.QUIT:
                break

            if file_board_aux:
                run_solver_game(screen, font, algorithm, file_board=file_board_aux)
            
            else:
                run_solver_game(screen, font, algorithm, grid_size=grid_size_aux, num_moves=num_moves_aux)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()