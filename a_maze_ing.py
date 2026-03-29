"""A-Maze-ing: maze generator entry point."""

import sys
from config_parser import parse_config, validate_config
from maze import Maze
from generator import generate


def main() -> None:
    """Run the maze generator with the given configuration file."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(1)

    config_path: str = sys.argv[1]

    try:
        config = parse_config(config_path)
        validate_config(config)

        # Build the maze configuration
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        # Gets the seed from the config, if there is none,
        # uses the seed = 42
        seed = int(config.get("SEED", 42))
        # Converts a string value into a comparison
        # in order to create a boolean
        perfect = config["PERFECT"] == "True"

        maze = Maze(width, height)
        generate(maze, seed, perfect)

        print(f"Maze generated ({width}x{height}):")
        maze.debug_print()

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
