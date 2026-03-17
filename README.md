# Maze Game (Python + Pygame)

This project is a small maze escape game built using Python and Pygame.
Each time the game starts, a new maze is generated and the player must reach the exit before being caught by the enemy.

The project was mainly built to experiment with maze generation and graph search algorithms such as DFS, BFS, Dijkstra, and A*.

---

## Overview

The maze is generated dynamically using a depth-first search based algorithm.
The player starts at the top-left corner of the maze and the exit is located at the bottom-right corner.

An enemy is also present in the maze. The enemy tracks the player by calculating the shortest path using the **A*** algorithm and moves toward the player depending on the selected difficulty level.

If the enemy catches the player, the game ends.

---

## Features

* Random maze generation every time the game starts
* Multiple pathfinding algorithms implemented
* Enemy AI that tracks the player
* Difficulty levels (Easy / Medium / Hard)
* Visualization of the optimal path when the player loses
* Simple keyboard controls for movement

---

## Algorithms Used

The project includes implementations of the following algorithms:

* **DFS (Depth First Search)** – used for maze generation
* **BFS (Breadth First Search)** – shortest path search
* **Dijkstra's Algorithm** – cost-based shortest path
* **A*** – used for enemy pathfinding

All algorithms operate on the maze grid structure.

---

## Project Structure

```
MazeGame
│
├── main.py
├── maze_core.py
├── algorithms.py
├── game_state.py
├── gui.py
├── implementation_plan.md
├── walkthrough.md
└── output.txt
```

### File description

**main.py**
Runs the game loop and handles input.

**maze_core.py**
Contains the maze grid structure and the maze generation logic.

**algorithms.py**
Contains the implementations of DFS, BFS, Dijkstra and A* search algorithms.

**game_state.py**
Handles player movement, enemy movement and win/loss conditions.

**gui.py**
Responsible for rendering the maze, player, enemy and UI elements using Pygame.

---

## Installation

Make sure Python 3 is installed.

Install pygame:

```
pip install pygame
```

Clone the repository:

```
git clone https://github.com/yourusername/MazeGame.git
cd MazeGame
```

---

## Running the Game

Run the following command in the project folder:

```
python main.py
```

---

## Controls

```
W / A / S / D  - Move player
Arrow Keys     - Move player
R              - Restart game
```

---

## Difficulty Levels

When the game starts, you can select the difficulty:

```
1 - Easy
2 - Medium
3 - Hard
```

The difficulty changes how often the enemy moves toward the player.

---

## Purpose of the Project

This project was created to explore:

* Maze generation algorithms
* Graph traversal techniques
* Basic game logic using Python
* Visualization of pathfinding algorithms

---

## Possible Improvements

Some ideas that could be added later:

* Larger mazes
* Score tracking
* Timer based gameplay
* Better graphics and animations
* Additional enemy behaviors


