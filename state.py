class LightsOutState:

    def __init__(self, board, size = 5):
        self.size = size
        self.board = tuple(tuple(row) for row in board)


    def is_goal(self):
        for row in self.board:
            for cel in row:
                if cel == 1: return False

        return True 


    def apply_move(self, row, col):

        board = [list(r) for r in self.board]  #lista mutável
        
        # aplica o toggle na célula e nos 4 vizinhos
        # retorna um NOVO LightsOutState com a grelha modificada
        pass

    def get_neighbors(self):
        # para cada célula (row, col) do tabuleiro
        # gera o estado resultante de clicar nessa célula
        # retorna uma lista de (novo_estado, (row, col))
        pass

    def __eq__(self, other):
        # dois estados são iguais se a grelha for igual
        pass

    def __hash__(self):
        # retorna o hash da grelha (já é tuple de tuples, hashável)
        pass

    def __repr__(self):
        # representação em texto, útil para debug
        pass