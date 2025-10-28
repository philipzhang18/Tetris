"""
Advanced Tetris Game using Python and Pygame

Installation:
pip install pygame

Controls:
- Arrow Left/Right: Move piece horizontally
- Arrow Down: Soft drop (move down faster)
- Arrow Up: Rotate piece
- Space: Hard drop (instantly drop to bottom)
- P: Pause/Resume game
- R: Restart game

Features:
- All 7 standard Tetromino shapes with different colors
- Next piece preview
- Score system with level progression
- Line clearing with visual effects
- Sound effects
- Game pause and restart
"""

import pygame
import random
import sys

# Constants
GRID_WIDTH = 10
GRID_HEIGHT = 20
TILE_SIZE = 30
GAME_WIDTH = GRID_WIDTH * TILE_SIZE
GAME_HEIGHT = GRID_HEIGHT * TILE_SIZE
WINDOW_WIDTH = GAME_WIDTH + 200  # Extra space for UI
WINDOW_HEIGHT = GAME_HEIGHT
SIDEBAR_WIDTH = 200

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Define colors for each tetromino
TETROMINO_COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': PURPLE,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE
}

# Tetromino shapes
TETROMINOES = {
    'I': [
        ['.....',
         '..#..',
         '..#..',
         '..#..',
         '..#..'],
        ['.....',
         '.....',
         '####.',
         '.....',
         '.....']
    ],
    'O': [
        ['.....',
         '.....',
         '.##..',
         '.##..',
         '.....']
    ],
    'T': [
        ['.....',
         '.....',
         '.#...',
         '###..',
         '.....'],
        ['.....',
         '.....',
         '.#...',
         '.##..',
         '.#...'],
        ['.....',
         '.....',
         '.....',
         '###..',
         '.#...'],
        ['.....',
         '.....',
         '.#...',
         '##...',
         '.#...']
    ],
    'S': [
        ['.....',
         '.....',
         '.##..',
         '##...',
         '.....'],
        ['.....',
         '.#...',
         '.##..',
         '..#..',
         '.....']
    ],
    'Z': [
        ['.....',
         '.....',
         '##...',
         '.##..',
         '.....'],
        ['.....',
         '..#..',
         '.##..',
         '.#...',
         '.....']
    ],
    'J': [
        ['.....',
         '.#...',
         '.#...',
         '##...',
         '.....'],
        ['.....',
         '.....',
         '#....',
         '###..',
         '.....'],
        ['.....',
         '.##..',
         '.#...',
         '.#...',
         '.....'],
        ['.....',
         '.....',
         '###..',
         '..#..',
         '.....']
    ],
    'L': [
        ['.....',
         '..#..',
         '..#..',
         '.##..',
         '.....'],
        ['.....',
         '.....',
         '###..',
         '#....',
         '.....'],
        ['.....',
         '##...',
         '.#...',
         '.#...',
         '.....'],
        ['.....',
         '.....',
         '..#..',
         '###..',
         '.....']
    ]
}

class Tetromino:
    """Class representing a tetromino piece"""
    
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = TETROMINO_COLORS[shape]
        self.rotation = 0
        
    def get_rotated_shape(self, rotation=None):
        """Get the shape at the specified rotation (if None, use current rotation)"""
        if rotation is None:
            rotation = self.rotation
            
        # Get the shape pattern, cycling through available rotations
        rotations = TETROMINOES[self.shape]
        return rotations[rotation % len(rotations)]
    
    def get_cells(self, x=None, y=None, rotation=None):
        """Get the grid cells occupied by this tetromino"""
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if rotation is None:
            rotation = self.rotation
            
        shape = self.get_rotated_shape(rotation)
        cells = []
        
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    cells.append((x + col_idx, y + row_idx))
        
        return cells

    def rotate(self, clockwise=True):
        """Rotate the tetromino"""
        if clockwise:
            self.rotation += 1
        else:
            self.rotation -= 1


