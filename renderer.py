""" ASCII renderer for the visual representation of the maze"""
from maze import Maze, NORTH, SOUTH, WEST

# ANSI color code for terminal output
COLORS: dict[str, str] = {
    "white":  "\033[97m",
    "red":    "\033[91m",
    "green":  "\033[92m",
    "yellow": "\033[93m",
    "blue":   "\033[94m",
    "reset":  "\033[0m",
}

# Characters used to draw the maze
WALL_H = "--"  # horizontal wall
WALL_V = "|"  # vertical wall
CORNER = "+"  # corner
SPACE = " "  # open corridor
PATH = "░░"  # path cell
ENTRY_CHAR = "EN"  # entry marker
EXIT_CHAR = "EX"  # exit marker
SOLID = "██"  # solid cell (in the 42 pattern)


def render(maze: Maze, entry: tuple[int, int],
           exit_: tuple[int, int],
           path_cells: set[tuple[int, int]],
           blocked: set[tuple[int, int]],
           wall_color: str = "white",
           show_path: bool = False) -> str:
    """ Render the maze as an ASCII string
    Args:
        maze: The Maze object to render.
        entry: Entry coordinates (x, y).
        exit_: Exit coordinates (x, y).
        path_cells: Set of (x, y) cells that form the solution path.
        blocked: Set of (x, y) cells belonging to the 42 pattern.
        wall_color: Color name for walls. Must be a key in COLORS.
        show_path: If True, highlights the solution path.

    Returns:
        A string containing the full ASCII representation of the maze
    """
    color = COLORS.get(wall_color, COLORS["white"])
    reset = COLORS["reset"]

    lines: list[str] = []

    for y in range(maze.height):
        # Top border of this row
        top_line = ""
        for x in range(maze.width):
            top_line += color + CORNER + reset
            if maze.has_wall(x, y, NORTH):
                top_line += color + WALL_H + reset
            else:
                top_line += SPACE
        top_line += color + CORNER + reset
        lines.append(top_line)

        # Cell content of this row
        cell_line = ""
        for x in range(maze.width):
            # Left wall
            if maze.has_wall(x, y, WEST):
                cell_line += color + WALL_V + reset
            else:
                cell_line += " "

            # Cell content
            if (x, y) == entry:
                cell_line += "\033[92m" + ENTRY_CHAR + reset
            elif (x, y) == exit_:
                cell_line += "\033[91m" + EXIT_CHAR + reset
            elif (x, y) in blocked:
                cell_line += color + SOLID + reset
            elif show_path and (x, y) in path_cells:
                cell_line += "\033[94m" + PATH + reset
            else:
                cell_line += SPACE

        # Right border
        cell_line += color + WALL_V + reset
        lines.append(cell_line)

    # Bottom border
    bottom_line = ""
    for x in range(maze.width):
        bottom_line += color + CORNER + reset
        if maze.has_wall(x, maze.height - 1, SOUTH):
            bottom_line += color + WALL_H + reset
        else:
            bottom_line += SPACE
    bottom_line += color + CORNER + reset
    lines.append(bottom_line)

    return "\n".join(lines)


def path_to_cells(entry: tuple[int, int],  path: str) -> set[tuple[int, int]]:
    """ Convert a path string to a set of cell coordinates

    Args:
        entry: Starting coordinates (x, y)
        path: Path string of N/E/S/W letters

    Returns:
        A set of (x, y) coordinates visited along the path
    """
    deltas: dict[str, tuple[int, int]] = {
        'N': (0, -1),
        'E': (1, 0),
        'S': (0, 1),
        'W': (-1, 0),
    }

    cells: set[tuple[int, int]] = {entry}
    x, y = entry

    for letter in path:
        dx, dy = deltas[letter]
        x, y = x + dx, y + dy
        cells.add((x, y))

    return cells
