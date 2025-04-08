import os
import logging
from typing import Optional

import pygame
from buttons.ButtonClass import Button
from buttons.ButtonCreator import create_button, create_slider
from utility.MusicManager import MusicManager

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# === Constants for Colors and Asset Paths ===
BACKGROUND_COLOR = (40, 44, 52)
TEXT_COLOR = (220, 220, 220)
HOVER_COLOR = (100, 100, 150, 180)
HOVER_TEXT_COLOR = (255, 255, 0)

CLICK_SOUND_PATH = os.path.join("assets", "audio", "click.wav")
HOVER_SOUND_PATH = os.path.join("assets", "audio", "hover.wav")
FOCUS_SOUND_PATH = os.path.join("assets", "audio", "focus.wav")
BACKGROUND_MUSIC_PATH = os.path.join("assets", "audio", "background_music.mp3")
BG_IMAGE_PATH = os.path.join("assets", "images", "MainMenuBackground.png")


# === Configuration and Dependency Injection ===
class GameConfig:
    """
    Configuration object for game settings and dependencies.
    Acts as a central place to store settings loaded from the settings manager
    and to access shared services like the music manager.
    """
    def __init__(self, music_manager: MusicManager) -> None:
        self.music_manager = music_manager
        self.fps_display_enabled: bool = self.music_manager.settings_manager.get_setting("fps_display", False)
        self.music_enabled: bool = self.music_manager.settings_manager.get_setting("music_enabled", True)
        self.fullscreen: bool = self.music_manager.settings_manager.get_setting("fullscreen", False)


