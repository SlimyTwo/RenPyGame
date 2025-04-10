# main_menu.py

import os
import logging
import pygame
from typing import Optional, Dict, Type, Any
from abc import ABC, abstractmethod

# Import your new ButtonBuilder instead of create_button
from ui.builders.button_builder import ButtonBuilder
from ui.components.button import Button
from engine.music import MusicManager

# Sample constants – adjust as needed
BACKGROUND_COLOR = (40, 44, 52)
TEXT_COLOR = (220, 220, 220)
HOVER_COLOR = (100, 100, 150, 180)
HOVER_TEXT_COLOR = (255, 255, 0)

CLICK_SOUND_PATH = os.path.join("assets", "audio", "click.wav")
HOVER_SOUND_PATH = os.path.join("assets", "audio", "hover.wav")
FOCUS_SOUND_PATH = os.path.join("assets", "audio", "focus.wav")
BACKGROUND_MUSIC_PATH = os.path.join("assets", "audio", "background_music.mp3")
BG_IMAGE_PATH = os.path.join("assets", "images", "MainMenuBackground.png")


class GameConfig:
    """
    Example config object that provides a music manager and some flags.
    Adapt this to your real config or inject dependencies as needed.
    """
    def __init__(self, music_manager: MusicManager) -> None:
        self.music_manager = music_manager
        self.fps_display_enabled: bool = music_manager.settings_manager.get_setting("fps_display", False)
        self.music_enabled: bool = music_manager.settings_manager.get_setting("music_enabled", True)
        self.fullscreen: bool = music_manager.settings_manager.get_setting("fullscreen", False)


class MenuState(ABC):
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


class MenuManager:
    """
    Manages transitions between menu states.
    """
    def __init__(self, base_menu: 'MenuBase'):
        self.base_menu = base_menu
        self.states: Dict[str, Type[MenuState]] = {}
        self.current_state: Optional[MenuState] = None

    def register_state(self, state_name: str, state_class: Type[MenuState]) -> None:
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


