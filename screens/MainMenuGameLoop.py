import pygame
import os
from buttons.ButtonClass import Button
from buttons.ButtonCreator import create_button, create_slider
from utility.MusicManager import MusicManager

# Colors
BACKGROUND = (40, 44, 52)
TEXT_COLOR = (220, 220, 220)
HOVER_COLOR = (100, 100, 150, 180)
HOVER_TEXT_COLOR = (255, 255, 0)

# Sound files paths
click_sound_path = os.path.join("assets", "audio", "click.wav")
hover_sound_path = os.path.join("assets", "audio", "hover.wav")
focus_sound_path = os.path.join("assets", "audio", "focus.wav")

# Music file path
background_music_path = os.path.join("assets", "audio", "background_music.mp3")

# Initialize music manager
music_manager = MusicManager()

# Global settings - now loaded from settings manager
fps_display_enabled = music_manager.settings_manager.get_setting("fps_display", False)
music_enabled = music_manager.settings_manager.get_setting("music_enabled", True)


class MenuBase:
    """Base class for menu screens with common functionality."""

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_width, self.screen_height = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.running = True

        # Fonts
        self.button_font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)

        # Background
        self.original_bg = None
        self.background_image = None
        self.bg_pos = (0, 0)

        # Sound effects
        self.sound_path = click_sound_path if os.path.exists(click_sound_path) else None
        self.hover_sound = hover_sound_path if os.path.exists(hover_sound_path) else None

        # Fullscreen state
        self.is_fullscreen = self.screen.get_flags() & pygame.FULLSCREEN

    def load_background_image(self):
        """Load and scale background image to fit screen."""
        # Update screen dimensions
        self.screen_width, self.screen_height = self.screen.get_size()

        try:
            bg_path = os.path.join("assets", "images", "MainMenuBackground.png")

            # Load original image only once
            if self.original_bg is None and os.path.exists(bg_path):
                self.original_bg = pygame.image.load(bg_path)

            if self.original_bg:
                # Get original image dimensions
                bg_width, bg_height = self.original_bg.get_size()

                # Calculate scaling factor to fill the screen
                width_ratio = self.screen_width / bg_width
                height_ratio = self.screen_height / bg_height
                scale_factor = max(width_ratio, height_ratio)

                # Calculate new dimensions
                new_width = int(bg_width * scale_factor)
                new_height = int(bg_height * scale_factor)

                # Scale the image with the calculated dimensions
                self.background_image = pygame.transform.scale(self.original_bg, (new_width, new_height))

                # Calculate position to center the image
                bg_x = (self.screen_width - new_width) // 2
                bg_y = (self.screen_height - new_height) // 2

                # Store position with the image
                self.bg_pos = (bg_x, bg_y)
            else:
                self.background_image = None
                self.bg_pos = (0, 0)
        except Exception as e:
            print(f"Error loading background: {e}")
            self.background_image = None
            self.bg_pos = (0, 0)

    def draw_background(self):
        """Draw the background on the screen."""
        if self.background_image:
            self.screen.fill(BACKGROUND)
            self.screen.blit(self.background_image, self.bg_pos)
        else:
            self.screen.fill(BACKGROUND)

    def draw_fps_counter(self):
        """Draw FPS counter if enabled."""
        global fps_display_enabled
        if fps_display_enabled:
            fps = int(self.clock.get_fps())
            fps_text = self.small_font.render(f"FPS: {fps}", True, (255, 255, 0))
            self.screen.blit(fps_text, (10, 10))

    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        self.is_fullscreen = not self.is_fullscreen

        # Save fullscreen setting
        music_manager.settings_manager.set_setting("fullscreen", self.is_fullscreen)

        # Toggle fullscreen mode
        if self.is_fullscreen:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

        # Reload background and recreate buttons
        Button.all_buttons.clear()
        self.load_background_image()
        self.create_buttons()

    def create_buttons(self):
        """Create and position buttons - to be implemented by subclasses."""
        pass

    def handle_common_events(self, event):
        """Handle common events like quit and fullscreen toggle."""
        if event.type == pygame.QUIT:
            self.running = False
            return True

        # Handle window resize
        elif event.type == pygame.VIDEORESIZE:
            Button.all_buttons.clear()
            self.load_background_image()
            self.create_buttons()
            return True

        # Keyboard shortcuts
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.running = False
                return True
            elif event.key == pygame.K_F11:
                self.toggle_fullscreen()
                return True

        return False

    def run(self):
        """Main loop for the menu - to be implemented by subclasses."""
        pass


