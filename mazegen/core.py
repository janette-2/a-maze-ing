"""Reusable maze generator package core."""

from .maze import Maze
from .generator import generate
from .pattern import embed_pattern
from .solver import solve
from .validator import validate_maze


class MazeGenerator:
    """Reusable maze generator interface."""

    def __init__(
        self,
        width: int,
        height: int,
        seed: int = 42,
        perfect: bool = True,
    ) -> None:
        """Initialize the maze generator.

        Args:
            width: Maze width in cells.
            height: Maze height in cells.
            seed: Random seed for reproducibility.
            perfect: Whether to generate a perfect maze.
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.maze: Maze | None = None
        self.blocked: set[tuple[int, int]] = set()

    def generate(self) -> Maze:
        """Generate and validate a maze.

        Returns:
            The generated Maze instance.
        """
        maze = Maze(self.width, self.height)
        blocked = embed_pattern(maze)
        generate(maze, self.seed, self.perfect, blocked)

        self.maze = maze
        self.blocked = blocked
        return maze

    def validate(
        self,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> None:
        """Validate the generated maze.

        Args:
            entry: Entry coordinates.
            exit_: Exit coordinates.

        Raises:
            ValueError: If the maze has not been generated or is invalid.
        """
        if self.maze is None:
            raise ValueError("Maze has not been generated yet")

        validate_maze(self.maze, entry, exit_, self.blocked)

    def solve(
        self,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> str:
        """Solve the maze from entry to exit.

        Args:
            entry: Entry coordinates.
            exit_: Exit coordinates.

        Returns:
            Shortest path as a string of N/E/S/W letters.
        """
        if self.maze is None:
            raise ValueError("Maze has not been generated yet")

        return solve(self.maze, entry, exit_)

    def get_grid(self) -> list[list[int]]:
        """Return the generated maze grid.

        Returns:
            The internal maze grid.

        Raises:
            ValueError: If the maze has not been generated yet.
        """
        if self.maze is None:
            raise ValueError("Maze has not been generated yet")

        return self.maze.grid
