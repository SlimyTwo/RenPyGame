"""Game configuration settings."""
from typing import Tuple
import os

# === Display Settings ===
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
GAME_TITLE: str = "Fantasy Falls"

# === Asset Directories ===
SOUNDS_DIR: str = "assets/audio"
IMAGES_DIR: str = "assets/images"

# === Specific Asset Paths ===
BG_IMAGE_PATH: str = os.path.join(IMAGES_DIR, "MainMenuBackground.png")
CLICK_SOUND_PATH: str = os.path.join(SOUNDS_DIR, "click.wav")
HOVER_SOUND_PATH: str = os.path.join(SOUNDS_DIR, "hover.wav")
BACKGROUND_MUSIC_PATH: str = os.path.join(SOUNDS_DIR, "background_music.mp3")

# === Font Settings ===
DEFAULT_FONT_SIZE: int = 60
BUTTON_FONT_SIZE: int = 32
SMALL_FONT_SIZE: int = 24
TITLE_FONT_SIZE: int = 48

# === UI Colors ===
BACKGROUND_COLOR: Tuple[int, int, int] = (40, 44, 52)               # Menu background color
TEXT_COLOR: Tuple[int, int, int] = (220, 220, 220)                  # Regular text color
HOVER_COLOR: Tuple[int, int, int, int] = (100, 100, 150, 180)       # Button hover overlay color (RGBA)
HOVER_TEXT_COLOR: Tuple[int, int, int] = (255, 255, 0)              # Text color on hover
