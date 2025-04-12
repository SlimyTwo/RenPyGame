# settings_menu.py

import os
import pygame

from screens.menu_system import AbstractMenuBase, MenuManager  # Updated import
from ui.builders.button_builder import ButtonBuilder

from config import BACKGROUND_MUSIC_PATH  # make sure this is at the top

# Constants from menu_system
TEXT_COLOR = (220, 220, 220)
HOVER_TEXT_COLOR = (255, 255, 0)


class SettingsAbstractMenuBase(AbstractMenuBase):
    """
    Settings menu state implementation
    """
    def __init__(self, menu_manager: MenuManager):
        super().__init__(menu_manager)
        self.title = "Settings Menu"

    def create_buttons(self) -> None:
        """Create settings menu buttons"""
        base_menu = self.menu_manager.base_menu
        config = base_menu.config
        
        # Button geometry and spacing
        button_width = 250
        button_height = 50
        button_spacing = 20
        
        # Toggle music button
        music_text = "Disable Music" if config.music_enabled else "Enable Music"
        music_btn = (
            ButtonBuilder(self.screen, self.button_font, text=music_text)
            .set_size(button_width, button_height)
            .set_offsets(0, -50)
            .set_hover_text_color(HOVER_TEXT_COLOR)
            .set_tooltip("Toggle background music")
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path)  # Removed focus_sound_path
            .set_is_background_visible(False)
            .set_music_manager(config.music_manager)
            .build()
        )
        music_btn.on_click = self.toggle_music

        # Toggle FPS display button
        fps_text = "Hide FPS" if config.fps_display_enabled else "Show FPS"
        fps_btn = (
            ButtonBuilder(self.screen, self.button_font, text=fps_text)
            .set_size(button_width, button_height)
            .set_offsets(0, -50 + button_height + button_spacing)
            .set_hover_text_color(HOVER_TEXT_COLOR)
            .set_tooltip("Toggle FPS counter")
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path)  # Removed focus_sound_path
            .set_is_background_visible(False)
            .set_music_manager(config.music_manager)
            .build()
        )
        fps_btn.on_click = self.toggle_fps
        
        # Back to Main Menu button
        back_btn = (
            ButtonBuilder(self.screen, self.button_font, text="Back to Main Menu")
            .set_size(button_width, button_height)
            .set_offsets(0, -50 + (button_height + button_spacing) * 2)
            .set_hover_text("⬅ Main Menu")
            .set_hover_text_color(HOVER_TEXT_COLOR)
            .set_tooltip("Return to main menu")
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path)  # Removed focus_sound_path
            .set_is_background_visible(False)
            .set_music_manager(config.music_manager)
            .build()
        )
        back_btn.on_click = lambda: self.menu_manager.transition_to("main")
        
        self.buttons = [music_btn, fps_btn, back_btn]

    def handle_events(self, event: pygame.event.Event) -> bool:
        """Handle events for this state"""
        for button in self.buttons:
            button.handle_event(event)
        return False
            
    def draw(self) -> None:
        """Draw the settings menu state"""
        # Draw title
        title_text = self.title_font.render(self.title, True, TEXT_COLOR)
        self.screen.blit(
            title_text,
            (self.screen_width // 2 - title_text.get_width() // 2, 100)
        )
        
        # Draw all buttons
        for button in self.buttons:
            button.draw()

    def toggle_music(self) -> bool:
        """Toggle music on/off"""
        config = self.menu_manager.base_menu.config
        music_manager = config.music_manager

        # Toggle the setting
        config.music_enabled = not config.music_enabled
        music_manager.settings_manager.set_setting("music_enabled", config.music_enabled)

        if config.music_enabled:
            # Use current track if available, otherwise fall back to default menu music
            music_path = music_manager.current_music or BACKGROUND_MUSIC_PATH
            if os.path.exists(music_path):
                music_manager.play_music(music_path)
            else:
                print(f"Music file not found: {music_path}")
        else:
            music_manager.stop_music()

        # Update button label
        self.buttons[0].text = "Disable Music" if config.music_enabled else "Enable Music"
        return True

    def toggle_fps(self) -> bool:
        """Toggle FPS display on/off"""
        config = self.menu_manager.base_menu.config
        config.fps_display_enabled = not config.fps_display_enabled
        config.music_manager.settings_manager.set_setting("fps_display", config.fps_display_enabled)
        
        # Update button text
        self.buttons[1].text = "Hide FPS" if config.fps_display_enabled else "Show FPS"
        return True

