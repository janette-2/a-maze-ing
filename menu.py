""" Interactive menu for A-Maze-ing """
from maze import Maze
from renderer import render, path_to_cells


def show_menu(maze: Maze, entry: tuple[int, int],
              exit_: tuple[int, int], path: str,
              blocked: set[tuple[int, int]]) -> str:
    """ Run the interactive menu loop

    Args:
        maze: The Maze object to display
        entry: Entry coordinates (x, y)
        exit_: Exit coordinates (x, y)
        path: Shortest path string of N/E/S/W letters
        blocked: Sef of cells belonging to the 42 pattern
    """
    show_path: bool = False
    wall_color: str = "white"
    color_options: list[str] = [
        "white", "red", "green", "yellow", "blue"
    ]
    color_index: int = 0

    while True:
        # Clear screen and render Maze
        print("\033[2J\033[H", end="")  # Avoids the \n at the end of printing
        cells = path_to_cells(entry, path)
        print(render(maze, entry, exit_, cells, blocked,
                     wall_color, show_path))

        # Show menu options
        print("\n==== A-Maze-ing ====")
        print("1. Regenerate maze")
        print("2. Show/Hide path")
        print("3. Change wall color")
        print("4. Quit")
        print("====================")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            # Signal caller to regenerate
            return "regenerate"
        elif choice == "2":
            show_path = not show_path  # Turns 'True'
        elif choice == "3":
            color_index = (color_index + 1) % len(color_options)
            wall_color = color_options[color_index]
        elif choice == "4":
            return "quit"
        else:
            print("Invalid choice, please enter 1-4")
            input("Press Enter to continue...")
