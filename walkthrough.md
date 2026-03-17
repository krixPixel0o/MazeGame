# Maze Game Implemented

I have completed the full backend logic and hooked it into a Pygame window as requested.

## Features Added

### 3D and 2D Rendering Engines
You can choose how you play!
- **2D Mode**: A top-down grid renderer using Pygame.
- **3D Mode**: A First-Person 3D voxel renderer using the Ursina Engine!

### Backend Algorithms
The core DSA structures requested have been completely integrated into BOTH engines:
- **Randomized Maze Generation**: A 10x10 or 15x15 perfect maze is generated dynamically using a **DFS Recursive Backtracker** every time the game starts or restarts.
- **Pathfinding Logic**:
  - [bfs](file:///c:/MazeGame/algorithms.py#48-67): Calculates the shortest path.
  - [dfs](file:///c:/MazeGame/algorithms.py#28-47): Finds any workable path.
  - [dijkstra](file:///c:/MazeGame/algorithms.py#68-94): Validates the shortest cost.
  - [a_star](file:///c:/MazeGame/algorithms.py#95-126): Fully integrated into the game state to maneuver both the Enemy and the hints.

### The Game Itself
- **Entities**: 
  - **Player (Blue)** starting at the top left [(0,0)](file:///c:/MazeGame/algorithms.py#28-47).
  - **Enemy (Red)** starting at the bottom right [(14, 14)](file:///c:/MazeGame/algorithms.py#28-47) which is also the exit.
  - **Exit (Green)** located at the bottom right.
- **Controls**: Use `W,A,S,D` or Arrow Keys to navigate the maze.
- **Enemy AI**: Every time the player takes a step, the enemy calculates the absolute shortest path to your position using **A***. To make the game fair, the Enemy is **half as fast** as you, meaning it only takes a step once for every two steps you take.
- **Win/Loss**: 
  - Reach the Green square before the Enemy catches you to Win!
  - If the Red square lands on you, you Lose! The screen will then reveal the **Yellow A* optimal path** you should have taken from your death location to the exit.
- **Replayability**: Press `R` after dying or winning to generate a brand new random maze and play again.

## Verification

You can play either version right now using the python terminal!

### To Play in 2D Top-Down View:
Run this in your terminal:
`python main.py`

### To Play in 3D First-Person View:
Run this in your terminal:
`python main_3d.py`
Use your mouse to look around and `W,A,S,D` to move. Press `Esc` to free your mouse to close the window.

- Verify the maze is sufficiently random.
- Test moving around.
- Try getting caught by the enemy to see the path algorithm visualize the intended route to the exit (in 3D, it will draw a trail of glowing yellow orbs)!
