"""A-Maze-ing: maze generator entry point."""

import sys
from config_parser import parse_config, validate_config
from maze import Maze
from generator import generate
from pattern import embed_pattern
from validator import validate_maze
from solver import solve
from writer import write_output
from menu import show_menu


def build_maze(config: dict[str, str]) -> tuple[
    Maze, tuple[int, int], tuple[int, int], str,
        set[tuple[int, int]]]:
    """ Build, validate and solve a maze from config

    Args:
        config: Dictionary of configuration key-value pairs

    Returns:
        A tuple of (maze, entry, exit_, path, blocked)
    """
    # Build the maze configuration
    width = int(config["WIDTH"])
    height = int(config["HEIGHT"])
    # Gets the seed from the config, if there is none,
    # uses the seed = 42
    seed = int(config.get("SEED", 42))
    # Converts a string value into a comparison
    # in order to create a boolean
    perfect = config["PERFECT"] == "True"

    # Coordinates of entry and exit
    entry_x, entry_y = map(int, config["ENTRY"].split(','))
    exit_x, exit_y = map(int, config["EXIT"].split(','))
    entry = (entry_x, entry_y)
    exit_ = (exit_x, exit_y)
    # Output file path configured
    output_file = config["OUTPUT_FILE"]
    maze = Maze(width, height)

    # Places the '42' pattern before generating the paths of the maze
    blocked = embed_pattern(maze)

    # Generates the final paths
    generate(maze, seed, perfect, blocked)

    # Validates the conditions of the maze
    validate_maze(maze, entry, exit_, blocked)

    # Solve the shortest path
    path = solve(maze, entry, exit_)
    if not path:
        print("Warning: no path found between entry and exit",
              file=sys.stderr)

    # Write output in file
    write_output(maze, entry, exit_, path, output_file)

    return maze, entry, exit_, path, blocked


def main() -> None:
    """Run the maze generator with the given configuration file."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(1)

    config_path: str = sys.argv[1]

    try:
        config = parse_config(config_path)
        validate_config(config)

        maze, entry, exit_, path, blocked = build_maze(config)
        # uses the seed = 42
        seed = int(config.get("SEED", 42))

        while True:
            action = show_menu(maze, entry, exit_, path, blocked)

            if action == "quit":
                break
            elif action == "regenerate":
                seed += 1
                config["SEED"] = str(seed)
                maze, entry, exit_, path, blocked = build_maze(config)

    except (FileNotFoundError, ValueError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
