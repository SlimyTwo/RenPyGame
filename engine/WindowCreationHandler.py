import pygame
from engine.config import (
    SCREEN_WIDTH, 
    SCREEN_HEIGHT, 
    GAME_TITLE, 
    MAIN_MENU_BG,
    DEFAULT_FONT_SIZE
)

class WindowManager:
    """Class to handle window creation and management."""
    
    def __init__(self):
        self.screen = None
        self.font = None
        self.background = None
        
    def initialize_window(self):
        """Initialize pygame and create the game window."""
        pygame.init()
        pygame.mixer.init()

        # Create screen and set caption
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(GAME_TITLE)
        
        # Initialize default font
        self.font = pygame.font.SysFont("", DEFAULT_FONT_SIZE)

        # Load background image
        try:
            self.background = pygame.image.load(MAIN_MENU_BG).convert()
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            self.background = None
        
        return self.screen
    
    def get_screen(self):
        """Return the current screen surface."""
        return self.screen
    
    def get_font(self):
        """Return the default font."""
        return self.font
    
    def get_background(self):
        """Return the background image."""
        return self.background

# Create a default instance for easy access
window_manager = WindowManager()

def initialize_window():
    """Initialize pygame and create the game window (compatibility function)."""
    return window_manager.initialize_window()

# For backward compatibility
InitializeWindowCreation = initialize_window
