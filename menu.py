import pygame
from draw import draw_menu, draw_solver_menu, draw_text_input
from state import LightsOutState


class MenuOption:
    PLAY = "play"
    SOLVER = "solver"
    FILE = "file"
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
    """
    Show the algorithm selection screen and return the chosen algorithm.
    Only reached if the user picked MenuOption.SOLVER.

    Returns:
        SolverOption.BFS   - breadth-first search
        SolverOption.ASTAR - A* search
        MenuOption.QUIT    - user closed the window
    """
    pass


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