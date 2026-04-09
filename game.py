import pygame
from state import LightsOutState
from draw import draw_board, draw_solver_overlay
from constants import *


def run_human_game(screen, font, file_board=None):
    """
    Main loop for the human-controlled game.
    Handles mouse clicks, timing, and win detection.
    """
    state = LightsOutState.generate_random_board(GRID_SIZE, NUM_MOVES)
    wins = 0
    time_left = TIME_START
    time1 = pygame.time.get_ticks()

    #carregar o board se existir
    if file_board:
        state = file_board
    else:
        state = LightsOutState.generate_random_board(GRID_SIZE, NUM_MOVES)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if (MARGIN_LEFT <= mouse_x <= MARGIN_LEFT + BOARD_WIDTH and
                        MARGIN_TOP <= mouse_y <= MARGIN_TOP + BOARD_HEIGHT):
                    
                    col = (mouse_x - MARGIN_LEFT) // CELL_SIZE
                    line = (mouse_y - MARGIN_TOP) // CELL_SIZE
                    state = state.apply_move(line, col)

                    if state.is_goal():
                        wins += 1
                        time_left += TIME_WON
                        state = LightsOutState.generate_random_board(GRID_SIZE, NUM_MOVES)

        time2 = pygame.time.get_ticks()
        time_left -= (time2 - time1) / 1000
        time1 = time2

        if time_left <= 0:
            return wins

        draw_board(screen, state, wins, time_left, font)
        pygame.display.flip()


def run_solver_game(screen, font, algorithm):
    """
    Main loop for the solver-controlled game.
    Calls the appropriate solver, then steps through its moves visually.

    Args:
        algorithm: a SolverOption constant (e.g. SolverOption.BFS)
    """
    pass


def _step_through_moves(screen, font, state, moves):
    """
    Animate a list of (row, col) moves on the board, one per frame/tick.
    Used by run_solver_game once a solution is found.

    Args:
        moves: list of (row, col) tuples returned by the solver
    """
    pass