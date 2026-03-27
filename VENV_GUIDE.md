# Virtual Environment Guide

## What is a virtual environment?

A virtual environment is a folder (`.venv/`) that contains an isolated Python
installation for your project. Libraries installed inside it do not affect the
rest of your system or other projects.

---

## Cloning the repository for the first time

```bash
# 1. Clone the repository
git clone https://github.com/tu-usuario/a-maze-ing.git

# 2. Enter the project folder
cd a-maze-ing

# 3. Create the virtual environment
python3 -m venv .venv

# 4. Activate it
source .venv/bin/activate

# 5. Install project dependencies
make install
```

After step 5 you are ready to work.

---

## Daily use

Every time you open a new terminal:

```bash
# Activate the virtual environment
source .venv/bin/activate
```

You know it is active because the prompt shows `(.venv)` at the start:

```
(.venv) user@LAPTOP:~/a-maze-ing$
```

To deactivate it when you are done:

```bash
deactivate
```

---

## Keeping your local copy up to date

Every time your partner pushes new changes to GitHub:

```bash
# Download the latest changes
git pull
```

If new dependencies were added:

```bash
# Install them
make install
```

---

## Quick reference

| Command | When to use it |
|---|---|
| `git clone <url>` | Only the first time |
| `python3 -m venv .venv` | Only the first time |
| `source .venv/bin/activate` | Every time you open a new terminal |
| `make install` | First time, or when new dependencies are added |
| `git pull` | Before starting to work each day |
| `deactivate` | When you finish working |

---

## Important notes

**`.venv/` is never uploaded to GitHub** — it is in `.gitignore`.
Each person has their own copy on their own machine.

**If you see `module not found` errors** — the virtual environment is probably
not active. Check that the prompt shows `(.venv)`.

**If a new dependency was added by your partner** — run `make install` after
`git pull` to install it.
