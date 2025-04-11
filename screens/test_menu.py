# test_menu.py

import logging
import pygame

from screens.menu_system import AbstractMenuBase, MenuManager  # Updated import
from ui.builders.button_builder import ButtonBuilder


# Constants from menu_system
TEXT_COLOR = (220, 220, 220)
HOVER_TEXT_COLOR = (255, 255, 0)


class TestAbstractMenuBase(AbstractMenuBase):
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
        
        # Button spacing
        button_spacing = 20
        
        # Default button using the preset
        default_btn = (
            ButtonBuilder.default_button(self.screen, self.button_font, text="Default Button Example")
            .set_offsets(0, -50)
            .set_tooltip("This is a button using the default preset")
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path)
            .set_music_manager(config.music_manager)
            .build()
        )
        default_btn.on_click = lambda: logging.info("Default button clicked!")
        default_btn.set_focus(True)  # Initially focused
        
        # Back to Main Menu button
        back_btn = (
            ButtonBuilder(self.screen, self.button_font, text="Back to Main Menu")
            .set_size(250, 50)
            .set_offsets(0, -50 + 50 + button_spacing)
            .set_hover_text("⬅ Main Menu")
            .set_hover_text_color(HOVER_TEXT_COLOR)
            .set_tooltip("Return to main menu")
            .set_sounds(base_menu.click_sound_path, base_menu.hover_sound_path)
            .set_is_background_visible(False)
            .set_music_manager(config.music_manager)
            .build()
        )
        back_btn.on_click = lambda: self.menu_manager.transition_to("main")
        
        self.buttons = [default_btn, back_btn]

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
