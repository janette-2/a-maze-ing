# .PHONY declares these as commands, not files.
# Without this, if a file named 'clean' existed, make clean would do nothing.
.PHONY: install run debug clean lint lint-strict

# Installs all dependencies listed in requirements.txt.
# Your partner should run this after cloning the repo.
install:
	pip install -r requirements.txt

# Runs the program with the default config file.
run:
	python3 a_maze_ing.py config.txt

# Opens Python's built-in interactive debugger (pdb).
# Useful commands: n=next line, p var=print variable, q=quit.
debug:
	python3 -m pdb a_maze_ing.py config.txt

# Removes all temporary files that Python generates automatically.
# - find searches recursively from the current directory (.)
# - -type d matches directories only
# - -exec rm -rf {} + deletes each match
# - 2>/dev/null silences errors if nothing is found
# - || true prevents make from failing if the command finds nothing
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

# Runs both code quality tools with the flags required by the subject.
# flake8: checks code style and formatting (PEP8).
# mypy: checks that declared types are correct.
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores \
	       --ignore-missing-imports --disallow-untyped-defs \
	       --check-untyped-defs

# Stricter version of lint (optional but recommended).
lint-strict:
	flake8 .
	mypy . --strict