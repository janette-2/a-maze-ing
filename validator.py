""" Maze validations """

from maze import Maze, NORTH, EAST, SOUTH, WEST, DELTA


# ** exit_ is written like that to avoid conflicts between the variable
#  and the exit() function when called
def validate_maze(maze: Maze, entry: tuple[int, int],
                  exit_: tuple[int, int],
                  blocked: set[tuple[int, int]]) -> None:
    """ Run all validations on a generated maze

    Args:
        maze: The Maze object to validate
        entry: Entry coodinates (x, y)
        exit_: Exit coordinates (x, y)
        blocked: Set of cells belonging to the 42 pattern

    Raises:
        ValueError: If any validation fails
    """
    # Private functions (_function_name),
    # they can't be accessed from other modules when imported
    _validate_coherence(maze)
    _validate_borders(maze, entry, exit_)
    _validate_no_large_open_areas(maze, blocked)
    _validate_connectivity(maze, entry, blocked)


def _validate_coherence(maze: Maze) -> None:
    """ Check that neighbour cells share coherent walls

    If cell A has its East wall closed, cell B to the right
    should have its West wall closed, and vice versa.

    Args:
        maze: The Maze object to validate

    Raises:
        ValueError: If any inconsistency is found
    """
    for y in range(maze.height):
        for x in range(maze.width):
            # Check East-West coherence
            if x + 1 < maze.width:
                # Checks if the actual wall was closed in the EAST
                east_closed = bool(maze.grid[y][x] & EAST)
                west_closed = bool(maze.grid[y][x + 1] & WEST)
                # If one is closed the next one should be closed too
                if east_closed != west_closed:
                    raise ValueError(
                        f"Wall coherence error at ({x},{y}): "
                        f"East = {east_closed} but "
                        f"({x + 1},{y}) West = {west_closed}"
                    )
            # Checks South-North coherence
            if y + 1 < maze.height:
                south_closed = bool(maze.grid[y][x] & SOUTH)
                north_closed = bool(maze.grid[y + 1][x] & NORTH)
                # If one is closed the next one should be closed too
                if south_closed != north_closed:
                    raise ValueError(
                        f"Wall coherence error at ({x},{y}): "
                        f"South={south_closed} but "
                        f"({x},{y+1}) North={north_closed}"
                    )


def _validate_borders(maze: Maze, entry: tuple[int, int],
                      exit_: tuple[int, int]) -> None:
    """ Check that external border walls are closed

    Border cells must have their outer walls closed except
    at the entry and exit points

    Args:
        maze: The Maze object to validate
        entry: Entry coordinates (x, y)
        exit_: Exit coordinates (x, y)

    Raises:
        ValueError: If a border wall is incorrectly open
        """

    # The cells of exit and entry (special) can have their border walls open
    special = {entry, exit_}

    # Checks the top and border rows borders
    for x in range(maze.width):
        if (x, 0) not in special:
            # If the north wall is open at the top...
            if not bool(maze.grid[0][x] & NORTH):
                raise ValueError(
                    f"Border error: North wall open at ({x}, 0)"
                )
        # If the south wall is open at the bottom...
        if (x, maze.height - 1) not in special:
            if not bool(maze.grid[maze.height - 1][x] & SOUTH):
                raise ValueError(
                    f"Border error: South wall open at "
                    f"({x}, {maze.height - 1})"
                )

    # Checks the left and right borders of the maze
    for y in range(maze.height):
        # If the west wall is open at the left border...
        if (0, y) not in special:
            if not bool(maze.grid[y][0] & WEST):
                raise ValueError(
                    f"Border error: West wall open at (0, {y})"
                )
        # If the east wall is open at the right border...
        if (maze.width - 1, y) not in special:
            if not bool(maze.grid[y][maze.width - 1] & EAST):
                raise ValueError(
                    f"Border error: East wall open at "
                    f"({maze.width - 1}, {y})"
                )


def _validate_no_large_open_areas(maze: Maze,
                                  blocked: set[tuple[int, int]]) -> None:
    """Check that no 3x3 area is completely open.

    Corridors can't be wider than 2 cells in both dimensions
    simultaneously. 2x3 or 3x2 areas are allowed, but never 3x3.

    Args:
        maze: The Maze object to validate.
        blocked: Set of cells belonging to the 42 pattern.

    Raises:
        ValueError: If a 3x3 open area is found.
    """
    for y in range(maze.height - 2):
        for x in range(maze.width - 2):
            is_blocked = any((x + dx, y + dy) in blocked
                             for dx in range(3) for dy in range(3))
            if is_blocked:
                continue

            open_area = True
            for dy in range(3):
                for dx in range(3):
                    cx, cy = x + dx, y + dy
                    if dx < 2 and bool(maze.grid[cy][cx] & EAST):
                        open_area = False
                        break
                    if dy < 2 and bool(maze.grid[cy][cx] & SOUTH):
                        open_area = False
                        break
                if not open_area:
                    break

            if open_area:
                raise ValueError(
                    f"Large open area (3x3) detected at ({x}, {y})"
                )


def _validate_connectivity(maze: Maze, entry: tuple[int, int],
                           blocked: set[tuple[int, int]]) -> None:
    """ Check that all non-blocked cells are reachable from entry

    Uses BFS from the entry point to verify full connectivity

    Args:
        maze: The Maze object to validate
        entry: Entry coordinates (x, y)
        blocked: Set of cells belonging to the 42 pattern

    Raises:
        ValueError: If any non-blocked cell is unreachable
    """
    from collections import deque

    visited: set[tuple[int, int]] = set()
    queue: deque[tuple[int, int]] = deque([entry])
    visited.add(entry)

    while queue:
        x, y = queue.popleft()
        for direction in [NORTH, EAST, SOUTH, WEST]:
            dx, dy = DELTA[direction]
            nx, ny = x + dx, y + dy
            if (maze.is_inside(nx, ny)
                    and (nx, ny) not in visited
                    and (nx, ny) not in blocked
                    and not maze.has_wall(x, y, direction)):
                visited.add((nx, ny))
                queue.append((nx, ny))

    # All non-blocked cells must be reachable
    total_cells = maze.width * maze.height
    reachable = len(visited)
    expected = total_cells - len(blocked)

    if reachable != expected:
        raise ValueError(
            f"Connectivity error: {reachable} cells reachable "
            f"but expected {expected} ({total_cells} total"
            f" - {len(blocked)} blocked)"
        )
