import pygame
import utility.GlobalVariables as gv  # gv = global variable alias
from engine.config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE

def initialize_window():
    """Initialize pygame and create the game window."""
    pygame.init()
    pygame.mixer.init()

    # Create and store shared screen + font
    gv.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(GAME_TITLE)
    gv.font = pygame.font.SysFont("", 60)

    # Load and store background image
    try:
        gv.background = pygame.image.load("assets/Images/MainMenuBackground.png").convert()
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        gv.background = None
    
    return gv.screen

# For backward compatibility
InitializeWindowCreation = initialize_window
