""" Creation of the 42 pattern in the maze"""

from maze import Maze

# Each digit is defined as a grid of 1s (solid) and 0s (empty)
# 1 = fully closed cell (all walls), 0 = normal cell
DIGIT_4: list[list[int]] = [
    [1, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 0, 1],
    [0, 0, 1],
]

DIGIT_2: list[list[int]] = [
    [1, 1, 1],
    [0, 0, 1],
    [1, 1, 1],
    [1, 0, 0],
    [1, 1, 1],
]

# Minimum maze size required to fit the pattern
PATTERN_WIDTH: int = 7   # 3 (digit '4') + 1 (gap) + 3 (digit '2')
PATTERN_HEIGHT: int = 5  # height of each digit
MIN_MAZE_WIDTH: int = PATTERN_WIDTH + 4   # pattern + margins
MIN_MAZE_HEIGHT: int = PATTERN_HEIGHT + 4  # pattern + margins


def can_embed_pattern(maze: Maze) -> bool:
    """ Checks if the '42' pattern fits in the maze configuration

    Args:
        maze: The Maze object to check.

    Returns:
        True if the pattern fits a '42' with margins, False otherwise.
    """
    return maze.width >= MIN_MAZE_WIDTH and maze.height >= MIN_MAZE_HEIGHT


def get_pattern_cells(maze: Maze) -> set[tuple[int, int]]:
    """ Get the set of cells that form the 42 pattern

    The pattern is centered in the maze

    Args:
        maze: The Maze object to embed the pattern in

    Returns:
        A set of (x, y) coordinates that belong to the pattern
    """

    # Finds the middle to place the pattern in the maze and get the
    # entire measurements. Returns a positive integer
    start_x = (maze.width - PATTERN_WIDTH) // 2
    start_y = (maze.height - PATTERN_HEIGHT) // 2

    cells: set[tuple[int, int]] = set()

    # Add the corresponding cells in the maze to place
    # the digit '4'. Enumerate returns the index of each
    # list that forms the '4' matrix, as well as the content of the
    # indexed list selected, returning each list component in order
    for row_index, row in enumerate(DIGIT_4):
        # Now enumerate returns each component inside the list
        for col_index, cell in enumerate(row):
            if cell == 1:
                x = start_x + col_index
                y = start_y + row_index
                cells.add((x, y))

    # Adss the corresponding cells in the maze to put the
    # digit '2'. This digit, compared to the starting reference,
    # is placed in an offset of 4 digits (3 for the width of '4'
    # and 1 for the gap) to the right of the starting point.
    for row_index, row in enumerate(DIGIT_2):
        for col_index, cell in enumerate(row):
            if cell == 1:
                x = start_x + 4 + col_index
                y = start_y + row_index
                cells.add((x, y))

    return cells


def embed_pattern(maze: Maze) -> set[tuple[int, int]]:
    """ Embed the 42 pattern into the maze by closing all walls

    Pattern cells will have all four walls closed (value: 0xF (15))
    These cells will be marked as visited before the generation of
    the maze paths, to avoid touching these cells.

    Args:
        maze: The Maze object to modify

    Returns:
        The set of (x, y) coordinates that belong to the pattern.
        Returns an empty set if the maze is too small
    """

    if not can_embed_pattern(maze):
        print(
            "Warning: maze is too small to embed the 42 pattern "
            f"(minimum size: {MIN_MAZE_WIDTH}x{MIN_MAZE_HEIGHT})"
        )
        return set()

    # Get the cells to place the pattern in
    cells = get_pattern_cells(maze)

    # Close all walls on pattern cells
    for x, y in cells:
        maze.grid[y][x] = 0xF

    return cells
