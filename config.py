"""Game configuration settings."""
from typing import Tuple

# Display settings
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
GAME_TITLE: str = "Fantasy Falls"

# Asset paths
MAIN_MENU_BG: str = "assets/Images/MainMenuBackground.png"
SOUNDS_DIR: str = "assets/audio"
IMAGES_DIR: str = "assets/images"

# Font settings
DEFAULT_FONT_SIZE: int = 60
BUTTON_FONT_SIZE: int = 32
SMALL_FONT_SIZE: int = 24
TITLE_FONT_SIZE: int = 48

# Colors
BACKGROUND_COLOR: Tuple[int, int, int] = (40, 44, 52)
TEXT_COLOR: Tuple[int, int, int] = (220, 220, 220)
HOVER_COLOR: Tuple[int, int, int, int] = (100, 100, 150, 180)
HOVER_TEXT_COLOR: Tuple[int, int, int] = (255, 255, 0)
