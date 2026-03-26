import pygame
from draw import draw_menu, draw_solver_menu


class MenuOption:
    PLAY = "play"
    SOLVER = "solver"
    QUIT = "quit"


class SolverOption:
    BFS = "bfs"
    ASTAR = "astar"


def run_main_menu(screen, font):
    """
    Show the main menu and return the user's choice.

    Returns:
        MenuOption.PLAY   - user wants to play manually
        MenuOption.SOLVER - user wants to watch a solver
        MenuOption.QUIT   - user closed the window
    """
    while True:
        play_rect, solver_rect, quit_rect = draw_menu(screen, font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return MenuOption.QUIT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                return MenuOption.QUIT

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return MenuOption.PLAY
                if solver_rect.collidepoint(event.pos):
                    return MenuOption.SOLVER
                if quit_rect.collidepoint(event.pos):
                    return MenuOption.QUIT


def run_solver_menu(screen, font):
    """
    Show the algorithm selection screen and return the chosen algorithm.
    Only reached if the user picked MenuOption.SOLVER.

    Returns:
        SolverOption.BFS   - breadth-first search
        SolverOption.ASTAR - A* search
        MenuOption.QUIT    - user closed the window
    """
    pass