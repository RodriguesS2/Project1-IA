import pygame
import sys

#tabuleiro
GRID_SIZE = 5
CELL_SIZE = 100
BOARD_WIDTH = GRID_SIZE * CELL_SIZE
BOARD_HEIGHT = GRID_SIZE * CELL_SIZE

#margens
MARGIN_TOP = 250   
MARGIN_BOTTOM = 250
MARGIN_LEFT = 250
MARGIN_RIGHT = 250
WINDOW_WIDTH = BOARD_WIDTH + MARGIN_LEFT + MARGIN_RIGHT
WINDOW_HEIGHT = BOARD_HEIGHT + MARGIN_TOP + MARGIN_BOTTOM

#cores
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (255, 255, 255)
LIGHT_COLOR_OFF = (255, 0, 255)

game_board = []

for i in range(GRID_SIZE):
    row = []
    for j in range(GRID_SIZE):
        row.append(False)
    game_board.append(row)

def board(screen):
    screen.fill(BACKGROUND_COLOR)

    distance_board = 10
    
    #coordenadas para contorno
    box_x = MARGIN_LEFT - distance_board
    box_y = MARGIN_TOP - distance_board
    box_width = BOARD_WIDTH + (distance_board * 2)
    box_height = BOARD_HEIGHT + (distance_board * 2)
    
    pygame.draw.rect(
        screen, 
        LIGHT_COLOR_OFF, 
        (box_x, box_y, box_width, box_height), 
        3,                 
        border_radius = 20   
    )

    #para desenhar os quadrados do tabuleiro
    for line in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            
            #pos
            x = MARGIN_LEFT + (column * CELL_SIZE)
            y = MARGIN_TOP + (line * CELL_SIZE)

            if game_board[line][column]:
                color = (255,255,0)   # light ON
            else:
                color = LIGHT_COLOR_OFF

            #desenha o fundo de cada quadrado
            pygame.draw.rect(
                screen, 
                color, 
                (x, y, CELL_SIZE, CELL_SIZE), 
                border_radius = 8
            )

            #desenha a linha que contorna cada quadrado
            pygame.draw.rect(
                screen, 
                LINE_COLOR, 
                (x, y, CELL_SIZE, CELL_SIZE), 
                2,               
                border_radius = 8 
            )

def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Lights Out")

    loop = True
    while loop:

        #processar as ações dentro do jogo
        for event in pygame.event.get():

            #parar o jogo
            if event.type == pygame.QUIT:
                loop = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x: #carregar no X fecha o jogo tbm
                    loop = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if (MARGIN_LEFT <= mouse_x and MARGIN_LEFT + BOARD_WIDTH >= mouse_x and MARGIN_TOP<=mouse_y and MARGIN_TOP+BOARD_HEIGHT>=mouse_y):
                    col=(mouse_x-MARGIN_LEFT) // CELL_SIZE
                    line=(mouse_y-MARGIN_TOP)//CELL_SIZE
                    game_board[line][col]=not game_board[line][col]


        board(screen)

        #atualiza o que vemos depois de desenhar o tabuleiro
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()