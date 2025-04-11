"""Menu system core — manages the main menu loop, background, and menu state transitions."""

import os
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Type, Any

import pygame

# === UI Components ===
from ui.builders.button_builder import ButtonBuilder
from ui.components.button import Button

# === Engine ===
from engine.music import MusicManager

# === Configuration ===
from config import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    HOVER_COLOR,
    HOVER_TEXT_COLOR,
    CLICK_SOUND_PATH,
    HOVER_SOUND_PATH,
    BACKGROUND_MUSIC_PATH,
    BG_IMAGE_PATH
)

# === Setup Logging ===
logging.basicConfig(level=logging.INFO)

# Holds global user settings like fullscreen, music, and FPS display.
class MenuConfig:
    """
    Example config object that provides a music manager and some flags.
    Adapt this to your real config or inject dependencies as needed.
    """
    def __init__(self, music_manager: MusicManager) -> None:
        self.music_manager = music_manager
        self.fps_display_enabled: bool = music_manager.settings_manager.get_setting("fps_display", False)
        self.music_enabled: bool = music_manager.settings_manager.get_setting("music_enabled", True)
        self.fullscreen: bool = music_manager.settings_manager.get_setting("fullscreen", False)

# Abstract base for all individual menu screens (e.g., Main, Settings).
class AbstractMenuBase(ABC):
    """
    Abstract base class for menu states.
    """
    def __init__(self, menu_manager: 'MenuManager'):
        self.menu_manager = menu_manager
        self.screen = pygame.display.get_surface()
        self.screen_width, self.screen_height = self.screen.get_size()
        self.button_font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        self.buttons = []
        self.create_buttons()

    @abstractmethod
    def create_buttons(self) -> None:
        """Each menu state must implement its own button creation"""
        pass

    @abstractmethod
    def handle_events(self, event: pygame.event.Event) -> bool:
        """Handle state-specific events"""
        pass

    @abstractmethod
    def draw(self) -> None:
        """Draw the current state"""
        pass

    def cleanup(self) -> None:
        """Called when exiting this state"""
        # Default implementation - override if needed
        self.buttons.clear()

# Handles switching between and managing active menu states.
class MenuManager:
    """
    Manages transitions between menu states.
    """
    def __init__(self, base_menu: 'MenuBase'):
        self.base_menu = base_menu
        self.states: Dict[str, Type[AbstractMenuBase]] = {}
        self.current_state: Optional[AbstractMenuBase] = None

    def register_state(self, state_name: str, state_class: Type[AbstractMenuBase]) -> None:
        """Register a menu state with a name"""
        self.states[state_name] = state_class

    def transition_to(self, state_name: str) -> None:
        """Transition to a new state by name"""
        if state_name not in self.states:
            logging.error(f"State {state_name} not registered")
            return

        # Clean up current state if it exists
        if self.current_state:
            self.current_state.cleanup()

        # Create new state
        self.current_state = self.states[state_name](self)
        logging.info(f"Transitioned to {state_name} state")

    def handle_events(self, event: pygame.event.Event) -> bool:
        """Forward events to current state"""
        if self.current_state:
            return self.current_state.handle_events(event)
        return False

    def draw(self) -> None:
        """Draw the current state"""
        if self.current_state:
            self.current_state.draw()

