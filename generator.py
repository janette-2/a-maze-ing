""" Maze generator using the Recursive Backtracker algorithm """
import random
from maze import Maze, NORTH, EAST, SOUTH, WEST, OPPOSITE, DELTA


def generate(maze: Maze, seed: int, perfect: bool,
             blocked: set[tuple[int, int]] | None = None) -> None:
    """ Generates a maze using the Recursive Backtracker algorithm

    Starts from cell (0, 0) and carves passages using an iterative
    depth-first search with a stack. Uses a seed for reproducibility.

    Args:
        maze: The Maze object to generate, modified in place
        seed: Random seed for reproducibility
        perfect: If True, generates a perfect maze (one path between
                 any two cells). If False, adds extra passages.
        blocked : Set of (x, y) cells to skip during generation,
                  reserved to place the '42' pattern. Accepts the
                  set of tuples with the pattern or None, but as
                  default is set to (= None)
    """
    rng = random.Random(seed)

    # Track visited cells, at start, fills the maze with 'False'
    visited: list[list[bool]] = [
        [False] * maze.width for _ in range(maze.height)
    ]

    # Checks if the pattern '42' doesn't fit
    if blocked is None:
        blocked = set()

    # If it fits, keeps the cells for the '42' as visited:
    for x, y in blocked:
        visited[y][x] = True

    # Starts searching the path from the top-left corner
    start_x, start_y = 0, 0
    visited[start_y][start_x] = True

    # Keep the visited cells in 'stack'
    stack: list[tuple[int, int]] = [(start_x, start_y)]

    # It keeps digging until there are no more elements
    # in the visited tracking list, meaning that every path
    # has been seen already, so the maze is complete
    while stack:
        # Gets the last element in the list
        x, y = stack[-1]

        # Find near unvisited cells
        neighbours: list[tuple[int, int, int]] = []
        for direction in [NORTH, EAST, SOUTH, WEST]:
            dx, dy = DELTA[direction]
            nx, ny = x + dx, y + dy
            if maze.is_inside(nx, ny) and not visited[ny][nx]:
                neighbours.append((nx, ny, direction))

        if neighbours:
            # Select a random near cell with the random generator
            nx, ny, direction = rng.choice(neighbours)

            # Creates random path in the maze by removing the walls
            # of random unvisited neighbours
            maze.remove_wall(x, y, direction)
            maze.remove_wall(nx, ny, OPPOSITE[direction])

            # Mark the open path as visited and store in the stack
            visited[ny][nx] = True
            stack.append((nx, ny))

        else:
            # When there are no more unvisited neighbours forward,
            # it gets back to the last previous element and deletes
            # the last one because it has no unvisited options
            stack.pop()

    # Ensure that all the border walls are closed
    _close_borders(maze)

    # If the maze is not meant to only have a unique path between
    # two cells, if there can be alternatives to connect the
    # same cells (unperfect)
    if not perfect:
        _add_extra_passage(maze, rng)


def _add_extra_passage(maze: Maze, rng: random.Random) -> None:
    """ Add random extra passages to create a non-perfect maze

    Removes additional walls to create loops and multiple paths

    Args:
        maze: The Maze object to modify in place
        rng: Random number generator instance
    """
    # Remove a small percentage of walls (10%) to create
    # alternative paths
    extra = (maze.width * maze.height) // 10

    for _ in range(extra):
        # Avoids bounds and last row/column to not open
        # walls in the bounds limits
        x = rng.randint(0, maze.width - 2)
        y = rng.randint(0, maze.height - 2)

        # Randomly picks a wall in every direction to remove
        if rng.choice([True, False]):
            # Opens a path horizontally if 'True'
            maze.remove_wall(x, y, EAST)
            maze.remove_wall(x + 1, y, WEST)
        else:
            # Opens a path vertically if 'False'
            maze.remove_wall(x, y, SOUTH)
            maze.remove_wall(x, y + 1, NORTH)


def _close_borders(maze: Maze) -> None:
    """ Ensure all external border walls are closed

        Args:
            maze: The Maze object to modify in place
    """
    # Top and bottom rows
    for x in range(maze.width):
        maze.add_wall(x, 0, NORTH)
        maze.add_wall(x, maze.height - 1, SOUTH)

    # Left and right columns
    for y in range(maze.height):
        maze.add_wall(0, y, WEST)
        maze.add_wall(maze.width - 1, y, EAST)
