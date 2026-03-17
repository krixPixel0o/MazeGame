from algorithms import a_star

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_to(self, x, y):
        self.x = x
        self.y = y
        
class Player(Entity):
    pass

class Enemy(Entity):
    pass

class GameState:
    def __init__(self, maze):
        self.maze = maze
        self.player = Player(maze.start[0], maze.start[1])
        # By default, enemy starts at the exit or somewhere random
        # Let's put the enemy near the middle for a challenge or the exit
        self.enemy = Enemy(maze.end[0], maze.end[1])
        self.game_over = False
        self.win = False
        self.player_move_counter = 0
        self.difficulty = "medium"  # 'easy', 'medium', 'hard'

    def update_player(self, new_x, new_y):
        """Moves player if the move is valid in the maze."""
        walls = self.maze.grid[self.player.x][self.player.y].walls
        
        # Check valid steps
        valid = False
        if new_x == self.player.x and new_y == self.player.y - 1 and not walls['top']:
            valid = True
        elif new_x == self.player.x + 1 and new_y == self.player.y and not walls['right']:
            valid = True
        elif new_x == self.player.x and new_y == self.player.y + 1 and not walls['bottom']:
            valid = True
        elif new_x == self.player.x - 1 and new_y == self.player.y and not walls['left']:
            valid = True

        if valid:
            self.player.move_to(new_x, new_y)
            self.player_move_counter += 1
        return valid

    def check_conditions(self):
        """Check if win or loss conditions are met."""
        if (self.player.x, self.player.y) == self.maze.end:
            self.game_over = True
            self.win = True
        elif (self.player.x, self.player.y) == (self.enemy.x, self.enemy.y):
            self.game_over = True
            self.win = False

    def move_enemy_towards_player(self):
        """Uses A* to find the path towards the player and takes one step.
        To balance the game, the enemy's speed is dictated by the difficulty setting."""
        if self.game_over:
            return
            
        # Throttling logic based on difficulty
        if self.difficulty == "easy":
            # Moves 1 time for every 3 player moves
            if self.player_move_counter % 3 != 0:
                return
        elif self.difficulty == "medium":
            # Moves 1 time for every 2 player moves
            if self.player_move_counter % 2 != 0:
                return
        # If "hard", moves every single player turn (1:1 ratio) - no throttle
        
        path = a_star(self.maze, (self.enemy.x, self.enemy.y), (self.player.x, self.player.y))
        # path[0] is current pos, path[1] is next step
        if path and len(path) > 1:
            next_step = path[1]
            self.enemy.move_to(next_step[0], next_step[1])
            
        # Check conditions again in case the enemy caught the player
        self.check_conditions()

    def get_optimal_path_for_player(self):
        """Returns the true perfect path from the start to the exit avoiding the enemy."""
        from collections import deque
        from algorithms import a_star, get_valid_neighbors
        
        start_state = (self.maze.start[0], self.maze.start[1], self.maze.end[0], self.maze.end[1], 0)
        # queue stores (px, py, ex, ey, turn_mod_6, absolute_turn)
        queue = deque([(*start_state, 0)])
        came_from = {start_state: None}
        visited = set([start_state])
        
        while queue:
            px, py, ex, ey, turn_mod, abs_turn = queue.popleft()
            
            if (px, py) == self.maze.end:
                path = []
                curr = (px, py, ex, ey, turn_mod)
                while curr is not None:
                    if not path or path[-1] != (curr[0], curr[1]):
                        path.append((curr[0], curr[1]))
                    curr = came_from[curr]
                path.reverse()
                return path
                
            for nx, ny in get_valid_neighbors(self.maze, px, py):
                # Player moves to nx, ny
                if (nx, ny) == (ex, ey) and (nx, ny) != self.maze.end:
                    continue  # Walked into enemy
                    
                new_abs_turn = abs_turn + 1
                new_turn_mod = new_abs_turn % 6
                nex, ney = ex, ey
                
                if (nx, ny) != self.maze.end:
                    enemy_moves = False
                    if self.difficulty == "easy" and new_abs_turn % 3 == 0:
                        enemy_moves = True
                    elif self.difficulty == "medium" and new_abs_turn % 2 == 0:
                        enemy_moves = True
                    elif self.difficulty == "hard":
                        enemy_moves = True
                        
                    if enemy_moves:
                        epath = a_star(self.maze, (ex, ey), (nx, ny))
                        if epath and len(epath) > 1:
                            nex, ney = epath[1][0], epath[1][1]
                            
                    if (nx, ny) == (nex, ney):
                        continue  # Enemy caught player
                        
                next_state = (nx, ny, nex, ney, new_turn_mod)
                if next_state not in visited:
                    visited.add(next_state)
                    came_from[next_state] = (px, py, ex, ey, turn_mod)
                    queue.append((*next_state, new_abs_turn))
                    
        # Fallback if no avoiding path exists
        return a_star(self.maze, self.maze.start, self.maze.end)
