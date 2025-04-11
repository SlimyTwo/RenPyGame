# main_menu.py

import logging
import pygame

from screens.menu_system import AbstractMenuBase, MenuManager
from ui.builders.button_builder import ButtonBuilder

# Constants from menu_system
TEXT_COLOR = (220, 220, 220)
HOVER_TEXT_COLOR = (255, 255, 0)


class MainAbstractMenuBase(AbstractMenuBase):
    """
    Main menu state implementation
    """
    def __init__(self, menu_manager: MenuManager):
        super().__init__(menu_manager)
        self.title = "Main Menu"

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
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path)
            .set_is_background_visible(False)
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
            .set_is_background_visible(False)
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
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path)
            .set_is_background_visible(False)
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
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path)
            .set_is_background_visible(False)
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
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path)
            .set_is_background_visible(False)
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
