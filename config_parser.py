"""Configuration file parser for A-Maze-ing."""


def parse_config(path: str) -> dict[str, str]:
    """Parse a KEY=VALUE configuration file.

    Args:
        path: Path to the configuration file.

    Returns:
        A dictionary mapping configuration keys to their string values.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If a line has invalid KEY=VALUE syntax.
    """
    config: dict[str, str] = {}

    try:
        # 'open' function -> Opens the given file and returns
        # a file object indexed by it's lines
        # 'with' method -> to read a file, ensures that after finishing,
        # the file will always close even if problems arise.
        with open(path, 'r') as f:
            # Gets the lines of the text and indexes one by one
            for line_number, line in enumerate(f, start=1):
                # Cleans each line of non readable chars (\n, \t, filling
                # spaces before and after the content)
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Validate KEY=VALUE format, puts an error otherwise
                if '=' not in line:
                    raise ValueError(
                        f"Line {line_number}: invalid syntax '{line}'"
                    )

                # Makes sure to separate only at the first
                # split("sep", maxsplit) occurance of the
                # found separator, if the separator shows more
                # than once, those will be ignored
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                if not key:
                    raise ValueError(
                        f"Line {line_number}: empty key"
                    )

                # After separating, cleaning and checking the
                # values, finally puts them in a dictionary if
                # everything is okay
                config[key] = value

    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: '{path}'")

    return config


def validate_config(config: dict[str, str]) -> None:

    required_keys = [
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

    # Checked that all the required keys exist in config
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required key: '{key}'")

    # Validates that WIDTH and HEIGHT are positive integers

    # Looks only in the keys specified
    for key in ("WIDTH", "HEIGHT"):
        try:
            value = int(config[key])
            if value <= 0:
                raise ValueError(
                    f"'{key}' must be a positive integer, but the given value"
                    f" has been '{config[key]}'"
                )
        except ValueError:
            raise ValueError(
                    f"'{key}' must be a positive integer, but the given value"
                    f" has been '{config[key]}'"
                )

        # If the values are okay (no errors raised)
    width: int = int(config["WIDTH"])
    height: int = int(config["HEIGHT"])

    # Validate the ENTRY and EXIT cells, check its format and bounds
    for key in ("ENTRY", "EXIT"):
        try:
            x_str, y_str = config[key].split(",")
            x, y = int(x_str.strip()), int(y_str.strip())
            if not (0 <= x < width and 0 <= y < height):
                raise ValueError(
                    f"'{key}' coordinates ({x}, {y}) are outside "
                    f"the maze bounds ({width}x{height})"
                )
        # Checks if the value is out of bounds or if it's
        # (None: obj -> Attribute)
        except (ValueError, AttributeError):
            raise ValueError(
                f"'{key}' must be a positive integer, got '{config[key]}'"
            )

    # Validate ENTRY AND EXIT ade different
    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("'ENTRY' and 'EXIT' must be different cells")

    # Validate that PERFECT is a boolean
    if config["PERFECT"] not in ("True", "False"):
        raise ValueError(
            f"'PERFECT' must be 'True' or 'False', got '{config['PERFECT']}"
        )