class MenuBase:
    """
    Base class for a Pygame menu screen. Handles background drawing, event loops, etc.
    """
    def __init__(self, config: GameConfig) -> None:
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
        self.focus_sound_path = FOCUS_SOUND_PATH if os.path.exists(FOCUS_SOUND_PATH) else None

        # Fullscreen state
        self.is_fullscreen: bool = bool(self.screen.get_flags() & pygame.FULLSCREEN)

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
        Example toggle logic.
        """
        self.is_fullscreen = not self.is_fullscreen
        self.config.fullscreen = self.is_fullscreen
        self.config.music_manager.settings_manager.set_setting("fullscreen", self.is_fullscreen)

        if self.is_fullscreen:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

        self.load_background_image()
        
        # When changing screen mode, we should reset the menu state
        if self.menu_manager.current_state:
            current_state_name = next(name for name, cls in self.menu_manager.states.items() 
                                     if isinstance(self.menu_manager.current_state, cls))
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


class MainMenuState(MenuState):
    """
    Main menu state implementation
    """
    def __init__(self, menu_manager: MenuManager):
        super().__init__(menu_manager)
        self.title = "Main Menu"
        
        # If music enabled
        config = self.menu_manager.base_menu.config
        if config.music_enabled and os.path.exists(BACKGROUND_MUSIC_PATH):
            config.music_manager.play_music(BACKGROUND_MUSIC_PATH)

    def create_buttons(self) -> None:
        """Create main menu buttons"""
        base_menu = self.menu_manager.base_menu
        config = base_menu.config
        
        # Button geometry and spacing
        button_width = 250
        button_height = 50
        button_spacing = 20

        # Start Game button
        start_game_btn = (
            ButtonBuilder(self.screen, self.button_font, text="Start Game")
            .set_size(button_width - 75, button_height)
            .set_offsets(0, -100)  # center horizontally, offset Y
            .set_hover_text("▶ Start Game ▶")
            .set_hover_text_color(HOVER_TEXT_COLOR)
            .set_tooltip("Start a new game")
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path, base_menu.focus_sound_path)
            .set_visible_background(False)
            .set_debug_hitbox(True)
            .set_music_manager(config.music_manager)
            .build()
        )
        start_game_btn.on_click = lambda: logging.info("Starting new game!")
        start_game_btn.set_focus(True)  # Initially focused
        
        # Load Game button (disabled)
        load_game_btn = (
            ButtonBuilder(self.screen, self.button_font, text="Load Game")
            .set_size(button_width, button_height)
            .set_offsets(0, -100 + button_height + button_spacing)
            .set_hover_text("Load Game (Unavailable)")
            .set_hover_text_color(HOVER_TEXT_COLOR)
            .set_tooltip("Load a saved game")
            .set_visible_background(False)
            .set_music_manager(config.music_manager)
            .set_disabled(True)
            .build()
        )
        
        # Settings button
        settings_btn = (
            ButtonBuilder(self.screen, self.button_font, text="Settings")
            .set_size(button_width, button_height)
            .set_offsets(0, -100 + (button_height + button_spacing) * 2)
            .set_hover_text("⚙ Settings ⚙")
            .set_hover_text_color(HOVER_TEXT_COLOR)
            .set_tooltip("Game settings")
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path, base_menu.focus_sound_path)
            .set_visible_background(False)
            .set_music_manager(config.music_manager)
            .build()
        )
        settings_btn.on_click = lambda: self.menu_manager.transition_to("settings")
        
        # Test Menu button
        test_btn = (
            ButtonBuilder(self.screen, self.button_font, text="Test Menu")
            .set_size(button_width, button_height)
            .set_offsets(0, -100 + (button_height + button_spacing) * 3)
            .set_hover_text("🧪 Test Menu 🧪")
            .set_hover_text_color(HOVER_TEXT_COLOR)
            .set_tooltip("Test features")
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path, base_menu.focus_sound_path)
            .set_visible_background(False)
            .set_music_manager(config.music_manager)
            .build()
        )
        test_btn.on_click = lambda: self.menu_manager.transition_to("test")
        
        # Quit button
        quit_btn = (
            ButtonBuilder(self.screen, self.button_font, text="Quit")
            .set_size(button_width, button_height)
            .set_offsets(0, -100 + (button_height + button_spacing) * 4)
            .set_hover_text("✖ Exit Game ✖")
            .set_hover_text_color((255, 100, 100))
            .set_tooltip("Exit the game")
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path, base_menu.focus_sound_path)
            .set_visible_background(False)
            .set_music_manager(config.music_manager)
            .build()
        )
        quit_btn.on_click = self.handle_quit
        
        self.buttons = [start_game_btn, load_game_btn, settings_btn, test_btn, quit_btn]

    def handle_events(self, event: pygame.event.Event) -> bool:
        """Handle events for this state"""
        for button in self.buttons:
            button.handle_event(event)
        return False
            
    def draw(self) -> None:
        """Draw the main menu state"""
        # Draw title
        title_text = self.title_font.render(self.title, True, TEXT_COLOR)
        self.screen.blit(
            title_text,
            (self.screen_width // 2 - title_text.get_width() // 2, 100)
        )
        
        # Draw all buttons
        for button in self.buttons:
            button.draw()
    
    def handle_quit(self) -> bool:
        """Handle quit button click"""
        self.menu_manager.base_menu.running = False
        return True


class MainMenu(MenuBase):
    """
    Main menu controller class that manages menu states.
    """
    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        
        # Import the other menu states here to avoid circular imports
        from screens.settings_menu import SettingsMenuState
        from screens.test_menu import TestMenuState
        
        # Register all menu states
        self.menu_manager.register_state("main", MainMenuState)
        self.menu_manager.register_state("settings", SettingsMenuState)
        self.menu_manager.register_state("test", TestMenuState)
        
        # Start with the main menu state
        self.menu_manager.transition_to("main")

        # If the user wants the game to start with music
        if self.config.music_enabled and os.path.exists(BACKGROUND_MUSIC_PATH):
            self.config.music_manager.play_music(BACKGROUND_MUSIC_PATH)


def run_main_menu_loop():
    """
    Example function that initializes Pygame and runs the main menu.
    """
    pygame.init()
    pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    music_manager = MusicManager()
    config = GameConfig(music_manager)
    main_menu = MainMenu(config)
    main_menu.run()
    pygame.quit()
