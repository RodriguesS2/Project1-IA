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