class SettingsMenu(MenuBase):
    """Settings menu screen."""

    def __init__(self):
        super().__init__()

        # Initialize button variables
        self.back_btn = None
        self.fullscreen_btn = None
        self.fps_btn = None
        self.music_toggle_btn = None
        self.volume_slider = None
        self.master_volume_slider = None

        # Initial setup
        self.load_background_image()
        self.create_buttons()

    def create_buttons(self):
        """Create and position all buttons for the settings menu."""
        global fps_display_enabled, music_enabled

        # Back button in top left
        self.back_btn = create_button(
            self.screen, self.button_font, "← Back",
            width=120, height=40,
            x_offset=-self.screen_width // 2 + 80, y_offset=-self.screen_height // 2 + 40,
            hover_text="← Return",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Return to main menu",
            sound_path=self.sound_path,
            hover_sound_path=self.hover_sound,
            visible_background=True,
            music_manager=music_manager
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
            sound_path=self.sound_path,
            hover_sound_path=self.hover_sound,
            toggle_mode=True,
            toggled=self.is_fullscreen,
            music_manager=music_manager
        )

        # FPS counter toggle button
        fps_text = "FPS Counter: ON" if fps_display_enabled else "FPS Counter: OFF"
        self.fps_btn = create_button(
            self.screen, self.button_font, fps_text,
            width=250, height=50,
            y_offset=50,
            hover_text="Toggle FPS Display",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Show or hide frames per second counter",
            sound_path=self.sound_path,
            hover_sound_path=self.hover_sound,
            toggle_mode=True,
            toggled=fps_display_enabled,
            music_manager=music_manager
        )

        # Music toggle button
        music_text = "Music: ON" if music_enabled else "Music: OFF"
        self.music_toggle_btn = create_button(
            self.screen, self.button_font, music_text,
            width=250, height=50,
            y_offset=120,
            hover_text="Toggle Background Music",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Turn background music on or off",
            sound_path=self.sound_path,
            hover_sound_path=self.hover_sound,
            toggle_mode=True,
            toggled=music_enabled,
            music_manager=music_manager
        )

        # Master volume slider
        self.master_volume_slider = create_slider(
            self.screen, self.button_font,
            width=250, height=30,
            y_offset=200,
            min_value=0, max_value=100,
            current_value=int(music_manager.get_master_volume() * 100),
            label="Master Volume",
            sound_path=self.sound_path,
            hover_sound_path=self.hover_sound,
            music_manager=music_manager
        )

        # Music volume slider
        self.volume_slider = create_slider(
            self.screen, self.button_font,
            width=250, height=30,
            y_offset=280,
            min_value=0, max_value=100,
            current_value=int(music_manager.get_volume() * 100),
            label="Music Volume",
            sound_path=self.sound_path,
            hover_sound_path=self.hover_sound,
            music_manager=music_manager
        )

        # Button handlers
        self.back_btn.on_click = self.handle_back
        self.fullscreen_btn.on_click = self.handle_fullscreen_toggle
        self.fps_btn.on_click = self.handle_fps_toggle
        self.music_toggle_btn.on_click = self.handle_music_toggle
        self.volume_slider.on_value_change = self.handle_volume_change
        self.master_volume_slider.on_value_change = self.handle_master_volume_change

        # Set focus on back button initially
        self.back_btn.set_focus(True)

    def handle_back(self):
        """Return to main menu."""
        self.running = False
        return True

    def handle_fullscreen_toggle(self):
        """Toggle fullscreen mode."""
        self.toggle_fullscreen()

        # Update button text
        fullscreen_text = "Fullscreen: ON" if self.is_fullscreen else "Fullscreen: OFF"
        self.fullscreen_btn.set_text(fullscreen_text)
        return True

    def handle_fps_toggle(self):
        """Toggle FPS counter display."""
        global fps_display_enabled
        fps_display_enabled = not fps_display_enabled

        # Save fps display setting
        music_manager.settings_manager.set_setting("fps_display", fps_display_enabled)

        # Update button text
        fps_text = "FPS Counter: ON" if fps_display_enabled else "FPS Counter: OFF"
        self.fps_btn.set_text(fps_text)
        return True

    def handle_music_toggle(self):
        """Toggle background music."""
        global music_enabled
        music_enabled = not music_enabled

        # Update music_enabled in music manager
        music_manager.set_music_enabled(music_enabled)

        # Update button text
        music_text = "Music: ON" if music_enabled else "Music: OFF"
        self.music_toggle_btn.set_text(music_text)

        # Start or stop music
        if music_enabled:
            if not music_manager.is_playing():
                music_manager.play_music(background_music_path)
        else:
            music_manager.stop_music()

        return True

    def handle_volume_change(self, value):
        """Update music volume."""
        volume = value / 100.0  # Convert to 0.0-1.0 range
        music_manager.set_volume(volume)
        return True

    def handle_master_volume_change(self, value):
        """Update master volume."""
        volume = value / 100.0  # Convert to 0.0-1.0 range
        music_manager.set_master_volume(volume)
        return True

    def run(self):
        """Run the settings menu loop."""
        self.running = True

        while self.running:
            # Draw background
            self.draw_background()

            # Draw title
            title_text = self.title_font.render("Settings", True, TEXT_COLOR)
            title_rect = title_text.get_rect(center=(self.screen_width // 2, 80))
            self.screen.blit(title_text, title_rect)

            # Process events
            for event in pygame.event.get():
                if self.handle_common_events(event):
                    continue

                # Handle button events
                Button.update_all(event)

                # Handle slider events directly
                if self.volume_slider:
                    self.volume_slider.handle_event(event)
                if self.master_volume_slider:
                    self.master_volume_slider.handle_event(event)

                # Additional keyboard shortcuts
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            # Draw all buttons and sliders
            self.back_btn.draw()
            self.fullscreen_btn.draw()
            self.fps_btn.draw()
            self.music_toggle_btn.draw()
            self.master_volume_slider.draw()
            self.volume_slider.draw()

            # Draw instructions
            instructions = self.small_font.render(
                "Press TAB to navigate, ENTER to select, ESC to go back, F11 for fullscreen",
                True, TEXT_COLOR
            )
            self.screen.blit(instructions,
                             (self.screen_width // 2 - instructions.get_width() // 2, self.screen_height - 40))

            # Draw FPS counter if enabled
            self.draw_fps_counter()

            pygame.display.flip()
            self.clock.tick(60)

        # Clear buttons before returning
        Button.all_buttons.clear()
        return True


class MainMenu(MenuBase):
    """Main menu screen."""

    def __init__(self):
        super().__init__()

        # Button dimensions
        self.button_width = 250
        self.button_height = 50
        self.button_spacing = 20

        # Initialize button variables
        self.start_game_btn = None
        self.load_game_btn = None
        self.settings_btn = None
        self.quit_btn = None

        # Apply fullscreen setting from saved settings
        is_fullscreen = music_manager.settings_manager.get_setting("fullscreen", False)
        if is_fullscreen and not (self.screen.get_flags() & pygame.FULLSCREEN):
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        elif not is_fullscreen and (self.screen.get_flags() & pygame.FULLSCREEN):
            pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

        # Update fullscreen state after potential change
        self.is_fullscreen = self.screen.get_flags() & pygame.FULLSCREEN

        # Start background music if enabled
        if music_enabled and os.path.exists(background_music_path):
            music_manager.play_music(background_music_path)

        # Initial setup
        self.load_background_image()
        self.create_buttons()

    def create_buttons(self):
        """Create and position all buttons for the main menu."""
        # Start Game button
        self.start_game_btn = create_button(
            self.screen, self.button_font, "Start Game",
            width=self.button_width, height=self.button_height,
            y_offset=-100,
            hover_text="▶ Start Game ▶",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Start a new game",
            sound_path=self.sound_path,
            hover_sound_path=self.hover_sound,
            visible_background=False,
            debug_hitbox=False,  # Changed from True to False
            music_manager=music_manager
        )

        # Load Game button (greyed out)
        self.load_game_btn = create_button(
            self.screen, self.button_font, "Load Game",
            width=self.button_width, height=self.button_height,
            y_offset=-100 + self.button_height + self.button_spacing,
            hover_text="Load Game (Unavailable)",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Load a saved game",
            visible_background=False,
            debug_hitbox=False,  # Changed from True to False
            disabled=True,
            music_manager=music_manager
        )

        # Settings button
        self.settings_btn = create_button(
            self.screen, self.button_font, "Settings",
            width=self.button_width, height=self.button_height,
            y_offset=-100 + (self.button_height + self.button_spacing) * 2,
            hover_text="⚙ Settings ⚙",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Game settings",
            sound_path=self.sound_path,
            hover_sound_path=self.hover_sound,
            visible_background=False,
            debug_hitbox=False,  # Changed from True to False
            music_manager=music_manager
        )

        # Quit button
        self.quit_btn = create_button(
            self.screen, self.button_font, "Quit",
            width=self.button_width, height=self.button_height,
            y_offset=-100 + (self.button_height + self.button_spacing) * 3,
            hover_text="✖ Exit Game ✖",
            hover_text_color=(255, 100, 100),
            tooltip="Exit the game",
            sound_path=self.sound_path,
            hover_sound_path=self.hover_sound,
            visible_background=False,
            debug_hitbox=False,  # Changed from True to False
            music_manager=music_manager
        )

        # Button handlers
        self.start_game_btn.on_click = self.handle_start_game
        self.settings_btn.on_click = self.handle_settings
        self.quit_btn.on_click = self.handle_quit

        # Ensure the first button has focus initially for keyboard navigation
        self.start_game_btn.set_focus(True)

    def handle_start_game(self):
        """Start a new game."""
        # Start new game logic would go here
        return True

    def handle_settings(self):
        """Open settings menu."""
        # Clear current buttons
        Button.all_buttons.clear()

        # Run settings menu
        settings_menu = SettingsMenu()
        settings_menu.run()

        # Recreate main menu buttons when returning
        self.load_background_image()
        self.create_buttons()
        return True

    def handle_quit(self):
        """Exit the game."""
        self.running = False
        return True

    def run(self):
        """Run the main menu loop."""
        self.running = True

        while self.running:
            # Draw background
            self.draw_background()

            # Process events
            for event in pygame.event.get():
                if self.handle_common_events(event):
                    continue

                # Handle button events
                Button.update_all(event)

            # Draw all buttons
            self.start_game_btn.draw()
            self.load_game_btn.draw()
            self.settings_btn.draw()
            self.quit_btn.draw()

            # Draw instructions
            instructions = self.small_font.render(
                "Press TAB to navigate, ENTER to select, Q to quit, F11 for fullscreen",
                True, TEXT_COLOR
            )
            self.screen.blit(instructions,
                             (self.screen_width // 2 - instructions.get_width() // 2, self.screen_height - 40))

            # Draw FPS counter if enabled
            self.draw_fps_counter()

            pygame.display.flip()
            self.clock.tick(60)


def RunSettingsMenuLoop():
    """Run the settings menu screen."""
    settings = SettingsMenu()
    return settings.run()


def RunMainMenuLoop():
    """Original function for backward compatibility."""
    main_menu = MainMenu()
    return main_menu.run()


def run_main_menu_loop(game):
    """Run the main menu screen with a game instance."""
    # Initialize the menu using the existing MainMenu class
    main_menu = MainMenu()
    # Run the menu loop
    return main_menu.run()

