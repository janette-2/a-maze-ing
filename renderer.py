""" ASCII renderer for the visual representation of the maze"""
from maze import Maze, NORTH, SOUTH, WEST, EAST

# ANSI color code for terminal output
COLORS: dict[str, str] = {
    "white":  "\033[97m",
    "red":    "\033[91m",
    "green":  "\033[92m",
    "yellow": "\033[93m",
    "blue":   "\033[94m",
    "reset":  "\033[0m",
    "bright_yellow": "\033[93;1m",  # negrita + amarillo = más neón
}

# Characters used to draw the maze
SPACE = " "  # open corridor
PATH = "░"  # path cell
ENTRY_CHAR = "I"  # entry marker
EXIT_CHAR = "O"  # exit marker
SOLID = "█"  # solid cell (in the 42 pattern)

# Unicode box characters indexed by (up, down, left, right)
# Each bool means, in this intersection of 4 cells, (+ all closed)
# "is there a line going in that direction?"
CORNER_CHARS: dict[tuple[bool, bool, bool, bool], str] = {
    (False, False, False, False): " ",
    (True,  False, False, False): "╵",
    (False, True,  False, False): "╷",
    (True,  True,  False, False): "│",
    (False, False, True,  False): "╴",
    (False, False, False, True): "╶",
    (False, False, True,  True): "─",
    (True,  False, True,  False): "┘",
    (True,  False, False, True): "└",
    (False, True,  True,  False): "┐",
    (False, True,  False, True): "┌",
    (True,  True,  True,  False): "┤",
    (True,  True,  False, True): "├",
    (True,  False, True,  True): "┴",
    (False, True,  True,  True): "┬",
    (True,  True,  True,  True): "┼",
}


def _get_corner(maze: Maze, cx: int, cy: int) -> str:
    """Return the correct Unicode character for a grid intersection.

    Each intersection (cx, cy) sits at the corner of up to four cells:
        top-left:     cell (cx-1, cy-1)
        top-right:    cell (cx,   cy-1)
        bottom-left:  cell (cx-1, cy  )
        bottom-right: cell (cx,   cy  )

    We check whether each of the four neighbouring cells has a wall
    facing this corner, then pick the matching box character.

    Args:
        maze: The Maze object.
        cx: Corner column (0 to maze.width).
        cy: Corner row (0 to maze.height).

    Returns:
        The correct Unicode box-drawing character.
    """
    # Does a line go upward from this corner?
    # Yes if the cell to the top-left has its East wall,
    # or the cell to the top-right has its West wall.
    up = (
        (cx > 0 and cy > 0 and maze.has_wall(cx - 1, cy - 1, EAST))
        or
        (cx < maze.width and cy > 0 and maze.has_wall(cx, cy - 1, WEST))
    )

    # Does a line go downward from this corner?
    down = (
        (cx > 0 and cy < maze.height and maze.has_wall(cx - 1, cy, EAST))
        or
        (cx < maze.width and cy < maze.height and maze.has_wall(cx, cy, WEST))
    )

    # Does a line go leftward from this corner?
    left = (
        (cx > 0 and cy > 0 and maze.has_wall(cx - 1, cy - 1, SOUTH))
        or
        (cx > 0 and cy < maze.height and maze.has_wall(cx - 1, cy, NORTH))
    )

    # Does a line go rightward from this corner?
    right = (
        (cx < maze.width and cy > 0 and maze.has_wall(cx, cy - 1, SOUTH))
        or
        (cx < maze.width and cy < maze.height and maze.has_wall(cx, cy, NORTH))
    )

    return CORNER_CHARS[(up, down, left, right)]


def render(maze: Maze, entry: tuple[int, int],
           exit_: tuple[int, int],
           path_cells: set[tuple[int, int]],
           blocked: set[tuple[int, int]],
           wall_color: str = "white",
           show_path: bool = False) -> str:
    """Render the maze as a Unicode box-drawing string

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
    green = COLORS["green"]
    red = COLORS["red"]
    blue = COLORS["blue"]

    lines: list[str] = []

    for y in range(maze.height + 1):

        # --- Intersection + horizontal wall row ---
        h_line = ""
        for x in range(maze.width + 1):
            # Corner character at intersection (x, y)
            h_line += color + _get_corner(maze, x, y) + reset

            # Horizontal wall to the right of this corner
            if x < maze.width:
                if y == 0 or y == maze.height:
                    # Always draw top and bottom borders
                    h_line += color + "─" + reset
                elif maze.has_wall(x, y, NORTH):
                    h_line += color + "─" + reset
                else:
                    h_line += " "
        lines.append(h_line)

        # --- Cell content row ---
        if y < maze.height:
            c_line = ""
            for x in range(maze.width):
                # Vertical wall to the left of this cell
                if x == 0 or maze.has_wall(x, y, WEST):
                    c_line += color + "│" + reset
                else:
                    c_line += " "

                # Cell content
                if (x, y) == entry:
                    c_line += green + ENTRY_CHAR + reset
                elif (x, y) == exit_:
                    c_line += red + EXIT_CHAR + reset
                elif (x, y) in blocked:
                    c_line += "\033[93;1m" + SOLID + reset
                elif show_path and (x, y) in path_cells:
                    c_line += blue + PATH + reset
                else:
                    c_line += SPACE

            # Right border
            c_line += color + "│" + reset
            lines.append(c_line)

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
