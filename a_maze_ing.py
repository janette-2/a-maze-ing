"""A-Maze-ing: maze generator entry point."""

import sys
from config_parser import parse_config, validate_config


def main() -> None:
    """Run the maze generator with the given configuration file."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(1)

    config_path: str = sys.argv[1]

    try:
        config = parse_config(config_path)
        validate_config(config)
        print("Config loaded successfully:")
        for key, value in config.items():
            print(f" {key} = {value}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
