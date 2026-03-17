import random

class LightsOutState:

    def __init__(self, board, size = 5):
        self.size = size
        self.board = tuple(tuple(row) for row in board)


    #num_moves é o numero de movimentos que vamos usar para baralhar o tabuleiro (em teoria quanto maior, mais dificil)
    @staticmethod #para não chamar com self
    def generate_random_board(size=5, num_moves=10): 
        board = [[0] * size for _ in range(size)] #cria um tabuleiro com tudo a 0
        state = LightsOutState(board, size)
        
        for _ in range(num_moves): 

            #escolhe uma linha e uma coluna onde aplicar o movimento
            row = random.randint(0, size - 1)
            col = random.randint(0, size - 1)
            
            state = state.apply_move(row, col)
        
        return state


    def is_goal(self):
        for row in self.board:
            for cel in row:
                if cel == 1: return False

        return True 
    

    #verificar que está dentro dos limites do tabuleiro
    def is_valid_move(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size


    def apply_move(self, row, col):
        board = [list(r) for r in self.board]  #transforma numa lista para ser mutável
        
        for pos_row, pos_col in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]: # 0,0 é o ponto onde clicamos e os outros são so 4 vizinhos
            neighbor_row = row + pos_row #anda na linha (pos antes e depois)
            neighbor_col = col + pos_col #anda na coluna (pos acima e abaixo)
            
            if self.is_valid_move(neighbor_row, neighbor_col): 
                board[neighbor_row][neighbor_col] ^= 1 #inverte o estado
        
        return LightsOutState(board, self.size) 


    #função para a IA, para saber todas as possibilidades de movimentos
    def get_neighbors(self):
        neighbors = []

        for row in range(self.size):
            for col in range(self.size):
                new_state = self.apply_move(row, col) #para cada posição aplica um movimento e adiciona a lista
                neighbors.append((new_state, (row, col)))

        return neighbors


    def __eq__(self, other):
        if isinstance(other, LightsOutState) and self.board == other.board: #verifica se são do mesmo tipo e o tabuleiro é igal
            return True
        
        return False
    

    def __hash__(self):
        return hash(self.board)
