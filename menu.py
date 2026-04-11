import pygame
from draw import draw_menu, draw_solver_menu, draw_text_input
from state import LightsOutState
from constants import GRID_SIZE


class MenuOption:
    PLAY = "play"
    SOLVER = "solver"
    FILE = "file"
    QUIT = "quit"


class SolverOption:
    BFS = "bfs"
    DFS = "dfs"
    ASTAR = "astar"
    WEIGHTED_ASTAR = "weighted_astar"
    IDS = "ids"
    UCS = "ucs"
    GREEDY = "greedy"


def run_main_menu(screen, font):

    while True:
        play_rect, solver_rect, file_rect, quit_rect = draw_menu(screen, font)
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
                
                if file_rect.collidepoint(event.pos): 
                    return MenuOption.FILE
                
                if quit_rect.collidepoint(event.pos):
                    return MenuOption.QUIT


def run_solver_menu(screen, font):

    while True:
        rects = draw_solver_menu(screen, font)
        pygame.display.flip()

        bfs_rect, dfs_rect, astar_rect, wastar_rect, ids_rect, ucs_rect, greedy_rect, back_rect = rects

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return MenuOption.QUIT

            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                return MenuOption.QUIT

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bfs_rect.collidepoint(event.pos):
                    return SolverOption.BFS
                if dfs_rect.collidepoint(event.pos):
                    return SolverOption.DFS
                if astar_rect.collidepoint(event.pos):
                    return SolverOption.ASTAR
                if wastar_rect.collidepoint(event.pos):
                    weight = run_weight_input_menu(screen, font)
                    if weight is None:
                        return None
                    return (SolverOption.WEIGHTED_ASTAR, weight)
                if ids_rect.collidepoint(event.pos):
                    return SolverOption.IDS
                if ucs_rect.collidepoint(event.pos):
                    return SolverOption.UCS
                if greedy_rect.collidepoint(event.pos):
                    return SolverOption.GREEDY
                if back_rect.collidepoint(event.pos):
                    return None


def run_file_input_menu(screen, font):
    filename = ""
    error_message = "" 
    
    while True:
        draw_text_input(screen, font, "File Name:", filename, error_message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not filename or filename.strip() == "":
                        error_message = "Invalid or empty name!"
                    
                    else:
                        #le
                        path = "file_board/" + filename.strip()
                        if not path.endswith(".txt"):
                            path += ".txt"
                        
                        board_from_file = LightsOutState.read_from_txt(path)
                        
                        if board_from_file:
                            #carrega o board
                            return board_from_file 
                        
                        else:
                            error_message = "File nor found or invalid!"
                
                elif event.key == pygame.K_BACKSPACE:
                    filename = filename[:-1]
                    error_message = "" #apaga o erro quando apagamos o nome
                
                elif event.key == pygame.K_ESCAPE:
                    return None
                
                else:
                    filename += event.unicode
                    error_message = "" #apaga erro quando escrevemos


def run_grid_size_menu(screen, font):
    grid_str = ""
    error_message = ""
    prompt = f"Enter grid size (default {GRID_SIZE}):"

    while True:
        draw_text_input(screen, font, prompt, grid_str, error_message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not grid_str.strip():
                        return GRID_SIZE

                    try:
                        size = int(grid_str)
                        if size < 2:
                            error_message = "Size must be 2 or greater!"
                        else:
                            return size
                    except ValueError:
                        error_message = "Invalid number!"

                elif event.key == pygame.K_BACKSPACE:
                    grid_str = grid_str[:-1]
                    error_message = ""

                elif event.key == pygame.K_ESCAPE:
                    return None

                else:
                    grid_str += event.unicode
                    error_message = ""


def run_weight_input_menu(screen, font):

    weight_str = ""
    error_message = ""

    while True:
        draw_text_input(screen, font, "Enter A* Weight (e.g. 1.5):", weight_str, error_message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        weight = float(weight_str)
                        if weight <= 0:
                            error_message = "Weight must be greater than 0!"
                        else:
                            return weight
                    except ValueError:
                        error_message = "Invalid number!"

                elif event.key == pygame.K_BACKSPACE:
                    weight_str = weight_str[:-1]
                    error_message = ""

                elif event.key == pygame.K_ESCAPE:
                    return None

                else:
                    weight_str += event.unicode
                    error_message = ""