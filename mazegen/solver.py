""" Maze solver using BFS (Breadth First Search) for A-Maze-ing """

from collections import deque
from .maze import Maze, NORTH, EAST, SOUTH, WEST, DELTA


def solve(maze: Maze, entry: tuple[int, int],
          exit_: tuple[int, int]) -> str:
    """ Find the shortest path from entry to exit using BFS

    Args:
        maze: The Maze object to solve
        entry: Entry coordinates (x, y)
        exit_: Exit coordinates (x, y)

    Returns:
        A string of N/E/S/W letters representing the shortest path.
        Returns an empty string if no path exists.
    """
    # Each queue item is (x, y, path_so_far)
    queue: deque[tuple[int, int, str]] = deque([(entry[0], entry[1], "")])
    visited: set[tuple[int, int]] = {entry}

    # Direction letters for the path string
    letters: dict[int, str] = {
        NORTH: 'N',
        EAST: 'E',
        SOUTH: 'S',
        WEST: 'W'
    }

    while queue:
        x, y, path = queue.popleft()

        if (x, y) == exit_:
            return path

        for direction in [NORTH, EAST, SOUTH, WEST]:
            dx, dy = DELTA[direction]
            nx, ny = x + dx, y + dy
            if (maze.is_inside(nx, ny)
                and (nx, ny) not in visited and not maze.has_wall(
                    x, y, direction)):
                visited.add((nx, ny))
                queue.append((nx, ny, path + letters[direction]))

    return ""
