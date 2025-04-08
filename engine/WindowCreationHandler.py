import pygame
from typing import Optional
from engine.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GAME_TITLE,
    MAIN_MENU_BG,
    DEFAULT_FONT_SIZE
)

class WindowManager:
    """Class to handle window creation and management of a Pygame window."""

    def __init__(self) -> None:
        """
        Initialize the WindowManager with no active screen, font, or background.
        """
        self.screen: Optional[pygame.Surface] = None
        self.font: Optional[pygame.font.Font] = None
        self.background: Optional[pygame.Surface] = None

    def initialize_window(self) -> pygame.Surface:
        """
        Initialize Pygame and create the main game window.

        Returns:
            pygame.Surface: The Pygame display surface representing the game window.
        """
        pygame.init()
        pygame.mixer.init()

        # Create screen and set window caption
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(GAME_TITLE)

        # Initialize default font
        self.font = pygame.font.SysFont("", DEFAULT_FONT_SIZE)

        # Attempt to load background image
        try:
            self.background = pygame.image.load(MAIN_MENU_BG).convert()
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            self.background = None

        return self.screen

    def get_screen(self) -> Optional[pygame.Surface]:
        """
        Retrieve the current Pygame display surface.

        Returns:
            Optional[pygame.Surface]: The current screen surface if available, otherwise None.
        """
        return self.screen

    def get_font(self) -> Optional[pygame.font.Font]:
        """
        Retrieve the default font loaded for text rendering.

        Returns:
            Optional[pygame.font.Font]: The loaded Pygame font if available, otherwise None.
        """
        return self.font

    def get_background(self) -> Optional[pygame.Surface]:
        """
        Retrieve the loaded background image.

        Returns:
            Optional[pygame.Surface]: The background surface if loading succeeded, otherwise None.
        """
        return self.background


# Create a default instance for easy, global-like access
window_manager: WindowManager = WindowManager()

def initialize_window() -> pygame.Surface:
    """
    Compatibility function to initialize the Pygame window using WindowManager.

    Returns:
        pygame.Surface: The created Pygame screen surface.
    """
    return window_manager.initialize_window()

# Backward compatibility alias
InitializeWindowCreation = initialize_window
