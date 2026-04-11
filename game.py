import pygame
from state import LightsOutState
from draw import draw_board, draw_solver_overlay
from solver import solve_dfs, solve_astar, solve_bfs, solve_ids, solve_ucs, solve_greedy
from draw import draw_message
import os
from datetime import datetime
from constants import *


def ensure_results_dir():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

def save_solver_results(algorithm_name, initial_state, moves, execution_time):
    ensure_results_dir()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    board_size = initial_state.size
    filename = f"{RESULTS_DIR}/{algorithm_name}_{board_size}x{board_size}_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("LIGHTS OUT - SOLVER RESULTS\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Algorithm: {algorithm_name}\n")
        f.write(f"Board Size: {board_size}x{board_size}\n")
        f.write(f"Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Execution Time: {execution_time:.4f} seconds\n")
        
        if moves is not None:
            f.write(f"Moves Found: {len(moves)}\n")
        else:
            f.write(f"Moves Found: NO SOLUTION\n")
        
        f.write("\n" + "-" * 70 + "\n")
        f.write("INITIAL BOARD:\n")
        f.write("-" * 70 + "\n")
        for row in initial_state.board:
            f.write(" ".join(str(cell) for cell in row) + "\n")
        
        if moves is not None and len(moves) > 0:
            f.write("\n" + "-" * 70 + "\n")
            f.write("SOLUTION MOVES:\n")
            f.write("-" * 70 + "\n")
            for i, (row, col) in enumerate(moves, 1):
                f.write(f"Move {i:2d}: ({row}, {col})\n")
            
            f.write("\n" + "-" * 70 + "\n")
            f.write("FINAL BOARD:\n")
            f.write("-" * 70 + "\n")
            final_state = initial_state
            for row, col in moves:
                final_state = final_state.apply_move(row, col)
            for row in final_state.board:
                f.write(" ".join(str(cell) for cell in row) + "\n")
        else:
            f.write("\n" + "-" * 70 + "\n")
            f.write("NO SOLUTION FOUND\n")
            f.write("-" * 70 + "\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 70 + "\n")
    
    return filename
    
def run_human_game(screen, font, file_board=None, grid_size=GRID_SIZE):
    wins = 0
    time_left = TIME_START
    time1 = pygame.time.get_ticks()

    if file_board:
        state = file_board
    else:
        state = LightsOutState.generate_random_board(grid_size, NUM_MOVES)

    board_width = state.size * CELL_SIZE
    board_height = state.size * CELL_SIZE
    board_x = (WINDOW_WIDTH - board_width) // 2
    board_y = (WINDOW_HEIGHT - board_height) // 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if (board_x <= mouse_x <= board_x + board_width and
                        board_y <= mouse_y <= board_y + board_height):
                    
                    col = (mouse_x - board_x) // CELL_SIZE
                    line = (mouse_y - board_y) // CELL_SIZE
                    state = state.apply_move(line, col)

                    if state.is_goal():
                        wins += 1
                        time_left += TIME_WON
                        state = LightsOutState.generate_random_board(state.size, NUM_MOVES)

        time2 = pygame.time.get_ticks()
        time_left -= (time2 - time1) / 1000
        time1 = time2

        if time_left <= 0:
            return wins

        draw_board(screen, state, wins, time_left, font)
        pygame.display.flip()


def run_solver_game(screen, font, algorithm, file_board=None, grid_size=GRID_SIZE):

    if file_board:
        initial_state = file_board
    else:
        initial_state = LightsOutState.generate_random_board(grid_size, NUM_MOVES)
        
    moves = None

    #se for A*
    if isinstance(algorithm, tuple):
        algo_name, weight = algorithm
    else:
        algo_name = algorithm
        weight = 1.0 #A* normal

    start_time = pygame.time.get_ticks()

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

    end_time = pygame.time.get_ticks()
    execution_time = (end_time - start_time)/1000

    algorithm_display = algo_name.upper() if algo_name != "weighted_astar" else "WEIGHTED_ASTAR"
    filename = save_solver_results(algorithm_display, initial_state, moves, execution_time)
    print(f"Results saved to: {filename}")

    #encontrou solucação da display dos moves feitos
    if moves is not None:
        step_through_moves(screen, font, initial_state, moves)
    
    else:
        #caso de erro 
        draw_message(screen, font, f"No solution found!\nSaved to:\n{os.path.basename(filename)}")


def step_through_moves(screen, font, state, moves):
    board_width = state.size * CELL_SIZE
    board_height = state.size * CELL_SIZE
    board_x = (WINDOW_WIDTH - board_width) // 2
    board_y = (WINDOW_HEIGHT - board_height) // 2

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
        draw_solver_overlay(screen, move, font, board_x, board_y)
        pygame.display.flip()
        
        #espera entre cada move
        pygame.time.wait(1000) 

    pygame.time.wait(500)