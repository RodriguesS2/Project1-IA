import pygame
from constants import *


def draw_board(screen, state, wins, time_left, font):
    screen.fill(BACKGROUND_COLOR)

    text_win = font.render(f"Wins: {wins}", True, TEXT_COLOR)
    text_time = font.render(f"Time: {int(time_left)}s", True, TEXT_COLOR)

    screen.blit(text_win, (MARGIN_LEFT, MARGIN_TOP - 80))
    screen.blit(text_time, (MARGIN_LEFT + BOARD_WIDTH - 150, MARGIN_TOP - 80))

    distance_board = 10
    box_x = MARGIN_LEFT - distance_board
    box_y = MARGIN_TOP - distance_board
    box_width = BOARD_WIDTH + (distance_board * 2)
    box_height = BOARD_HEIGHT + (distance_board * 2)

    pygame.draw.rect(screen, LIGHT_COLOR_OFF, (box_x, box_y, box_width, box_height), 3, border_radius=20)

    for line in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            x = MARGIN_LEFT + (column * CELL_SIZE)
            y = MARGIN_TOP + (line * CELL_SIZE)

            color = LIGHT_COLOR_ON if state.board[line][column] == 1 else LIGHT_COLOR_OFF

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE), border_radius=8)
            pygame.draw.rect(screen, LINE_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 2, border_radius=8)



def draw_menu(screen, font):
    """Draw the main menu with Play and Solver options."""
    screen.fill(BACKGROUND_COLOR)


    #title
    title_font = pygame.font.SysFont(None, 80)
    title = title_font.render("Lights Out", True, LIGHT_COLOR_OFF)
    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    screen.blit(title, title_rect)

    #buttons
    button_width = 250
    button_height = 60
    button_x = WINDOW_WIDTH // 2 - button_width // 2
    gap = 30
 
    play_y = WINDOW_HEIGHT // 2
    solver_y = play_y + button_height + gap
    file_y = solver_y + button_height + gap
    quit_y = file_y + button_height + gap
 
    play_rect = pygame.Rect(button_x, play_y, button_width, button_height)
    solver_rect = pygame.Rect(button_x, solver_y, button_width, button_height)
    file_rect = pygame.Rect(button_x, file_y, button_width, button_height)
    quit_rect = pygame.Rect(button_x, quit_y, button_width, button_height)
 
    for rect, label in [(play_rect, "Play"), (solver_rect, "Solver"), (quit_rect, "Quit"), (file_rect, "Use File"),]:
        pygame.draw.rect(screen, LIGHT_COLOR_OFF, rect, border_radius=12)
        text = font.render(label, True, BACKGROUND_COLOR)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
 
    return play_rect, solver_rect, file_rect, quit_rect


def draw_solver_menu(screen, font):
    screen.fill(BACKGROUND_COLOR)

    #title 
    title_font = pygame.font.SysFont(None, 80)
    title = title_font.render("Select Algorithm", True, LIGHT_COLOR_OFF)
    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 5))
    screen.blit(title, title_rect)

    # --- Button grid: 2 columns, 3 rows ---
    button_width = 220
    button_height = 60
    col_gap = 30
    row_gap = 20

    total_width = button_width * 2 + col_gap
    start_x = WINDOW_WIDTH // 2 - total_width // 2
    start_y = WINDOW_HEIGHT // 3

    labels = ["BFS", "DFS", "A*", "Weighted A*", "IDS", "UCS", "Greedy"]
    rects = []

    for i, label in enumerate(labels):
        col = i % 2
        row = i // 2
        x = start_x + col * (button_width + col_gap)
        y = start_y + row * (button_height + row_gap)
        rect = pygame.Rect(x, y, button_width, button_height)
        rects.append(rect)
        pygame.draw.rect(screen, LIGHT_COLOR_OFF, rect, border_radius=12)
        text = font.render(label, True, BACKGROUND_COLOR)
        screen.blit(text, text.get_rect(center=rect.center))

    # --- Back button (centered below the grid) ---
    back_rect = pygame.Rect(
        WINDOW_WIDTH // 2 - button_width // 2,
        start_y + 4 * (button_height + row_gap) + 10,
        button_width,
        button_height
    )
    pygame.draw.rect(screen, LIGHT_COLOR_OFF, back_rect, border_radius=12)
    back_text = font.render("Back", True, BACKGROUND_COLOR)
    screen.blit(back_text, back_text.get_rect(center=back_rect.center))

    return (*rects, back_rect)


def draw_solver_overlay(screen, move, font):
    if move is None:
        return
        
    row, col = move
    
    #calcula as coordenadas exatas do quadrado a aplicar o movimento
    x = MARGIN_LEFT + (col * CELL_SIZE)
    y = MARGIN_TOP + (row * CELL_SIZE)
    
    #desenha uma borda vermelha a volta do quadrado
    highlight_color = (255, 50, 50) # Vermelho
    pygame.draw.rect(screen, highlight_color, (x, y, CELL_SIZE, CELL_SIZE), 5, border_radius=8)
    


def draw_text_input(screen, font, prompt, current_text, error_message=""):
    screen.fill(BACKGROUND_COLOR)
    
    #caixa
    input_text = font.render(prompt, True, TEXT_COLOR)
    screen.blit(input_text, (WINDOW_WIDTH // 2 - input_text.get_width() // 2, WINDOW_HEIGHT // 3))
    
    input_rect = pygame.Rect(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2, WINDOW_WIDTH // 2, 50)
    pygame.draw.rect(screen, LIGHT_COLOR_OFF, input_rect, 2, border_radius=5)
    
    #pos escrita
    text_pos = font.render(current_text + "|", True, LIGHT_COLOR_OFF) 
    screen.blit(text_pos, (input_rect.x + 10, input_rect.y + 10))
    
    if error_message:
        error_font = pygame.font.SysFont(None, 30)
        error_message = error_font.render(error_message, True, (200, 50, 50))

        screen.blit(error_message, (WINDOW_WIDTH // 2 - error_message.get_width() // 2, WINDOW_HEIGHT - 140))
    
    hint_message = pygame.font.SysFont(None, 24).render("Press ENTER to load or ESC to go back", True, (150, 150, 150))
    screen.blit(hint_message, (WINDOW_WIDTH // 2 - hint_message.get_width() // 2, WINDOW_HEIGHT - 100))


def draw_message(screen, font, message):
    screen.fill(BACKGROUND_COLOR)
    
    text_surf = font.render(message, True, (200, 50, 50)) 
    text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    
    screen.blit(text_surf, text_rect)
    pygame.display.flip()
    
    pygame.time.wait(2000)