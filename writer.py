""" Maze output writer in external file for A-Maze-ing """

from maze import Maze


def write_output(maze: Maze, entry: tuple[int, int],
                 exit_: tuple[int, int], path: str,
                 output_file: str) -> None:
    """ Write the maze in a file in hexadecimal format

    Format:
        - One hex digit per cell, one row per line
        - Empty line after the grid
        - Entry coordinates (x, y)
        - Exit coordinates (x, y)
        - Shortest path as string of N/E/S/W letters

    Args:
        maze: The Maze object to write
        entry: Entry coordinates (x, y)
        exit_: Exit coordinates (x, y)
        path: Shortest path from entry to exit
        output_file: Path to the output file

    Raise:
        OSError: If the file cannot be written
    """

    try:
        with open(output_file, 'w') as f:
            # Write grid row by row in hex formats
            for row in maze.grid:
                line = ''.join(format(cell, 'X') for cell in row)
                f.write(line + '\n')

            # Empty line separator
            f.write('\n')

            # Entry, exit and path
            f.write(f'{entry[0]},{entry[1]}\n')
            f.write(f'{exit_[0]},{exit_[1]}\n')
            f.write(path + '\n')

    except OSError as e:
        raise OSError(f"Could not write output file '{output_file}': {e}")