# === Base Menu Class ===
class MenuBase:
    """
    Base class for menu screens with common functionality.
    All menus receive a GameConfig instance as a dependency.
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

        # Background properties
        self.original_bg: Optional[pygame.Surface] = None
        self.background_image: Optional[pygame.Surface] = None
        self.bg_pos = (0, 0)

        # Sound effects (only if the file exists)
        self.click_sound_path: Optional[str] = CLICK_SOUND_PATH if os.path.exists(CLICK_SOUND_PATH) else None
        self.hover_sound_path: Optional[str] = HOVER_SOUND_PATH if os.path.exists(HOVER_SOUND_PATH) else None

        # Fullscreen state (from display flags)
        self.is_fullscreen: bool = bool(self.screen.get_flags() & pygame.FULLSCREEN)

    def load_background_image(self) -> None:
        """
        Load the background image and scale it so that it covers the entire screen.
        If the background image is missing or an error occurs, the method logs the error.
        """
        # Refresh dimensions in case the window was resized
        self.screen_width, self.screen_height = self.screen.get_size()
        try:
            if self.original_bg is None and os.path.exists(BG_IMAGE_PATH):
                self.original_bg = pygame.image.load(BG_IMAGE_PATH)

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
        except Exception as e:
            logging.exception(f"Error loading background image: {e}")
            self.background_image = None
            self.bg_pos = (0, 0)

    def draw_background(self) -> None:
        """
        Draw the background onto the screen.
        If a background image is available, it is blitted according to its pre‑computed position.
        """
        self.screen.fill(BACKGROUND_COLOR)
        if self.background_image:
            self.screen.blit(self.background_image, self.bg_pos)

    def draw_fps_counter(self) -> None:
        """
        Draw the frames-per-second counter on the screen if enabled in configuration.
        """
        if self.config.fps_display_enabled:
            fps = int(self.clock.get_fps())
            fps_text = self.small_font.render(f"FPS: {fps}", True, (255, 255, 0))
            self.screen.blit(fps_text, (10, 10))

    def toggle_fullscreen(self) -> None:
        """
        Toggle between fullscreen and windowed mode.
        Updates both the display mode and the persisted configuration setting.
        """
        self.is_fullscreen = not self.is_fullscreen
        self.config.fullscreen = self.is_fullscreen
        self.config.music_manager.settings_manager.set_setting("fullscreen", self.is_fullscreen)
        if self.is_fullscreen:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        # Clear and reset UI elements after display mode change
        Button.all_buttons.clear()
        self.load_background_image()
        self.create_buttons()

    def handle_common_events(self, event: pygame.event.Event) -> bool:
        """
        Handle events common to all menus (e.g. quit, fullscreen toggling, window resizing).
        Returns True if the event was fully handled.
        """
        if event.type == pygame.QUIT:
            self.running = False
            return True
        elif event.type == pygame.VIDEORESIZE:
            Button.all_buttons.clear()
            self.load_background_image()
            self.create_buttons()
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.running = False
                return True
            elif event.key == pygame.K_F11:
                self.toggle_fullscreen()
                return True
        return False

    def create_buttons(self) -> None:
        """
        Create and position buttons.
        This must be implemented in each subclass.
        """
        raise NotImplementedError

    def run(self) -> bool:
        """
        Main loop method for the menu.
        Must be implemented by subclasses.
        """
        raise NotImplementedError


# === Settings Menu ===
class SettingsMenu(MenuBase):
    """
    Settings menu that allows the user to toggle fullscreen, FPS display,
    music, and adjust volume levels.
    """
    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        self.back_btn = None
        self.fullscreen_btn = None
        self.fps_btn = None
        self.music_toggle_btn = None
        self.volume_slider = None
        self.master_volume_slider = None
        self.load_background_image()
        self.create_buttons()

    def create_buttons(self) -> None:
        """
        Create and position all buttons and sliders for the settings menu.
        """
        # Back button (top left)
        self.back_btn = create_button(
            self.screen, self.button_font, "← Back",
            width=120, height=40,
            x_offset=-self.screen_width // 2 + 80, y_offset=-self.screen_height // 2 + 40,
            hover_text="← Return",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Return to main menu",
            sound_path=self.click_sound_path,
            hover_sound_path=self.hover_sound_path,
            visible_background=True,
            music_manager=self.config.music_manager
        )
        # Fullscreen toggle button
        fullscreen_text = "Fullscreen: ON" if self.is_fullscreen else "Fullscreen: OFF"
        self.fullscreen_btn = create_button(
            self.screen, self.button_font, fullscreen_text,
            width=250, height=50,
            y_offset=-20,
            hover_text="Toggle Fullscreen Mode",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Switch between windowed and fullscreen modes",
            sound_path=self.click_sound_path,
            hover_sound_path=self.hover_sound_path,
            toggle_mode=True,
            toggled=self.is_fullscreen,
            music_manager=self.config.music_manager
        )
        # FPS counter toggle button
        fps_text = "FPS Counter: ON" if self.config.fps_display_enabled else "FPS Counter: OFF"
        self.fps_btn = create_button(
            self.screen, self.button_font, fps_text,
            width=250, height=50,
            y_offset=50,
            hover_text="Toggle FPS Display",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Show or hide frames per second counter",
            sound_path=self.click_sound_path,
            hover_sound_path=self.hover_sound_path,
            toggle_mode=True,
            toggled=self.config.fps_display_enabled,
            music_manager=self.config.music_manager
        )
        # Music toggle button
        music_text = "Music: ON" if self.config.music_enabled else "Music: OFF"
        self.music_toggle_btn = create_button(
            self.screen, self.button_font, music_text,
            width=250, height=50,
            y_offset=120,
            hover_text="Toggle Background Music",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Turn background music on or off",
            sound_path=self.click_sound_path,
            hover_sound_path=self.hover_sound_path,
            toggle_mode=True,
            toggled=self.config.music_enabled,
            music_manager=self.config.music_manager
        )
        # Master volume slider
        self.master_volume_slider = create_slider(
            self.screen, self.button_font,
            width=250, height=30,
            y_offset=200,
            min_value=0, max_value=100,
            current_value=int(self.config.music_manager.get_master_volume() * 100),
            label="Master Volume",
            sound_path=self.click_sound_path,
            hover_sound_path=self.hover_sound_path,
            music_manager=self.config.music_manager
        )
        # Music volume slider
        self.volume_slider = create_slider(
            self.screen, self.button_font,
            width=250, height=30,
            y_offset=280,
            min_value=0, max_value=100,
            current_value=int(self.config.music_manager.get_volume() * 100),
            label="Music Volume",
            sound_path=self.click_sound_path,
            hover_sound_path=self.hover_sound_path,
            music_manager=self.config.music_manager
        )
        # Attach event handlers for buttons and sliders
        self.back_btn.on_click = self.handle_back
        self.fullscreen_btn.on_click = self.handle_fullscreen_toggle
        self.fps_btn.on_click = self.handle_fps_toggle
        self.music_toggle_btn.on_click = self.handle_music_toggle
        self.volume_slider.on_value_change = self.handle_volume_change
        self.master_volume_slider.on_value_change = self.handle_master_volume_change
        self.back_btn.set_focus(True)

    def handle_back(self) -> bool:
        """Return to the main menu."""
        self.running = False
        return True

    def handle_fullscreen_toggle(self) -> bool:
        """Toggle fullscreen mode and update the corresponding button text."""
        self.toggle_fullscreen()
        fullscreen_text = "Fullscreen: ON" if self.is_fullscreen else "Fullscreen: OFF"
        self.fullscreen_btn.set_text(fullscreen_text)
        return True

    def handle_fps_toggle(self) -> bool:
        """Toggle FPS counter display."""
        self.config.fps_display_enabled = not self.config.fps_display_enabled
        self.config.music_manager.settings_manager.set_setting("fps_display", self.config.fps_display_enabled)
        fps_text = "FPS Counter: ON" if self.config.fps_display_enabled else "FPS Counter: OFF"
        self.fps_btn.set_text(fps_text)
        return True

    def handle_music_toggle(self) -> bool:
        """Toggle background music on or off."""
        self.config.music_enabled = not self.config.music_enabled
        self.config.music_manager.set_music_enabled(self.config.music_enabled)
        music_text = "Music: ON" if self.config.music_enabled else "Music: OFF"
        self.music_toggle_btn.set_text(music_text)
        if self.config.music_enabled:
            if not self.config.music_manager.is_playing() and os.path.exists(BACKGROUND_MUSIC_PATH):
                self.config.music_manager.play_music(BACKGROUND_MUSIC_PATH)
        else:
            self.config.music_manager.stop_music()
        return True

    def handle_volume_change(self, value: int) -> bool:
        """Update the music volume based on slider input."""
        volume = value / 100.0  # Convert percentage to 0.0–1.0 range
        self.config.music_manager.set_volume(volume)
        return True

    def handle_master_volume_change(self, value: int) -> bool:
        """Update the master volume based on slider input."""
        volume = value / 100.0  # Convert percentage to 0.0–1.0 range
        self.config.music_manager.set_master_volume(volume)
        return True

    def run(self) -> bool:
        """Run the settings menu loop."""
        self.running = True
        while self.running:
            self.draw_background()
            title_text = self.title_font.render("Settings", True, TEXT_COLOR)
            title_rect = title_text.get_rect(center=(self.screen_width // 2, 80))
            self.screen.blit(title_text, title_rect)
            for event in pygame.event.get():
                if self.handle_common_events(event):
                    continue
                Button.update_all(event)
                if self.volume_slider:
                    self.volume_slider.handle_event(event)
                if self.master_volume_slider:
                    self.master_volume_slider.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
            self.back_btn.draw()
            self.fullscreen_btn.draw()
            self.fps_btn.draw()
            self.music_toggle_btn.draw()
            self.master_volume_slider.draw()
            self.volume_slider.draw()
            instructions = self.small_font.render(
                "Press TAB to navigate, ENTER to select, ESC to go back, F11 for fullscreen",
                True, TEXT_COLOR
            )
            self.screen.blit(instructions,
                             (self.screen_width // 2 - instructions.get_width() // 2, self.screen_height - 40))
            self.draw_fps_counter()
            pygame.display.flip()
            self.clock.tick(60)
        Button.all_buttons.clear()
        return True


# === Main Menu ===
class MainMenu(MenuBase):
    """
    Main menu that provides options such as starting a game, loading a game,
    accessing settings, and quitting the game.
    """
    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        self.button_width = 250
        self.button_height = 50
        self.button_spacing = 20
        self.start_game_btn = None
        self.load_game_btn = None
        self.settings_btn = None
        self.quit_btn = None

        # Set display mode based on persisted fullscreen setting
        if self.config.fullscreen and not (self.screen.get_flags() & pygame.FULLSCREEN):
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        elif not self.config.fullscreen and (self.screen.get_flags() & pygame.FULLSCREEN):
            pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.is_fullscreen = bool(self.screen.get_flags() & pygame.FULLSCREEN)

        if self.config.music_enabled and os.path.exists(BACKGROUND_MUSIC_PATH):
            self.config.music_manager.play_music(BACKGROUND_MUSIC_PATH)
        self.load_background_image()
        self.create_buttons()

    def create_buttons(self) -> None:
        """Create and position all buttons for the main menu."""
        self.start_game_btn = create_button(
            self.screen, self.button_font, "Start Game",
            width=self.button_width, height=self.button_height,
            y_offset=-100,
            hover_text="▶ Start Game ▶",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Start a new game",
            sound_path=self.click_sound_path,
            hover_sound_path=self.hover_sound_path,
            visible_background=False,
            debug_hitbox=False,
            music_manager=self.config.music_manager
        )
        self.load_game_btn = create_button(
            self.screen, self.button_font, "Load Game",
            width=self.button_width, height=self.button_height,
            y_offset=-100 + self.button_height + self.button_spacing,
            hover_text="Load Game (Unavailable)",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Load a saved game",
            visible_background=False,
            debug_hitbox=False,
            disabled=True,
            music_manager=self.config.music_manager
        )
        self.settings_btn = create_button(
            self.screen, self.button_font, "Settings",
            width=self.button_width, height=self.button_height,
            y_offset=-100 + (self.button_height + self.button_spacing) * 2,
            hover_text="⚙ Settings ⚙",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Game settings",
            sound_path=self.click_sound_path,
            hover_sound_path=self.hover_sound_path,
            visible_background=False,
            debug_hitbox=False,
            music_manager=self.config.music_manager
        )
        self.quit_btn = create_button(
            self.screen, self.button_font, "Quit",
            width=self.button_width, height=self.button_height,
            y_offset=-100 + (self.button_height + self.button_spacing) * 3,
            hover_text="✖ Exit Game ✖",
            hover_text_color=(255, 100, 100),
            tooltip="Exit the game",
            sound_path=self.click_sound_path,
            hover_sound_path=self.hover_sound_path,
            visible_background=False,
            debug_hitbox=False,
            music_manager=self.config.music_manager
        )
        self.start_game_btn.on_click = self.handle_start_game
        self.settings_btn.on_click = self.handle_settings
        self.quit_btn.on_click = self.handle_quit
        self.start_game_btn.set_focus(True)

    def handle_start_game(self) -> bool:
        """
        Start a new game.
        Implement your game startup logic here.
        """
        # Game start logic goes here.
        return True

    def handle_settings(self) -> bool:
        """Open the settings menu and update the main menu afterwards."""
        Button.all_buttons.clear()
        settings_menu = SettingsMenu(self.config)
        settings_menu.run()
        self.load_background_image()
        self.create_buttons()
        return True

    def handle_quit(self) -> bool:
        """Exit the game."""
        self.running = False
        return True

    def run(self) -> bool:
        """Run the main menu loop."""
        self.running = True
        while self.running:
            self.draw_background()
            for event in pygame.event.get():
                if self.handle_common_events(event):
                    continue
                Button.update_all(event)
            self.start_game_btn.draw()
            self.load_game_btn.draw()
            self.settings_btn.draw()
            self.quit_btn.draw()
            instructions = self.small_font.render(
                "Press TAB to navigate, ENTER to select, Q to quit, F11 for fullscreen",
                True, TEXT_COLOR
            )
            self.screen.blit(instructions,
                             (self.screen_width // 2 - instructions.get_width() // 2, self.screen_height - 40))
            self.draw_fps_counter()
            pygame.display.flip()
            self.clock.tick(60)
        return True


# === Application Entry Point ===
def run_main_menu_loop() -> bool:
    """
    Initialize Pygame, create necessary dependencies, and start the main menu.
    When the menu loop finishes, Pygame is properly quit.
    """
    pygame.init()
    pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    music_manager = MusicManager()
    config = GameConfig(music_manager)
    main_menu = MainMenu(config)
    result = main_menu.run()
    pygame.quit()
    return result


# For backwards compatibility with existing code
def RunSettingsMenuLoop():
    """Run the settings menu screen."""
    pygame.init()
    pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    music_manager = MusicManager()
    config = GameConfig(music_manager)
    settings = SettingsMenu(config)
    result = settings.run()
    pygame.quit()
    return result


def RunMainMenuLoop():
    """Original function for backward compatibility."""
    return run_main_menu_loop()


def run_main_menu_loop_game(game):
    """Run the main menu screen with a game instance."""
    pygame.init()
    pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    music_manager = MusicManager()
    config = GameConfig(music_manager)
    main_menu = MainMenu(config)
    result = main_menu.run()
    pygame.quit()
    return result


if __name__ == '__main__':
    run_main_menu_loop()
