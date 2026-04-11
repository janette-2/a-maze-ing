*This project has been created as part of the 42 curriculum by janrodri and cvaz-alf*
# a-maze-ing
## Description

This project consists of a maze generator developed in Python that, based on a configuration file, generates a maze and exports it to a file using a hexadecimal representation. Additionally, it includes a terminal-based visualization along with an interactive menu that allows the user to perform different actions on the maze.

## Instructions

### Requirements

- Python 3.10 or higher
- pip
- flake8 (optional)

### Compilation, instalation and execution

0. Create a virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

1. Install dependencies

```
make install
```

2. Execution
```
make run
```
- which is equivalent to running:
```
python3 a_maze_ing.py config.txt
```
- other useful commands:
```
make run
make debug
make clean
make lint   # cumple normas y no hay errores de tipos 
make lint-strict
```

### Configuration File

The configuration file controls the maze dimensions, the entry and exit points, the output file, and how the maze itself is generated.

An example of a config.txt could be:
```
WIDTH = 20
HEIGHT = 15
ENTRY = 0,0
EXIT = 19,14
OUTPUT_FILE = maze.txt
PERFECT = True 
SEED = 42
```
Where each KEY refers to:
* **WIDTH**: Maze width (number of cells) 
* **HEIGHT**: Maze height 
* **ENTRY**: Entry coordinates (x,y) 
* **EXIT**: Exit coordinates (x,y) E
* **OUTPUT_FILE**: Output filename 
* **PERFECT**:
    * True = generates a maze with a single solution

    * False =  generates a maze with multiple posible solutions
* **SEED**: Integer for reproducible results

### Maze Algorithm
The maze is generated using a Depth-First Search (DFS) algorithm, as it naturally produces perfect mazes, with a single path between any two cells, in a simple and efficient way.

The shortest path is computed using Breadth-First Search (BFS), since it guarantees finding the minimum path in an unweighted grid.

### Code Reusability (mazegen)
The reusable part of the project is the **mazegen** package, which provides the **MazeGenerator class**. It encapsulates the core logic of maze generation and solving, allowing it to be imported and used independently from the main application.

**Steps to test the reusable package:**

0. Clone the repository and create a virtual environment
```
git clone <repo_url>
cd a-maze-ing

python3 -m venv venv
source venv/bin/activate
```

1. Build and install the package
```
python -m build
cd dist
pip uninstall mazegen    # uninstall old packages
pip install mazegen-1.0.0-py3-none-any.whl
```

2. Leave the repository directory
```
cd /tmp   # por ejemplo
```

3. Run Python and test the package
```
python3
```
```python
from mazegen import MazeGenerator

gen = MazeGenerator(20, 15, 42, True)
maze = gen.generate()
path = gen.solve((0, 0), (19, 14))

print(path)
```

### Team and project management

**Roles:**

On one hand, *janrodri* handled the input/output algorithms, data validation, and graphical output. Meanwhile, *cvaz-alf* was responsible for packaging the reusable module and writing the README.md.

**Planning and evolution:**

At the beginning, a plan of approximately 7 days was established, where the work was organized into sequential parts. However, as the project progressed, it became necessary to work on tasks originally planned for later days in order to move forward, so the work assigned to the final days was completed throughout the rest of the project.

### Retrospective

**What worked well:**
- Dividing the project into daily sessions made it easier to track progress
  and stay focused on one task at a time.

- Using GitHub from day one allowed both team members to stay in sync and
  review each other's work through commits.

- The choice of the Recursive Backtracker algorithm proved solid — it naturally
  produces perfect mazes and was straightforward to adapt for the non-perfect
  mode and the 42 pattern embedding.

- Catching issues early (such as flake8 scanning .venv, or the border wall
  coherence bug) by testing frequently prevented bigger problems later.

- The modular structure of the project (separate files for config, maze,
  generator, validator, solver, renderer, menu) made it easy to work on
  each part independently.
 

**What could be improved:**
- The initial planning underestimated the complexity of some parts, particularly
  the ASCII renderer and the Unicode box-drawing character alignment, which
  required several iterations.

- The .flake8 configuration file was not included in the initial setup, which
  caused unexpected linting errors when first running make lint. Adding it from
  the start would have saved time.

- More unit tests would have made debugging faster, especially for the validator
  and the renderer.

- The visual representation of the solved path could have been more unified or improved visually

### Tools used
- Python 3.10+
- flake8 (linting)
- mypy (static type checking)
- Makefile (task automation)
- build (package building)
- GitHub (repository hosting)

## Resources
- Direct searches on Google about Python syntax (mostly answered automatically by Google’s AI)
- Use of AI to organize the different workdays