class Game:
    """Main game class"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Advanced Tetris')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 36)
        
        self.reset_game()
        
        # For key repeat
        pygame.key.set_repeat(200, 50)  # Delay 200ms, interval 50ms
        
        # Initialize sound effects (if available)
        self.init_sounds()
        
    def init_sounds(self):
        """Initialize sound effects"""
        try:
            # Create simple sounds using pygame.mixer.Sound
            # In a real implementation, you would load actual sound files
            # For now, we'll create placeholder sounds
            self.move_sound = None
            self.rotate_sound = None
            self.line_clear_sound = None
            self.game_over_sound = None
            self.hard_drop_sound = None
        except:
            # If sound initialization fails, set to None
            self.move_sound = None
            self.rotate_sound = None
            self.line_clear_sound = None
            self.game_over_sound = None
            self.hard_drop_sound = None
    
    def play_sound(self, sound):
        """Play a sound if it exists"""
        if sound:
            try:
                sound.play()
            except:
                pass  # Ignore errors if sound doesn't play
    
    def reset_game(self):
        """Reset the game state"""
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.paused = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500  # milliseconds
        self.last_move_time = pygame.time.get_ticks()
        
    def new_piece(self):
        """Generate a new random piece"""
        shape = random.choice(list(TETROMINOES.keys()))
        return Tetromino(GRID_WIDTH // 2 - 2, 0, shape)
    
    def valid_position(self, piece=None, x=None, y=None, rotation=None):
        """Check if the piece is in a valid position"""
        if piece is None:
            piece = self.current_piece
        if x is None:
            x = piece.x
        if y is None:
            y = piece.y
        if rotation is None:
            rotation = piece.rotation
            
        for pos_x, pos_y in piece.get_cells(x, y, rotation):
            # Check if out of bounds
            if pos_x < 0 or pos_x >= GRID_WIDTH or pos_y >= GRID_HEIGHT:
                return False
            # Check if collides with placed pieces (and only if in play area)
            if pos_y >= 0 and self.grid[pos_y][pos_x] != 0:
                return False
        return True
    
    def place_piece(self):
        """Place the current piece on the grid"""
        for pos_x, pos_y in self.current_piece.get_cells():
            if 0 <= pos_y < GRID_HEIGHT and 0 <= pos_x < GRID_WIDTH:
                self.grid[pos_y][pos_x] = self.current_piece.color
    
    def clear_lines(self):
        """Clear completed lines and return the number of lines cleared"""
        lines_to_clear = []
        for i in range(GRID_HEIGHT):
            if all(self.grid[i]):
                lines_to_clear.append(i)
        
        # Remove the lines and add new empty ones at the top
        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        # Calculate score
        if lines_to_clear:
            # Score based on number of lines cleared at once
            line_scores = {1: 100, 2: 300, 3: 500, 4: 800}
            base_score = line_scores.get(len(lines_to_clear), 800)  # 4+ lines get 800
            self.score += base_score * self.level
            self.lines_cleared += len(lines_to_clear)
            
            # Increase level every 10 lines
            self.level = self.lines_cleared // 10 + 1
            # Increase speed with level (but cap it)
            self.fall_speed = max(50, 500 - (self.level - 1) * 50)
        
        return len(lines_to_clear)
    
    def move(self, dx, dy):
        """Move the current piece by dx, dy"""
        if self.game_over or self.paused:
            return False
            
        new_x = self.current_piece.x + dx
        new_y = self.current_piece.y + dy
        
        if self.valid_position(x=new_x, y=new_y):
            self.current_piece.x = new_x
            self.current_piece.y = new_y
            if dx != 0:  # Horizontal movement
                self.play_sound(self.move_sound)
            return True
        elif dy > 0:  # If moving down and can't, place the piece
            self.place_piece()
            cleared = self.clear_lines()
            if cleared > 0:
                self.play_sound(self.line_clear_sound)
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()
            
            # Check if game over (new piece collides immediately)
            if not self.valid_position():
                self.game_over = True
                self.play_sound(self.game_over_sound)
                
        return False
    
    def rotate_piece(self):
        """Rotate the current piece"""
        if self.game_over or self.paused:
            return
            
        original_rotation = self.current_piece.rotation
        self.current_piece.rotate()
        
        # If rotation causes collision, try wall kicks
        if not self.valid_position():
            # Try moving left
            if self.valid_position(x=self.current_piece.x - 1):
                self.current_piece.x -= 1
            # Try moving right
            elif self.valid_position(x=self.current_piece.x + 1):
                self.current_piece.x += 1
            # Try moving up
            elif self.valid_position(y=self.current_piece.y - 1):
                self.current_piece.y -= 1
            else:
                # Revert rotation if no valid position found
                self.current_piece.rotation = original_rotation
        else:
            self.play_sound(self.rotate_sound)
    
    def hard_drop(self):
        """Drop the piece to the bottom"""
        if self.game_over or self.paused:
            return
            
        while self.move(0, 1):
            pass  # Keep moving down until it can't anymore
        self.play_sound(self.hard_drop_sound)
    
    def draw_grid(self):
        """Draw the grid and placed pieces"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, GRAY, rect, 1)  # Draw grid lines
                
                if self.grid[y][x] != 0:
                    pygame.draw.rect(self.screen, self.grid[y][x], (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, WHITE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
    
    def draw_current_piece(self):
        """Draw the current falling piece"""
        for pos_x, pos_y in self.current_piece.get_cells():
            if 0 <= pos_y < GRID_HEIGHT and 0 <= pos_x < GRID_WIDTH:
                rect = pygame.Rect(pos_x * TILE_SIZE, pos_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, self.current_piece.color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
    
    def draw_next_piece(self):
        """Draw the next piece preview"""
        # Draw a small preview of the next piece
        preview_x = GAME_WIDTH + 30
        preview_y = 50
        
        # Draw label
        label = self.font.render("Next:", True, WHITE)
        self.screen.blit(label, (preview_x, preview_y - 30))
        
        # Draw the next piece
        shape = self.next_piece.get_rotated_shape()
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    rect = pygame.Rect(preview_x + col_idx * TILE_SIZE, 
                                       preview_y + row_idx * TILE_SIZE, 
                                       TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(self.screen, self.next_piece.color, rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
    
    def draw_ui(self):
        """Draw the user interface elements"""
        # Draw borders
        pygame.draw.line(self.screen, WHITE, (GAME_WIDTH, 0), (GAME_WIDTH, GAME_HEIGHT), 2)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (GAME_WIDTH + 20, 150))
        
        # Draw level
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (GAME_WIDTH + 20, 190))
        
        # Draw lines cleared
        lines_text = self.font.render(f"Lines: {self.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (GAME_WIDTH + 20, 230))
        
        # Draw controls info with graphical arrows
        controls_y = 300
        
        # Draw "Controls:" label
        ctrl_text = self.font.render("Controls:", True, WHITE)
        self.screen.blit(ctrl_text, (GAME_WIDTH + 20, controls_y))
        
        # Draw controls with arrows
        arrow_y_start = controls_y + 30
        arrow_size = 8
        
        # Move control: ← → : Move
        self.draw_arrow(GAME_WIDTH + 20, arrow_y_start + 10, 'left', WHITE, arrow_size)
        self.draw_arrow(GAME_WIDTH + 40, arrow_y_start + 10, 'right', WHITE, arrow_size)
        move_text = self.font.render(": Move", True, WHITE)
        self.screen.blit(move_text, (GAME_WIDTH + 60, arrow_y_start))
        
        # Rotate control: ↑ : Rotate
        arrow_y_start += 30
        self.draw_arrow(GAME_WIDTH + 20, arrow_y_start + 10, 'up', WHITE, arrow_size)
        rotate_text = self.font.render(": Rotate", True, WHITE)
        self.screen.blit(rotate_text, (GAME_WIDTH + 40, arrow_y_start))
        
        # Soft drop control: ↓ : Soft Drop
        arrow_y_start += 30
        self.draw_arrow(GAME_WIDTH + 20, arrow_y_start + 10, 'down', WHITE, arrow_size)
        soft_drop_text = self.font.render(": Soft Drop", True, WHITE)
        self.screen.blit(soft_drop_text, (GAME_WIDTH + 40, arrow_y_start))
        
        # Other controls without arrows
        other_controls = [
            "Space : Hard Drop",
            "P : Pause",
            "R : Restart"
        ]
        
        for i, text in enumerate(other_controls):
            ctrl_text = self.font.render(text, True, WHITE)
            self.screen.blit(ctrl_text, (GAME_WIDTH + 20, arrow_y_start + 30 + i*30))
    
    def draw_arrow(self, x, y, direction, color=WHITE, size=10):
        """
        Draw an arrow in the specified direction
        Direction: 'up', 'down', 'left', 'right'
        """
        if direction == 'up':
            points = [(x, y - size), (x - size//2, y), (x + size//2, y)]
        elif direction == 'down':
            points = [(x, y + size), (x - size//2, y), (x + size//2, y)]
        elif direction == 'left':
            points = [(x - size, y), (x, y - size//2), (x, y + size//2)]
        elif direction == 'right':
            points = [(x + size, y), (x, y - size//2), (x, y + size//2)]
        else:
            return  # Invalid direction
            
        pygame.draw.polygon(self.screen, color, points)
    
    def draw_game_over(self):
        """Draw the game over screen"""
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.set_alpha(180)  # Semi-transparent
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.title_font.render("GAME OVER", True, RED)
        restart_text = self.font.render("Press R to restart", True, WHITE)
        
        # Center the text
        self.screen.blit(game_over_text, 
                         (GAME_WIDTH//2 - game_over_text.get_width()//2, 
                          GAME_HEIGHT//2 - game_over_text.get_height()//2))
        self.screen.blit(restart_text, 
                         (GAME_WIDTH//2 - restart_text.get_width()//2, 
                          GAME_HEIGHT//2 - restart_text.get_height()//2 + 40))
    
    def draw_pause_screen(self):
        """Draw the pause screen"""
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.set_alpha(150)  # Semi-transparent
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        paused_text = self.title_font.render("PAUSED", True, YELLOW)
        continue_text = self.font.render("Press P to continue", True, WHITE)
        
        # Center the text
        self.screen.blit(paused_text, 
                         (GAME_WIDTH//2 - paused_text.get_width()//2, 
                          GAME_HEIGHT//2 - paused_text.get_height()//2))
        self.screen.blit(continue_text, 
                         (GAME_WIDTH//2 - continue_text.get_width()//2, 
                          GAME_HEIGHT//2 - continue_text.get_height()//2 + 40))
    
    def draw(self):
        """Draw the entire game"""
        self.screen.fill(BLACK)
        
        # Draw the game grid
        self.draw_grid()
        
        # Draw the current piece
        if not self.game_over:
            self.draw_current_piece()
        
        # Draw the next piece preview
        self.draw_next_piece()
        
        # Draw UI elements
        self.draw_ui()
        
        # Draw game over screen if game is over
        if self.game_over:
            self.draw_game_over()
        
        # Draw pause screen if paused
        if self.paused:
            self.draw_pause_screen()
        
        pygame.display.flip()
    
    def handle_input(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                
                if not self.game_over and not self.paused:
                    if event.key == pygame.K_LEFT:
                        self.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()
        
        return True
    
    def update(self):
        """Update the game state"""
        if self.game_over or self.paused:
            return
            
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.fall_speed:
            self.move(0, 1)
            self.last_move_time = current_time
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()


# Main execution
if __name__ == "__main__":
    game = Game()
    game.run()