# Base loop and rendering logic for the overall menu system.
class MenuBase:
    """
    Base class for a Pygame menu screen. Handles background drawing, event loops, etc.
    """
    def __init__(self, config: MenuConfig) -> None:
        self.config = config
        self.screen = pygame.display.get_surface()
        self.screen_width, self.screen_height = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.running: bool = True

        # Fonts
        self.button_font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)

        # Background handling
        self.original_bg: Optional[pygame.Surface] = None
        self.background_image: Optional[pygame.Surface] = None
        self.bg_pos = (0, 0)

        # Sound effect file paths (only if they exist)
        self.click_sound_path = CLICK_SOUND_PATH if os.path.exists(CLICK_SOUND_PATH) else None
        self.hover_sound_path = HOVER_SOUND_PATH if os.path.exists(HOVER_SOUND_PATH) else None

        # State management
        self.menu_manager = MenuManager(self)
        
        self.load_background_image()

    def load_background_image(self) -> None:
        """
        Load and scale a background image, if available.
        """
        self.screen_width, self.screen_height = self.screen.get_size()
        if self.original_bg is None and os.path.exists(BG_IMAGE_PATH):
            try:
                self.original_bg = pygame.image.load(BG_IMAGE_PATH)
            except Exception as e:
                logging.exception(f"Error loading background: {e}")
                self.original_bg = None

        if self.original_bg:
            bg_width, bg_height = self.original_bg.get_size()
            width_ratio = self.screen_width / bg_width
            height_ratio = self.screen_height / bg_height
            scale_factor = max(width_ratio, height_ratio)
            new_width = int(bg_width * scale_factor)
            new_height = int(bg_height * scale_factor)
            self.background_image = pygame.transform.scale(self.original_bg, (new_width, new_height))
            bg_x = (self.screen_width - new_width) // 2
            bg_y = (self.screen_height - new_height) // 2
            self.bg_pos = (bg_x, bg_y)
        else:
            self.background_image = None
            self.bg_pos = (0, 0)

    def draw_background(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        if self.background_image:
            self.screen.blit(self.background_image, self.bg_pos)

    def draw_fps_counter(self) -> None:
        if self.config.fps_display_enabled:
            fps = int(self.clock.get_fps())
            fps_text = self.small_font.render(f"FPS: {fps}", True, (255, 255, 0))
            self.screen.blit(fps_text, (10, 10))

    def toggle_fullscreen(self) -> None:
        """
        Toggle between fullscreen and windowed mode.
        """
        self.config.fullscreen = not self.config.fullscreen
        self.config.music_manager.settings_manager.set_setting("fullscreen", self.config.fullscreen)

        if self.config.fullscreen:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

        self.load_background_image()

        # Reset the current menu state
        if self.menu_manager.current_state:
            current_state_name = next(
                name for name, cls in self.menu_manager.states.items()
                if isinstance(self.menu_manager.current_state, cls)
            )
            self.menu_manager.transition_to(current_state_name)

    def handle_common_events(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.QUIT:
            self.running = False
            return True
        elif event.type == pygame.VIDEORESIZE:
            self.load_background_image()
            # Reload current state when resizing
            if self.menu_manager.current_state:
                current_state_name = next(name for name, cls in self.menu_manager.states.items() 
                                         if isinstance(self.menu_manager.current_state, cls))
                self.menu_manager.transition_to(current_state_name)
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.running = False
                return True
            elif event.key == pygame.K_F11:
                self.toggle_fullscreen()
                return True
        return False

    def run(self) -> bool:
        """
        Main menu loop using state pattern
        """
        while self.running:
            self.draw_background()

            for event in pygame.event.get():
                if self.handle_common_events(event):
                    continue
                
                # Let current state handle events
                self.menu_manager.handle_events(event)

            # Draw the current state
            self.menu_manager.draw()

            # Example text instructions (common across states)
            instructions = self.small_font.render(
                "Press TAB to navigate, ENTER to select, Q to quit, F11 for fullscreen",
                True, TEXT_COLOR
            )
            self.screen.blit(
                instructions,
                (self.screen_width // 2 - instructions.get_width() // 2, self.screen_height - 40)
            )

            self.draw_fps_counter()
            pygame.display.flip()
            self.clock.tick(60)

        return True

# Initializes and runs the full menu system with registered states handles the logic of the state pattern.
class MenuBaseStateController(MenuBase):
    """
    Main menu controller class that manages menu states.
    """
    def __init__(self, config: MenuConfig) -> None:
        super().__init__(config)
        
        # Import the menu states
        from screens.main_menu import MainAbstractMenuBase
        from screens.settings_menu import SettingsAbstractMenuBase
        from screens.test_menu import TestAbstractMenuBase
        
        # Register all menu states
        self.menu_manager.register_state("main", MainAbstractMenuBase)
        self.menu_manager.register_state("settings", SettingsAbstractMenuBase)
        self.menu_manager.register_state("test", TestAbstractMenuBase)
        
        # Start with the main menu state
        self.menu_manager.transition_to("main")

        # If the user wants the game to start with music
        if self.config.music_enabled and os.path.exists(BACKGROUND_MUSIC_PATH):
            self.config.music_manager.play_music(BACKGROUND_MUSIC_PATH)
