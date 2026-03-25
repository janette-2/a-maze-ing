"""A-Maze-ing: maze generator entry point."""

import sys


def main() -> None:
    """Run the maze generator with the given configuration file."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(1)

    config_path: str = sys.argv[1]
    print(f"Config file: {config_path}")


if __name__ == "__main__":
    main()
