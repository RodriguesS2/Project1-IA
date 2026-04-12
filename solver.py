from state import LightsOutState
import heapq
from collections import deque

def solve_bfs(initial_state):
    if initial_state.is_goal():
        return [], {"states_analyzed": 0, "max_memory": 0}

    #queue guarda tuplos com estado atual e caminho (usado deque para facilitar remoção de elementos)
    queue = deque([(initial_state, [])])

    #funciona com set graças ao hash e eq
    visited = set([initial_state])

    states_analyzed = 0
    max_memory = 1  #começa com 1 elemento na queue

    while queue:
        current_state, path = queue.popleft()
        states_analyzed += 1  #cada pop é um estado analisado

        for next_state, move in current_state.get_neighbors():
            if next_state not in visited:

                #o prox passo é a solução
                if next_state.is_goal():
                    return path + [move], {
                        "states_analyzed": states_analyzed,
                        "max_memory": max_memory
                    }

                visited.add(next_state)
                queue.append((next_state, path + [move]))

        max_memory = max(max_memory, len(queue))  #mede após adicionar vizinhos

    return None, {"states_analyzed": states_analyzed, "max_memory": max_memory}


def solve_dfs(initial_state):
    if initial_state.is_goal():
        return [], {"states_analyzed": 0, "max_memory": 0}

    #a stack guarda tuplos com estado, caminho
    stack = [(initial_state, [])]
    visited = set([initial_state])

    states_analyzed = 0
    max_memory = 1

    while stack:
        #ir buscar ultimo elemento adicionado
        current_state, path = stack.pop()
        states_analyzed += 1

        if current_state.is_goal():
            return path, {"states_analyzed": states_analyzed, "max_memory": max_memory}

        for next_state, move in current_state.get_neighbors():
            if next_state not in visited:
                visited.add(next_state)
                stack.append((next_state, path + [move]))

        max_memory = max(max_memory, len(stack))

    return None, {"states_analyzed": states_analyzed, "max_memory": max_memory}


def solve_astar(initial_state, heuristic=None, weight = 1.0):

    if heuristic is None:
        heuristic = lights_on_count

    if initial_state.is_goal():
        return [], {"states_analyzed": 0, "max_memory": 0}

    # priority queue: (f, counter, g, state, moves)
    # f = g + h  (custo total estimado)
    # g = moves realizados até ao momento (custo atual)
    # h = heuristica
    # counter serve de desempate para o Python não comparar LightsOutState objects
    counter = 0
    heap = []
    heapq.heappush(heap, (heuristic(initial_state), counter, 0, initial_state, []))

    # Mapeia state hash -> melhor g (custo) até ao momento
    best_g = {hash(initial_state): 0}

    states_analyzed = 0
    max_memory = 1

    while heap:
        # Dá pop ao estado com menor f (custo total estimado)
        f, _, g, current_state, moves = heapq.heappop(heap)
        states_analyzed += 1

        if current_state.is_goal():
            return moves, {"states_analyzed": states_analyzed, "max_memory": max_memory}

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

        max_memory = max(max_memory, len(heap))

    return None, {"states_analyzed": states_analyzed, "max_memory": max_memory}

def solve_ids(initial_state, max_depth=100):
    if initial_state.is_goal():
        return [], {"states_analyzed": 0, "max_memory": 0}

    total_states_analyzed = 0
    total_max_memory = 0

    for depth_limit in range(max_depth + 1):
        explored = set()
        result, states_analyzed, max_memory = dls(initial_state, depth_limit, explored)

        total_states_analyzed += states_analyzed
        total_max_memory = max(total_max_memory, max_memory)

        if result is not None:
            return result, {
                "states_analyzed": total_states_analyzed,
                "max_memory": total_max_memory
            }

    return None, {"states_analyzed": total_states_analyzed, "max_memory": total_max_memory}


def dls(initial_state,depth_limit,explored,path=None):
    if path is None:
        path = []

    states_analyzed = 1  #este nó está a ser analisado agora
    max_memory = len(explored)

    if initial_state.is_goal():
        return path, states_analyzed, max_memory

    if depth_limit == 0:
        return None, states_analyzed, max_memory

    explored.add(initial_state)

    for neighbor, move in initial_state.get_neighbors():
        if neighbor not in explored:
            new_path = path + [move]
            result, child_states, child_memory = dls(neighbor, depth_limit - 1, explored.copy(), new_path)

            states_analyzed += child_states
            max_memory = max(max_memory, child_memory)

            if result is not None:
                return result, states_analyzed, max_memory

    return None, states_analyzed, max_memory


