"""Snake game implementation."""
import pygame
import random
from typing import List, Tuple, Optional

class SnakeGame:
    """
    Simple Snake game implementation that runs in the existing pygame window.
    """
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    DARK_GREEN = (0, 100, 0)
    
    # Directions
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        """Initialize the Snake game with the given screen and clock."""
        self.screen = screen
        self.clock = clock
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Game settings
        self.cell_size = 20
        self.grid_width = self.screen_width // self.cell_size
        self.grid_height = self.screen_height // self.cell_size
        
        # Game state
        self.running = True
        self.paused = False
        self.game_over = False
        self.escape_overlay = False  # New state for escape overlay
        self.score = 0
        self.high_score = 0
        
        # Init font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Overlay buttons
        self.overlay_buttons = []
        self.create_overlay_buttons()
        
        # Init game
        self.initialize_game()
    
    def create_overlay_buttons(self):
        """Create buttons for the escape overlay"""
        button_width = 200
        button_height = 50
        button_spacing = 20
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Resume button
        self.resume_button = {
            'rect': pygame.Rect(center_x - button_width//2, center_y - 60, button_width, button_height),
            'text': "Resume Game",
            'action': self.resume_game,
            'color': (100, 100, 200),
            'hover_color': (150, 150, 255),
            'hovered': False
        }
        
        # Main Menu button
        self.menu_button = {
            'rect': pygame.Rect(center_x - button_width//2, center_y, button_width, button_height),
            'text': "Return to Main Menu",
            'action': self.return_to_menu,
            'color': (100, 200, 100),
            'hover_color': (150, 255, 150),
            'hovered': False
        }
        
        # Quit button
        self.quit_button = {
            'rect': pygame.Rect(center_x - button_width//2, center_y + 60, button_width, button_height),
            'text': "Quit Game",
            'action': self.quit_game,
            'color': (200, 100, 100),
            'hover_color': (255, 150, 150),
            'hovered': False
        }
        
        self.overlay_buttons = [self.resume_button, self.menu_button, self.quit_button]
    
    def initialize_game(self):
        """Set up the initial game state."""
        # Initialize snake in the middle of the screen
        x = self.grid_width // 2
        y = self.grid_height // 2
        self.snake: List[Tuple[int, int]] = [(x, y), (x-1, y), (x-2, y)]
        
        # Initial direction
        self.direction = self.RIGHT
        self.next_direction = self.RIGHT
        
        # Place initial food
        self.food = self.place_food()
        
        # Reset states
        self.game_over = False
        self.score = 0
        self.speed = 10  # Initial FPS
    
    def place_food(self) -> Tuple[int, int]:
        """Place food at a random empty position."""
        while True:
            food = (
                random.randint(0, self.grid_width - 1),
                random.randint(0, self.grid_height - 1)
            )
            # Make sure food is not on snake
            if food not in self.snake:
                return food
    
    def handle_events(self) -> bool:
        """Process user input events. Returns True if should exit to menu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return True
                
            if event.type == pygame.KEYDOWN:
                # ESC key now toggles the escape overlay
                if event.key == pygame.K_ESCAPE:
                    if self.escape_overlay:
                        self.escape_overlay = False
                    else:
                        self.escape_overlay = True
                        self.paused = True  # Pause the game when showing overlay
                # Game state keys
                elif event.key == pygame.K_p and not self.escape_overlay:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over and not self.escape_overlay:
                    self.initialize_game()
                
                # Snake direction keys (only if not in escape overlay)
                elif not self.escape_overlay:
                    if event.key in (pygame.K_UP, pygame.K_w) and self.direction != self.DOWN:
                        self.next_direction = self.UP
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and self.direction != self.UP:
                        self.next_direction = self.DOWN
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and self.direction != self.RIGHT:
                        self.next_direction = self.LEFT
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and self.direction != self.LEFT:
                        self.next_direction = self.RIGHT
            
            # Handle mouse events for the overlay
            if self.escape_overlay:
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check button hover states
                    for button in self.overlay_buttons:
                        button['hovered'] = button['rect'].collidepoint(mouse_pos)
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.overlay_buttons:
                        if button['rect'].collidepoint(mouse_pos):
                            return button['action']()
                    
        return False  # Continue game
    
    def resume_game(self) -> bool:
        """Resume the game"""
        self.escape_overlay = False
        self.paused = False
        return False  # Don't exit to menu
    
    def return_to_menu(self) -> bool:
        """Return to the main menu"""
        return True  # Exit to menu
    
    def quit_game(self) -> bool:
        """Quit the entire game"""
        self.running = False
        pygame.quit()
        import sys
        sys.exit()
    
    def update(self):
        """Update the game state."""
        if self.paused or self.game_over or self.escape_overlay:
            return
            
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % self.grid_width, 
                    (head_y + dy) % self.grid_height)
        
        # Check for collision with self
        if new_head in self.snake:
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            return
            
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check for food
        if new_head == self.food:
            # Snake grows, don't remove tail
            self.score += 1
            # Increase speed every 5 points
            if self.score % 5 == 0:
                self.speed = min(20, self.speed + 1)
            # Place new food
            self.food = self.place_food()
        else:
            # Remove tail
            self.snake.pop()
    
    def draw_cell(self, x: int, y: int, color: Tuple[int, int, int]):
        """Draw a cell at the given grid coordinates."""
        pygame.draw.rect(
            self.screen, 
            color, 
            pygame.Rect(
                x * self.cell_size, 
                y * self.cell_size, 
                self.cell_size, 
                self.cell_size
            )
        )
    
    def draw_grid(self):
        """Draw a light grid for visual reference."""
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                pygame.draw.rect(
                    self.screen,
                    (30, 30, 30),
                    pygame.Rect(
                        x * self.cell_size,
                        y * self.cell_size,
                        self.cell_size,
                        self.cell_size
                    ),
                    1  # Line width
                )
    
    def draw_escape_overlay(self):
        """Draw the escape menu overlay"""
        # Semi-transparent background
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with 70% opacity
        self.screen.blit(overlay, (0, 0))
        
        # Draw title
        title_text = self.font.render("Game Paused", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 120))
        self.screen.blit(title_text, title_rect)
        
        # Draw buttons
        for button in self.overlay_buttons:
            # Draw button background
            color = button['hover_color'] if button['hovered'] else button['color']
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=5)
            pygame.draw.rect(self.screen, self.WHITE, button['rect'], 2, border_radius=5)  # Button border
            
            # Draw button text
            btn_text = self.font.render(button['text'], True, self.WHITE)
            text_rect = btn_text.get_rect(center=button['rect'].center)
            self.screen.blit(btn_text, text_rect)
    
    def draw(self):
        """Render the game state."""
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Draw grid
        self.draw_grid()
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            color = self.GREEN if i > 0 else self.DARK_GREEN  # Different color for head
            self.draw_cell(x, y, color)
            
            # Add eyes to head
            if i == 0:
                eye_size = self.cell_size // 5
                eye_offset = self.cell_size // 3
                
                # Position eyes based on direction
                if self.direction == self.RIGHT:
                    left_eye = (x * self.cell_size + self.cell_size - eye_offset, y * self.cell_size + eye_offset)
                    right_eye = (x * self.cell_size + self.cell_size - eye_offset, y * self.cell_size + self.cell_size - eye_offset)
                elif self.direction == self.LEFT:
                    left_eye = (x * self.cell_size + eye_offset, y * self.cell_size + eye_offset)
                    right_eye = (x * self.cell_size + eye_offset, y * self.cell_size + self.cell_size - eye_offset)
                elif self.direction == self.UP:
                    left_eye = (x * self.cell_size + eye_offset, y * self.cell_size + eye_offset)
                    right_eye = (x * self.cell_size + self.cell_size - eye_offset, y * self.cell_size + eye_offset)
                else:  # DOWN
                    left_eye = (x * self.cell_size + eye_offset, y * self.cell_size + self.cell_size - eye_offset)
                    right_eye = (x * self.cell_size + self.cell_size - eye_offset, y * self.cell_size + self.cell_size - eye_offset)
                
                pygame.draw.circle(self.screen, self.WHITE, left_eye, eye_size)
                pygame.draw.circle(self.screen, self.WHITE, right_eye, eye_size)
        
        # Draw food
        food_x, food_y = self.food
        self.draw_cell(food_x, food_y, self.RED)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw high score
        high_score_text = self.small_font.render(f"High Score: {self.high_score}", True, self.WHITE)
        self.screen.blit(high_score_text, (10, 50))
        
        # Game state messages
        if self.game_over and not self.escape_overlay:
            game_over_text = self.font.render("GAME OVER - Press R to Restart", True, self.RED)
            text_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(game_over_text, text_rect)
        
        if self.paused and not self.game_over and not self.escape_overlay:
            paused_text = self.font.render("PAUSED - Press P to Resume", True, self.WHITE)
            text_rect = paused_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(paused_text, text_rect)
            
        # Draw escape overlay if active
        if self.escape_overlay:
            self.draw_escape_overlay()
            
        # Controls info
        controls_text = self.small_font.render("Controls: Arrow Keys/WASD to move, P to pause, ESC for menu", True, self.WHITE)
        self.screen.blit(controls_text, (10, self.screen_height - 30))
    
    def run(self) -> bool:
        """
        Run the snake game loop.
        Returns True if the game should transition back to the menu.
        """
        while self.running:
            # Handle events
            exit_to_menu = self.handle_events()
            if exit_to_menu or not self.running:
                return True
                
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Update display
            pygame.display.flip()
            
            # Cap frame rate based on current speed
            self.clock.tick(self.speed)
            
        return True
