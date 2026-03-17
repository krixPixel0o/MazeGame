import pygame

# Enhanced Colors (Tailwind inspired palette)
BG_COLOR = (15, 23, 42)           # Very Dark Slate (Background)
CELL_COLOR = (30, 41, 59)         # Dark Slate (Path)
WALL_COLOR = (56, 189, 248)       # Neon Cyan (Walls)
PLAYER_COLOR = (52, 211, 153)     # Emerald Green (Player)
ENEMY_COLOR = (248, 113, 113)     # Light Red (Enemy)
EXIT_COLOR = (192, 38, 211)       # Fuchsia (Exit)
PATH_COLOR = (250, 204, 21)       # Yellow (Optimal Path)
TEXT_BG = (15, 23, 42)
TEXT_FG = (248, 250, 252)

class MazeGUI:
    def __init__(self, game_state=None, cols=15, rows=15, cell_size=40):
        pygame.init()
        self.game = game_state
        self.maze = game_state.maze if game_state else None
        self.cell_size = cell_size
        self.width = cols * self.cell_size
        self.height = rows * self.cell_size
        
        # Add padding for text
        self.screen_width = self.width
        self.screen_height = self.height + 60
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Zloniac Krixo Maze")
        self.font = pygame.font.SysFont("impact", 28)
        
        # Starfield for menu
        import random
        self.stars = []
        for _ in range(150):
            # [x, y, depth]
            x = random.uniform(0, self.screen_width)
            y = random.uniform(0, self.screen_height)
            z = random.uniform(0.2, 1.0)
            self.stars.append([x, y, z])
        self.star_vel_x = 0.0
        self.star_vel_y = 0.0

    def draw_maze(self):
        # Fill background
        self.screen.fill(BG_COLOR)
        
        # Wall thickness relative to cell size
        wt = max(3, self.cell_size // 8)
        
        for x in range(self.maze.cols):
            for y in range(self.maze.rows):
                cell = self.maze.grid[x][y]
                px = x * self.cell_size
                py = y * self.cell_size
                
                # Draw cell interior with a slight padding so walls look cleaner
                pad = 1
                pygame.draw.rect(self.screen, CELL_COLOR, (px + pad, py + pad, self.cell_size - pad*2, self.cell_size - pad*2))
                
                # Draw exit highlight (a pulsing rect or inner rect)
                if (x, y) == self.maze.end:
                    pygame.draw.rect(self.screen, EXIT_COLOR, (px + pad, py + pad, self.cell_size - pad*2, self.cell_size - pad*2))
                
                # Draw walls with rounded-like connections by drawing lines extending slightly
                # Pygame lines can be flat, so we could draw thin rects, but lines with width work perfectly fine here.
                if cell.walls['top']:
                    pygame.draw.line(self.screen, WALL_COLOR, (px, py), (px + self.cell_size, py), wt)
                if cell.walls['right']:
                    pygame.draw.line(self.screen, WALL_COLOR, (px + self.cell_size, py), (px + self.cell_size, py + self.cell_size), wt)
                if cell.walls['bottom']:
                    pygame.draw.line(self.screen, WALL_COLOR, (px, py + self.cell_size), (px + self.cell_size, py + self.cell_size), wt)
                if cell.walls['left']:
                    pygame.draw.line(self.screen, WALL_COLOR, (px, py), (px, py + self.cell_size), wt)

    def draw_entity(self, entity, color):
        center_x = entity.x * self.cell_size + self.cell_size // 2
        center_y = entity.y * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 3
        # Outer generic glow ring
        pygame.draw.circle(self.screen, color, (center_x, center_y), radius + 2, 2)
        # Inner solid circle
        pygame.draw.circle(self.screen, color, (center_x, center_y), radius - 1)

    def draw_path(self, path):
        """Draws the optimal path as a glowing line."""
        if not path:
            return
            
        points = []
        for x, y in path:
            px = x * self.cell_size + self.cell_size // 2
            py = y * self.cell_size + self.cell_size // 2
            points.append((px, py))
            
        if len(points) > 1:
            pygame.draw.lines(self.screen, PATH_COLOR, False, points, max(3, self.cell_size // 6))
            
        # Draw small nodes on the path
        for p in points:
             pygame.draw.circle(self.screen, PATH_COLOR, p, max(3, self.cell_size // 8))

    def draw_text(self, text, color):
        """Draws status text at the bottom."""
        # Clear bottom area
        pygame.draw.rect(self.screen, TEXT_BG, (0, self.height, self.screen_width, 60))
        # Draw a separator bar
        pygame.draw.line(self.screen, WALL_COLOR, (0, self.height), (self.screen_width, self.height), 4)
        
        img = self.font.render(text, True, color)
        rect = img.get_rect(center=(self.screen_width // 2, self.height + 30))
        self.screen.blit(img, rect)

    def render_menu(self, mouse_rel=(0, 0)):
        self.screen.fill(BG_COLOR)
        
        # Update and draw stars
        mx, my = mouse_rel
        # Smooth out velocity changes
        self.star_vel_x = self.star_vel_x * 0.9 + mx * 0.1
        self.star_vel_y = self.star_vel_y * 0.9 + my * 0.1
        
        for star in self.stars:
            # Parallax mapping: deeper stars (lower z) move slower
            star[0] += (0.2 + self.star_vel_x) * star[2]
            star[1] += (0.2 + self.star_vel_y) * star[2]
            
            # Wrap around screen edges
            if star[0] > self.screen_width: star[0] -= self.screen_width
            elif star[0] < 0: star[0] += self.screen_width
            if star[1] > self.screen_height: star[1] -= self.screen_height
            elif star[1] < 0: star[1] += self.screen_height
            
            # Star color varying by depth
            c_val = max(50, int(255 * star[2]))
            pygame.draw.circle(self.screen, (c_val, c_val, c_val), (int(star[0]), int(star[1])), max(1, int(2 * star[2])))
        
        title_font = pygame.font.SysFont("impact", 48)
        title = title_font.render("ZLONIAC KRIXO MAZE", True, WALL_COLOR)
        
        opt1 = self.font.render("Press 1 : EASY", True, PLAYER_COLOR)
        opt2 = self.font.render("Press 2 : MEDIUM", True, PATH_COLOR)
        opt3 = self.font.render("Press 3 : HARD", True, ENEMY_COLOR)
        
        self.screen.blit(title, title.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 80)))
        self.screen.blit(opt1, opt1.get_rect(center=(self.screen_width // 2, self.screen_height // 2)))
        self.screen.blit(opt2, opt2.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50)))
        self.screen.blit(opt3, opt3.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 100)))
        
        pygame.display.flip()

    def render(self, show_path=False):
        self.draw_maze()
        
        if show_path:
            path = self.game.get_optimal_path_for_player()
            self.draw_path(path)
            
        self.draw_entity(self.game.player, PLAYER_COLOR) # Player
        self.draw_entity(self.game.enemy, ENEMY_COLOR)   # Enemy
        
        if self.game.game_over:
            if self.game.win:
                self.draw_text("YOU ESCAPED! [ PRESS R TO RESTART ]", PLAYER_COLOR)
            else:
                self.draw_text("ELIMINATED. [ PRESS R TO TRY AGAIN ]", ENEMY_COLOR)
        else:
             self.draw_text("W,A,S,D TO MOVE. REACH THE DESTINATION !", TEXT_FG)
             
        pygame.display.flip()