def solve_ucs(initial_state):
    if initial_state.is_goal():
        return [], {"states_analyzed": 0, "max_memory": 0}

    c = 0
    to_visit = [(0, c, initial_state, [])]
    explored = set()

    best_cost = {initial_state: 0}

    states_analyzed = 0
    max_memory = 1

    while to_visit:
        cost, _, current_state, path = heapq.heappop(to_visit)
        states_analyzed += 1

        if current_state.is_goal():
            return path, {"states_analyzed": states_analyzed, "max_memory": max_memory}

        if current_state in explored:
            continue

        explored.add(current_state)

        for neighbor, move in current_state.get_neighbors():
            new_cost = cost + 1
            
            if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                best_cost[neighbor] = new_cost
                new_path = path + [move]
                c += 1
                heapq.heappush(to_visit, (new_cost, c, neighbor, new_path))

        max_memory = max(max_memory, len(to_visit))

    return None, {"states_analyzed": states_analyzed, "max_memory": max_memory}


def solve_greedy(initial_state, heuristic=None):
    if heuristic is None:
        heuristic = lights_on_count

    if initial_state.is_goal():
        return [], {"states_analyzed": 0, "max_memory": 0}

    c = 0
    to_visit = [(heuristic(initial_state), c, initial_state, [])]
    explored = set()

    states_analyzed = 0
    max_memory = 1

    while to_visit:
        h_score, _, current_state, path = heapq.heappop(to_visit)
        states_analyzed += 1

        if current_state.is_goal():
            return path, {"states_analyzed": states_analyzed, "max_memory": max_memory}

        if current_state in explored:
            continue

        explored.add(current_state)

        for neighbor, move in current_state.get_neighbors():
            if neighbor not in explored:
                new_path = path + [move]
                h = heuristic(neighbor)
                c += 1
                heapq.heappush(to_visit, (h, c, neighbor, new_path))

        max_memory = max(max_memory, len(to_visit))

    return None, {"states_analyzed": states_analyzed, "max_memory": max_memory}


def lights_on_count(state):

    # Número de luzes acesas é usado como heurística, pois cada move altera no
    # máximo 5 quadrados, portanto no mínimo serão usados ("lights_on" / 5) moves.
    return sum(cell for row in state.board for cell in row)


def parity_heuristic(state):
 
    # Luzes nos cantos só são afetadas por 2 moves cada, nas arestas por 3,
    # e no centro por 4 ou 5. Penalizamos mais as luzes difíceis de apagar.
    corner_weight = 1.0   # cantos: apenas 2 moves as afetam
    edge_weight = 0.6     # arestas: 3 moves as afetam
    center_weight = 0.4   # centro: 4-5 moves as afetam
 
    size = state.size
    last = size - 1
    total = 0.0
 
    for row in range(size):
        for col in range(size):
            if state.board[row][col] == 1:
                is_corner = (row in (0, last)) and (col in (0, last))
                is_edge = (row in (0, last)) or (col in (0, last))
 
                if is_corner:
                    total += corner_weight
                
                elif is_edge:
                    total += edge_weight
                
                else:
                    total += center_weight
 
    return total


def isolated_lights_heuristic(state):
 
    #luzes isoladas (sem vizinhos acesos) são mais difícil de apagar,
    #pois al clicas acendemos as celulas adjacentes
    isolated_weight = 2.0   #luz acesa sem nenhum vizinho aceso (mais pesada)
    grouped_weight  = 0.5   #luz acesa com pelo menos um vizinho aceso
 
    size = state.size
    total = 0.0
    neighbors_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)] #pos dos vizinhos
 
    for row in range(size):
        for col in range(size):
            if state.board[row][col] == 1:
                has_lit_neighbor = any(
                    0 <= row + pos_row < size and 0 <= col + pos_col < size and state.board[row + pos_row][col + pos_col] == 1
                    for pos_row, pos_col in neighbors_offsets
                )
                
                total += grouped_weight if has_lit_neighbor else isolated_weight
 
    return total