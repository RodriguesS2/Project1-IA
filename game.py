import pygame
from state import LightsOutState
from draw import draw_board, draw_solver_overlay, draw_hint_button
from solver import solve_dfs, solve_astar, solve_bfs, solve_ids, solve_ucs, solve_greedy
from draw import draw_message
import os
from datetime import datetime
from constants import *
from menu import run_heuristic_menu


def ensure_results_dir():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)


def save_solver_results(algorithm_name, initial_state, moves, execution_time, metrics, heuristic_name=None):
    ensure_results_dir()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    board_size = initial_state.size
    filename = f"{RESULTS_DIR}/{algorithm_name}_{board_size}x{board_size}_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("LIGHTS OUT - SOLVER RESULTS\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Algorithm: {algorithm_name}\n")
        
        #heurística usada se existir
        if heuristic_name:
            f.write(f"Heuristic: {heuristic_name}\n")
        
        f.write(f"Board Size: {board_size}x{board_size}\n")
        f.write(f"Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Execution Time: {execution_time:.4f} seconds\n")
        f.write(f"States Analyzed: {metrics['states_analyzed']}\n")
        f.write(f"Max Memory (queue size): {metrics['max_memory']}\n")
        
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
    
    return filename


def get_heuristic_name(heuristic_used):
    names = {
        "lights_on_count":        "Lights On Count",
        "parity_heuristic":       "Parity",
        "isolated_lights_heuristic": "Isolated Lights"
    }
    return names.get(heuristic_used.__name__, heuristic_used.__name__)


def run_human_game(screen, font, file_board=None, grid_size=GRID_SIZE, num_moves=NUM_MOVES):
    wins = 0
    time_left = TIME_START
    time1 = pygame.time.get_ticks()
    hint_cell = None

    if file_board:
        state = file_board
    else:
        state = LightsOutState.generate_random_board(grid_size, num_moves)

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

                hint_button = pygame.Rect(board_x + board_width - 160, board_y + board_height + 20, 150, 50)
                if hint_button.collidepoint(mouse_x, mouse_y):
                    #usa A* na hint
                    solution, _ = solve_astar(state)
                    if solution:
                        hint_cell = solution[0]
                    continue

                if (board_x <= mouse_x <= board_x + board_width and board_y <= mouse_y <= board_y + board_height):
                    
                    col = (mouse_x - board_x) // CELL_SIZE
                    line = (mouse_y - board_y) // CELL_SIZE
                    state = state.apply_move(line, col)
                    hint_cell = None   

                    if state.is_goal():
                        wins += 1
                        time_left += TIME_WON
                        state = LightsOutState.generate_random_board(state.size, NUM_MOVES)
                        hint_cell = None

        time2 = pygame.time.get_ticks()
        time_left -= (time2 - time1) / 1000
        time1 = time2

        if time_left <= 0:
            return wins

        board_x, board_y = draw_board(screen, state, wins, time_left, font, hint_cell)
        draw_hint_button(screen, font, board_x, board_y, board_width)
        pygame.display.flip()


def run_solver_game(screen, font, algorithm, file_board=None, grid_size=GRID_SIZE, num_moves=NUM_MOVES):
    if file_board:
        initial_state = file_board
    else:
        initial_state = LightsOutState.generate_random_board(grid_size, num_moves)
        
    moves = None
    heuristic_name = None
 
    #se for A*
    if isinstance(algorithm, tuple):
        algo_name, weight = algorithm
    else:
        algo_name = algorithm
        weight = 1.0 #A* normal
 
    start_time = pygame.time.get_ticks()
 
    if algorithm == "bfs":
        moves, metrics = solve_bfs(initial_state)
    
    elif algorithm == "dfs":
        moves, metrics = solve_dfs(initial_state)
    
    elif algorithm == "greedy":
        heuristic = run_heuristic_menu(screen, font)
        if heuristic is None:
            return
        
        heuristic_name = get_heuristic_name(heuristic)
        moves, metrics = solve_greedy(initial_state, heuristic=heuristic)

    elif algorithm == "astar":
        heuristic = run_heuristic_menu(screen, font)
        if heuristic is None:
            return
        
        heuristic_name = get_heuristic_name(heuristic)
        moves, metrics = solve_astar(initial_state, heuristic=heuristic)

    elif algo_name == "weighted_astar":
        heuristic = run_heuristic_menu(screen, font)
        if heuristic is None:
            return
        
        heuristic_name = get_heuristic_name(heuristic)
        moves, metrics = solve_astar(initial_state, heuristic=heuristic, weight=weight)
    
    elif algorithm == "ids":
        moves, metrics = solve_ids(initial_state)
    
    elif algorithm == "ucs":
        moves, metrics = solve_ucs(initial_state)
 
    end_time = pygame.time.get_ticks()
    execution_time = (end_time - start_time) / 1000
 
    algorithm_display = algo_name.upper() if algo_name != "weighted_astar" else "WEIGHTED_ASTAR"
    filename = save_solver_results(algorithm_display, initial_state, moves, execution_time, metrics, heuristic_name)
    print(f"Results saved to: {filename}")
 
    #encontrou solucação da display dos moves feitos
    if moves is not None:
        step_through_moves(screen, font, initial_state, moves)
    
    #caso de erro 
    else:
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