import pygame
import sys
from maze_core import Maze
from game_state import GameState
from gui import MazeGUI

def generate_new_game(cols=15, rows=15, difficulty="medium"):
    """Factory function to regenerate a new shuffled maze and state."""
    maze = Maze(cols, rows)
    maze.generate(start_x=0, start_y=0, end_x=cols-1, end_y=rows-1)
    state = GameState(maze)
    state.difficulty = difficulty
    return state

def main():
    gui = MazeGUI(None, cols=15, rows=15)
    clock = pygame.time.Clock()
    running = True
    in_menu = True
    game_state = None
    
    pygame.mouse.get_rel() # Clear initial relative mouse movement

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
                
            if event.type == pygame.KEYDOWN:
                if in_menu:
                    difficulty = None
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        difficulty = "easy"
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        difficulty = "medium"
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        difficulty = "hard"
                        
                    if difficulty:
                        game_state = generate_new_game(difficulty=difficulty)
                        gui.game = game_state
                        gui.maze = game_state.maze
                        in_menu = False
                    continue
                    
                if game_state.game_over:
                    # Press R to go back to menu
                    if event.key == pygame.K_r:
                        in_menu = True
                    continue

                player_moved = False
                
                # Check directional keys
                if event.key in (pygame.K_w, pygame.K_UP):
                    player_moved = game_state.update_player(game_state.player.x, game_state.player.y - 1)
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    player_moved = game_state.update_player(game_state.player.x, game_state.player.y + 1)
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    player_moved = game_state.update_player(game_state.player.x - 1, game_state.player.y)
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    player_moved = game_state.update_player(game_state.player.x + 1, game_state.player.y)
                    
                if player_moved:
                    # Check win condition before enemy moves
                    game_state.check_conditions()
                    
                    if not game_state.game_over:
                        # Allow enemy to advance
                        game_state.move_enemy_towards_player()

        if in_menu:
            mouse_rel = pygame.mouse.get_rel()
            gui.render_menu(mouse_rel)
        else:
            pygame.mouse.get_rel() # Prevent sudden accumulation when returning to menu
            # Check conditions
            game_state.check_conditions()
            
            # Draw frame
            show_path = game_state.game_over and not game_state.win
            gui.render(show_path=show_path)
        
        # Max FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
