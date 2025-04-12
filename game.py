"""Main game class."""
import pygame
import sys
# from engine.resource_loader import ResourceManager
from screens.menu_system import MenuBaseStateController, MenuConfig
from engine.music import MusicManager
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GAME_TITLE,
)

class Game:
    # Constructor
    def __init__(self):
        self.running = False
        self.screen = None
        # self.resources = ResourceManager()
        self.clock = None

    def run_main_menu(self):
        """Run the main menu game loop."""
        try:
            pygame.init()
            pygame.mixer.init()

            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            pygame.display.set_caption(GAME_TITLE)


            # Create required dependencies
            music_manager = MusicManager()
            config = MenuConfig(music_manager)
            
            # Create and run the main menu with proper configuration
            menu = MenuBaseStateController(config)
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
