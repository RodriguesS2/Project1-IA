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


    # --- Title ---
    title_font = pygame.font.SysFont(None, 80)
    title = title_font.render("Lights Out", True, LIGHT_COLOR_OFF)
    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    screen.blit(title, title_rect)

    # --- Buttons ---
    button_width = 220
    button_height = 60
    button_x = WINDOW_WIDTH // 2 - button_width // 2
    gap = 30
 
    play_y = WINDOW_HEIGHT // 2
    solver_y = play_y + button_height + gap
    quit_y = solver_y + button_height + gap
 
    play_rect = pygame.Rect(button_x, play_y, button_width, button_height)
    solver_rect = pygame.Rect(button_x, solver_y, button_width, button_height)
    quit_rect = pygame.Rect(button_x, quit_y, button_width, button_height)
 
    for rect, label in [(play_rect, "Play"), (solver_rect, "Solver"), (quit_rect, "Quit")]:
        pygame.draw.rect(screen, LIGHT_COLOR_OFF, rect, border_radius=12)
        text = font.render(label, True, BACKGROUND_COLOR)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
 
    return play_rect, solver_rect, quit_rect


def draw_solver_menu(screen, font):
    """Draw the algorithm selection screen (BFS, A*, etc.)."""
    pass


def draw_solver_overlay(screen, move, font):
    """Draw an overlay showing the solver's current move on top of the board."""
    pass