from state import LightsOutState
import heapq
from collections import deque

def solve_bfs(initial_state):
    """
    Solve the board using Breadth-First Search.

    Args:
        initial_state: LightsOutState

    Returns:
        List of (row, col) moves that lead to the goal, or None if unsolvable.
    """
    pass


def solve_astar(initial_state, heuristic=None, weight = 1.0):

    if heuristic is None:
        heuristic = lights_on_count
    
    if initial_state.is_goal():
        return []
 
    # Priority queue: (f, counter, g, state, moves)
    # f = g + h  (custo total estimado)
    # g = moves realizados até ao momento (custo atual)
    # h = heuristica 
    # counter serve de desempate para o Python não comparar LightsOutState objects
    counter = 0
    heap = []
    heapq.heappush(heap, (heuristic(initial_state), counter, 0, initial_state, []))
 
    # Mapeia state hash -> melhor g (custo) até ao momento
    best_g = {hash(initial_state): 0}
 
    while heap:
        # Dá pop ao estado com menor f (custo total estimado)
        f, _, g, current_state, moves = heapq.heappop(heap)
 
        if current_state.is_goal():
            return moves
 
        # Skip se já foi encontrado um caminho mais "barato" pra chegar a este state
        if g > best_g.get(hash(current_state), float('inf')):
            continue
        
        # Analisar os estados vizinhos do current state
        for next_state, (row, col) in current_state.get_neighbors():
            next_hash = hash(next_state)
            next_g = g + 1
            
            # se o state já tiver sido alcançado anteriormente,
            # mas agora com custo menor, é colocado na queue
            if next_g < best_g.get(next_hash, float('inf')):
                best_g[next_hash] = next_g
                counter += 1
                next_f = next_g + weight * heuristic(next_state)
                heapq.heappush(heap, (next_f, counter, next_g, next_state, moves + [(row, col)]))
 
    return None
 
 
def lights_on_count(state):

    # Número de luzes acesas é usado como heurística, pois cada move altera no
    # máximo 5 quadrados, portanto no mínimo serão usados ("lights_on" / 5) moves.
    return sum(cell for row in state.board for cell in row)