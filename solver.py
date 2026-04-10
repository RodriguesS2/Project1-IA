from state import LightsOutState


def solve_bfs(initial_state):
    """
    Solve the board using Breadth-First Search.

    Args:
        initial_state: LightsOutState

    Returns:
        List of (row, col) moves that lead to the goal, or None if unsolvable.
    """
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

def solve_ids(initial_state,max_depth=100):
    if initial_state.is_goal():
        return []
    for depth_limit in range(max_depth + 1):
        explored = set()
        result = dls(initial_state, depth_limit, explored)
        if result is not None:
            return result

    return None

def dls(initial_state,depth_limit,explored,path=None):
    if path is None:
        path=[]
    if initial_state.is_goal():
        return path 
    if depth_limit == 0:
        return None
    
    explored.add(initial_state)
    for neighbor,move in initial_state.get_neighbors():
        if neighbor not in explored:
            new_path = path + [move]
            result = dls(neighbor, depth_limit - 1, explored.copy(), new_path)
            if result is not None:
                return result
    return None

def solve_ucs(initial_state):
    if initial_state.is_goal():
        return []
    
    c = 0
    to_visit = [(0, c, initial_state, [])]
    explored = set()

    best_cost = {initial_state: 0}

    while to_visit:
        cost,_,current_state,path=heapq.heappop(to_visit) 

        if current_state.is_goal():
            return path
        
        if current_state in explored:
            continue

        explored.add(current_state)

        for neighbor, move in current_state.get_neighbors():
            new_cost=cost+1
            if neighbor not in best_cost or new_cost<best_cost[neighbor]:
                best_cost[neighbor]=new_cost
                new_path=path+[move]
                c+=1
                heapq.heappush(to_visit, (new_cost, c, neighbor, new_path))
        
        return None
    
def solve_greedy(initial_state, heuristic=None):
    if heuristic is None:
        heuristic = lights_on_count

    if initial_state.is_goal():
        return []

    c = 0
    to_visit = [(heuristic(initial_state), c, initial_state, [])]
    explored = set()

    while to_visit:
        h_score, _, current_state, path = heapq.heappop(to_visit)

        if current_state.is_goal():
            return path

        if current_state in explored:
            continue

        explored.add(current_state)

        for neighbor, move in current_state.get_neighbors():
            if neighbor not in explored:
                new_path = path + [move]
                h = heuristic(neighbor)
                c += 1
                heapq.heappush(to_visit, (h, c, neighbor, new_path))

    return None
