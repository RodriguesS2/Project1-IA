from state import LightsOutState


def solve_bfs(initial_state):
    if initial_state.is_goal():
        return []
    
    #queue guarda tuplos com estado atual e caminho (usado deque para facilitar remoção de elementos)
    queue = deque([(initial_state, [])])
    
    #funciona com set graças ao hash e eq 
    visited = set([initial_state])

    while queue:
        current_state, path = queue.popleft()

        for next_state, move in current_state.get_neighbors():
            if next_state not in visited:
                
                #o prox passo é a solução
                if next_state.is_goal():
                    return path + [move]
                
                visited.add(next_state)
                queue.append((next_state, path + [move]))
                
    return None


def solve_dfs(initial_state):
    pass


def solve_astar(initial_state, heuristic=None):
    """
    Solve the board using A* search.

    Args:
        initial_state: LightsOutState
        heuristic:     function(state) -> int  (defaults to lights_on_count)

    Returns:
        List of (row, col) moves that lead to the goal, or None if unsolvable.
    """
    pass


def lights_on_count(state):
    """
    Heuristic: number of lights still on.
    Simple admissible estimate — each move toggles at most 5 lights.
    """
    pass