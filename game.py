"""Main game class."""
import pygame
import sys
import os
from config import DEFAULT_FONT_SIZE, BG_IMAGE_PATH
from engine.resource_loader import ResourceManager
from engine.display import initialize_window

class Game:
    # Constructor
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
            if os.path.exists(BG_IMAGE_PATH):
                self.resources.load_image("main_menu_bg", BG_IMAGE_PATH)
            else:
                print(f"Warning: Main menu background image not found at {BG_IMAGE_PATH}")
            
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
            from screens.menu_system import MainMenu, GameConfig
            from engine.music import MusicManager
            
            # Create required dependencies
            music_manager = MusicManager()
            config = GameConfig(music_manager)
            
            # Create and run the main menu with proper configuration
            menu = MainMenu(config)
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
        print("Exiting game. Cleaning up and shutting down...")
        self.running = False
        pygame.quit()
        sys.exit(0)  # Use 0 to indicate normal exit
