import random

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

class Maze:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.grid = [[Cell(x, y) for y in range(rows)] for x in range(cols)]
        self.start = None
        self.end = None

    def _get_neighbors(self, cell):
        neighbors = []
        x, y = cell.x, cell.y

        # Top
        if y > 0:
            neighbors.append((self.grid[x][y - 1], 'top', 'bottom'))
        # Right
        if x < self.cols - 1:
            neighbors.append((self.grid[x + 1][y], 'right', 'left'))
        # Bottom
        if y < self.rows - 1:
            neighbors.append((self.grid[x][y + 1], 'bottom', 'top'))
        # Left
        if x > 0:
            neighbors.append((self.grid[x - 1][y], 'left', 'right'))

        return [n for n in neighbors if not n[0].visited]

    def _remove_walls(self, current, next_cell, direction, opposite):
        current.walls[direction] = False
        next_cell.walls[opposite] = False

    def generate(self, start_x=0, start_y=0, end_x=None, end_y=None):
        """Generates a perfect maze using DFS recursive backtracker."""
        # Reset visited state in case of regenerating
        for x in range(self.cols):
            for y in range(self.rows):
                self.grid[x][y].visited = False
                self.grid[x][y].walls = {'top': True, 'right': True, 'bottom': True, 'left': True}

        if end_x is None:
            end_x = self.cols - 1
        if end_y is None:
            end_y = self.rows - 1
            
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)

        stack = []
        current = self.grid[start_x][start_y]
        current.visited = True
        stack.append(current)

        while stack:
            # Pop a cell from the stack and make it a current cell
            current = stack.pop()
            unvisited_neighbors = self._get_neighbors(current)

            if unvisited_neighbors:
                # Push the current cell to the stack
                stack.append(current)
                # Choose one of the unvisited neighbours
                next_cell, direction, opposite = random.choice(unvisited_neighbors)
                # Remove the wall between the current cell and the chosen cell
                self._remove_walls(current, next_cell, direction, opposite)
                # Mark the chosen cell as visited and push it to the stack
                next_cell.visited = True
                stack.append(next_cell)
                
        # BRAID MAZE CONVERSION: Create loops by knocking down random walls
        # Without loops, a tracking enemy is mathematically impossible to dodge in a perfect maze.
        braid_ratio = 0.2  # 20% chance to remove an internal wall
        for x in range(1, self.cols - 1):
            for y in range(1, self.rows - 1):
                if random.random() < braid_ratio:
                    cell = self.grid[x][y]
                    # Get existing walls
                    walls = [d for d in ['top', 'right', 'bottom', 'left'] if cell.walls[d]]
                    if walls:
                        d = random.choice(walls)
                        if d == 'top':
                            self._remove_walls(cell, self.grid[x][y-1], 'top', 'bottom')
                        elif d == 'right':
                            self._remove_walls(cell, self.grid[x+1][y], 'right', 'left')
                        elif d == 'bottom':
                            self._remove_walls(cell, self.grid[x][y+1], 'bottom', 'top')
                        elif d == 'left':
                            self._remove_walls(cell, self.grid[x-1][y], 'left', 'right')

        return self

    def __str__(self):
        
        res = ""
        for y in range(self.rows):
            top_line = ""
            mid_line = ""
            for x in range(self.cols):
                cell = self.grid[x][y]
                # Top wall
                top_line += "+---" if cell.walls['top'] else "+   "
                
                # Left wall and interior
                if (x, y) == self.start:
                    interior = " S "
                elif (x, y) == self.end:
                    interior = " E "
                else:
                    interior = "   "
                mid_line += "|" + interior if cell.walls['left'] else " " + interior

            res += top_line + "+\n"
            res += mid_line + "|\n"
            
        # Bottom edge of the maze
        bottom_line = ""
        for x in range(self.cols):
            bottom_line += "+---" if self.grid[x][self.rows-1].walls['bottom'] else "+   "
        res += bottom_line + "+\n"
        return res
