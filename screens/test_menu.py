# test_menu.py

import logging
import pygame

from screens.main_menu import MenuState, MenuManager
from ui.builders.button_builder import ButtonBuilder

# Constants from main_menu.py
TEXT_COLOR = (220, 220, 220)
HOVER_TEXT_COLOR = (255, 255, 0)


class TestMenuState(MenuState):
    """
    Test menu state implementation
    """
    def __init__(self, menu_manager: MenuManager):
        super().__init__(menu_manager)
        self.title = "Test Menu"

    def create_buttons(self) -> None:
        """Create test menu buttons"""
        base_menu = self.menu_manager.base_menu
        config = base_menu.config
        
        # Button geometry and spacing
        button_width = 250
        button_height = 50
        button_spacing = 20
        
        # Example test button 1
        test1_btn = (
            ButtonBuilder(self.screen, self.button_font, text="Test Feature 1")
            .set_size(button_width, button_height)
            .set_offsets(0, -50)
            .set_hover_text_color(HOVER_TEXT_COLOR)
            .set_tooltip("Try test feature 1")
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path, base_menu.focus_sound_path)
            .set_visible_background(False)
            .set_music_manager(config.music_manager)
            .build()
        )
        test1_btn.on_click = lambda: logging.info("Test feature 1 activated")
        test1_btn.set_focus(True)  # Initially focused
        
        # Example test button 2
        test2_btn = (
            ButtonBuilder(self.screen, self.button_font, text="Test Feature 2")
            .set_size(button_width, button_height)
            .set_offsets(0, -50 + button_height + button_spacing)
            .set_hover_text_color(HOVER_TEXT_COLOR)
            .set_tooltip("Try test feature 2")
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path, base_menu.focus_sound_path)
            .set_visible_background(False)
            .set_music_manager(config.music_manager)
            .build()
        )
        test2_btn.on_click = lambda: logging.info("Test feature 2 activated")
        
        # Back to Main Menu button
        back_btn = (
            ButtonBuilder(self.screen, self.button_font, text="Back to Main Menu")
            .set_size(button_width, button_height)
            .set_offsets(0, -50 + (button_height + button_spacing) * 2)
            .set_hover_text("⬅ Main Menu")
            .set_hover_text_color(HOVER_TEXT_COLOR)
            .set_tooltip("Return to main menu")
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path, base_menu.focus_sound_path)
            .set_visible_background(False)
            .set_music_manager(config.music_manager)
            .build()
        )
        back_btn.on_click = lambda: self.menu_manager.transition_to("main")
        
        self.buttons = [test1_btn, test2_btn, back_btn]

    def handle_events(self, event: pygame.event.Event) -> bool:
        """Handle events for this state"""
        for button in self.buttons:
            button.handle_event(event)
        return False
            
    def draw(self) -> None:
        """Draw the test menu state"""
        # Draw title
        title_text = self.title_font.render(self.title, True, TEXT_COLOR)
        self.screen.blit(
            title_text,
            (self.screen_width // 2 - title_text.get_width() // 2, 100)
        )
        
        # Draw all buttons
        for button in self.buttons:
            button.draw()
