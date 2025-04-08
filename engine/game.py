"""Main game class."""
import pygame
import sys
import os
from engine.config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, DEFAULT_FONT_SIZE, MAIN_MENU_BG
from engine.resource_manager import ResourceManager
from engine.WindowCreationHandler import initialize_window

class Game:
    def __init__(self):
        self.running = False
        self.screen = None
        self.resources = ResourceManager()
        self.clock = None
        
    def initialize(self):
        """Initialize pygame and create window."""
        try:
            # Use the existing window creation function
            self.screen = initialize_window()
            
            # Create a clock for controlling frame rate
            self.clock = pygame.time.Clock()
            
            # Load common resources
            self.resources.load_font("default", "", DEFAULT_FONT_SIZE)
            self.resources.load_font("button", "", 32)
            self.resources.load_font("small", "", 24)
            self.resources.load_font("title", "", 48)
            
            # Load main menu background
            if os.path.exists(MAIN_MENU_BG):
                self.resources.load_image("main_menu_bg", MAIN_MENU_BG)
            else:
                print(f"Warning: Main menu background image not found at {MAIN_MENU_BG}")
            
            self.running = True
            return self
        except Exception as e:
            print(f"Error initializing game: {e}")
            import traceback
            traceback.print_exc()
            pygame.quit()
            sys.exit(1)
    
    def run_main_menu(self):
        """Run the main menu game loop."""
        try:
            from screens.MainMenuGameLoop import MainMenu
            
            # Create and run the main menu directly
            menu = MainMenu()
            menu.run()
            
            # If we return from the menu and quit was selected
            if not menu.running:
                self.running = False
        except Exception as e:
            print(f"Error in main menu: {e}")
            import traceback
            traceback.print_exc()
            self.running = False
        
    def quit(self):
        """Clean up and quit the game."""
        self.running = False
        pygame.quit()
        sys.exit(0)  # Use 0 to indicate normal exit
