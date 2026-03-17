# Maze Game Backend Implementation Plan

We will create a foundational backend to generate and solve grid-based mazes. This will encapsulate all DSA logic as requested.

## Proposed Changes

### Core Backend Logic
We will structure the code into several python scripts to cleanly separate concerns.

#### [NEW] `maze_core.py`(file:///c:/MazeGame/maze_core.py)
This file will contain the Grid definition, the Maze class, and the generation logic.
- `Cell`: Represents individual grid cells (walls, paths, start, end).
- `Maze`: Manages the 2D grid, start, and end coordinates.
- **Generation Logic (Randomized DFS)**: A depth-first search approach (Recursive Backtracker) to carve a random perfect maze each time it is instantiated.

#### [NEW] `algorithms.py`(file:///c:/MazeGame/algorithms.py)
Contains various graph traversal algorithms to solve the maze.
- `bfs(maze, start, end)`: Breadth-First Search (Shortest Path)
- `dfs(maze, start, end)`: Depth-First Search (Any Path)
- `dijkstra(maze, start, end)`: Dijkstra's Algorithm (Shortest Path)
- `a_star(maze, start, end)`: A* Search Algorithm (Shortest Path, optimized with Manhattan distance)

#### [NEW] `game_state.py`(file:///c:/MazeGame/game_state.py)
Manages the players and the rules of the game.
- Track `Player` position and `Enemy` position.
- Turn-based or step-based update function.
- `check_game_over()`: Checks if the player reached the end (Win) or if the enemy caught the player / finished first (Loss).
- Function to return the correct shortest path (using BFS/A*) to show the user if they lose.

#### [MODIFY] `main.py`(file:///c:/MazeGame/main.py)
A driver script to demonstrate creating a random maze, running the algorithms, and testing the backend without UI. We will wipe the existing `main.py` contents.

## Verification Plan

### Automated Tests
- Run `main.py` to print a text-based ASCII representation of the randomly generated maze.
- Verify that the pathfinding algorithms can successfully return a path from Start to End.
- Ensure the shortest path length returned by BFS, Dijkstra, and A* are identical.
