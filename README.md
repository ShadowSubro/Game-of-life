# Conway's Game of Life -- Python Implementation

This project is a simple and clear implementation of **Conway's Game of
Life**, a zero-player cellular automaton where cells evolve based on a
set of rules.\
It includes both a **Python script** and a **Jupyter Notebook demo**,
along with a **compiled executable** for easy use.

## Features

-   Fully working Game of Life simulation in Python\
-   Supports any grid size\
-   Simple terminal-based visualization\
-   Jupyter Notebook version for demonstrations\
-   Windows executable included in the `dist/` folder\
-   Packaged using PyInstaller (one-file executable)

## Project Structure

    Game-of-life/
    ├── Game_of_life.ipynb      # Notebook version with explanations
    ├── game_of_life.py         # Main Python implementation
    ├── game_of_life.spec       # PyInstaller spec file (onefile)
    ├── dist/
    │   └── game_of_life.exe    # Compiled executable
    ├── build/                  # PyInstaller build directory
    └── .gitattributes

## How to Run

### 1. Run using Python

Make sure Python 3 is installed.

    python game_of_life.py

### 2. Run the Executable (Windows)

Inside the `dist` folder:

-   Double-click **game_of_life.exe**\
    No installation required.

## About Conway's Game of Life

The simulation follows 4 rules applied to each cell:

1.  **Underpopulation:** Fewer than 2 neighbors → dies\
2.  **Survival:** 2 or 3 neighbors → lives\
3.  **Overpopulation:** More than 3 neighbors → dies\
4.  **Reproduction:** Exactly 3 neighbors → becomes alive

## Build Instructions (Optional)

Rebuild the `.exe`:

    pyinstaller --onefile game_of_life.py

Or using the existing `.spec` file:

    pyinstaller game_of_life.spec

## License

This project is for educational use.
