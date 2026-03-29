"""Maze data structure for A-Maze-ing."""

# Wall constants — each bit put as '1' represents
# a wall in the cell's structure
NORTH: int = 1  # bit 0 -> 0001 (N)
EAST: int = 2   # bit 1 -> 0010 (E)
SOUTH: int = 4  # bit 2 -> 0100 (S)
WEST: int = 8   # bit 3 -> 1000 (W)

# Opposite direction of each wall, to create the cell on the side
OPPOSITE: dict[int, int] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

# Movement deltas for each direction (dx, dy)
# represents a movement in each direction (x:column, y:row)
DELTA: dict[int, tuple[int, int]] = {
    NORTH: (0, -1),
    EAST: (1, 0),
    SOUTH: (0, 1),
    WEST: (-1, 0),
}


class Maze:
    """
    Represents a maze as a 2D grid of cells.

    Each cell is an integer where each bit represents a wall:
        bit 0 (value 1) = North wall closed
        bit 1 (value 2) = East wall closed
        bit 2 (value 4) = South wall closed
        bit 3 (value 8) = West wall closed

    A bit set to 1 means the wall is closed (solid).
    A bit set to 0 means the wall is open (passage).
    """

    def __init__(self, width: int, height: int) -> None:
        """Initialize a maze with all walls closed

        Args:
            width: Number of columns in the maze
            height: Number of rows in the maze
        """
        self.width = width
        self.height = height
        # 0xF = 1111 = (HEX:F)15 = all four walls closed
        self.grid: list[list[int]] = [
            # Fills each row (height) with '15' for each column (width)
            [0xF] * width for _ in range(height)
        ]

    def has_wall(self, x: int, y: int, direction: int) -> bool:
        """ Check if a cell has a wall in the given direction

        Args:
            x: Column of the cell
            y: Row of the cell
            direction: One of NORTH, EAST, SOUTH, WEST

        Returns:
            True if the wall is closed, False if open.
        """
        # Makes a bit operation, multiplies the values of a cell
        # by the representation of the direction they are going.
        # For example, if a cell is set to 13 -> 1101 (W,S,E,N)
        # and we mask the bits of the cell with the desired going direction:
        # 1101 & 0001(N) -> True -> has a wall in that direction
        # 1101 & 0010 (E) -> False -> doesn't have a wall in that direction
        return bool(self.grid[y][x] & direction)

    def remove_wall(self, x: int, y: int, direction: int) -> None:
        """ Open a wall in the given direction

        Args:
            x: Column of the cell
            y: Row of the cell
            direction: One of NORTH, EAST, SOUTH, WEST
        """
        # The ~direction, is an expression to flip the value of the
        # bits in direction. If the original was: direction = 1000
        # with ~direction it would be: ~direction = 0111

        # This operation would force the value of the given direction
        # in the cell to be '0', making the specific wall open.
        # Ex: cell = 1111, direction = 0100 (S), ~direction = 1011
        # result = 1111 & 1011 = 1011
        self.grid[y][x] = self.grid[y][x] & ~direction

    def add_wall(self, x: int, y: int, direction: int) -> None:
        """ Close a wall in the given direction

        Args:
            x: Column of the cell
            y: Row of the cell
            direction: One of NORTH, EAST, SOUTH, WEST
        """
        # With | we can add the value of a bit to the given direction.
        # Ex: cell = 1010, direction = 0001 (N),
        # cell | direction = 1010 + 0001 = 1011
        self.grid[y][x] = self.grid[y][x] | direction

    def is_inside(self, x: int, y: int) -> bool:
        """ Check if the coordinates are within the maze bounds

        Args:
            x: Column to check
            y: Row to check

        Returns:
            True if the coordinates are valid, False otherwise.
        """
        # It's True only if x and y are positive and below the limits
        return 0 <= x < self.width and 0 <= y < self.height

    def debug_print(self) -> None:
        """ Print the maze grid as hexadecimal values for debugging """
        for row in self.grid:
            # Converts each cell of every row into 'X'(HEX) and prints all
            # of them separated by an space ' '.
            print(' '.join(format(cell, 'X') for cell in row))
