import pygame
from state import LightsOutState
from draw import draw_board, draw_solver_overlay
from solver import solve_dfs, solve_astar, solve_bfs, solve_ids, solve_ucs, solve_greedy
from draw import draw_message
from constants import *


def run_human_game(screen, font, file_board=None):
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


def run_solver_game(screen, font, algorithm, file_board=None):

    if file_board:
        initial_state = file_board
    else:
        initial_state = LightsOutState.generate_random_board(GRID_SIZE, NUM_MOVES)
        
    moves = None

    #se for A*
    if isinstance(algorithm, tuple):
        algo_name, weight = algorithm
    else:
        algo_name = algorithm
        weight = 1.0 #A* normal

    if algorithm == "bfs":
        moves = solve_bfs(initial_state)
    
    elif algorithm == "dfs":
        moves = solve_dfs(initial_state)

    elif algorithm == "greedy":
        moves = solve_greedy(initial_state)

    elif algorithm == "astar":
        moves = solve_astar(initial_state)

    elif algo_name == "weighted_astar":
        moves = solve_astar(initial_state, weight=weight)

    elif algorithm == "ids":
        moves = solve_ids(initial_state)

    elif algorithm == "ucs":
        moves = solve_ucs(initial_state)

    #encontrou solucação da display dos moves feitos
    if moves is not None:
        step_through_moves(screen, font, initial_state, moves)
    
    else:
        #caso de erro 
        draw_message(screen, font, "Error while solving")


def step_through_moves(screen, font, state, moves):
    #desenha tabuleiro inicial
    draw_board(screen, state, wins=0, time_left=0, font=font)
    pygame.display.flip()
    pygame.time.wait(2000)

    for move in moves:
        #caso queira sair
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        row, col = move
        state = state.apply_move(row, col)

        draw_board(screen, state, wins=0, time_left=0, font=font)        
        draw_solver_overlay(screen, move, font)
        pygame.display.flip()
        
        #espera entre cada move
        pygame.time.wait(1000) 

    pygame.time.wait(500)