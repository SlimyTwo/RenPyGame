import pygame
import os
from buttons.ButtonClass import Button

class MenuButtonFactory:
    """
    Factory class for creating menu buttons
    """
    def __init__(self, screen, font, sound_paths, music_manager, font_size=36, padding=10):
        self.screen = screen
        self.font = font if font else pygame.font.Font(None, font_size)
        self.padding = padding
        self.sound_paths = sound_paths
        self.music_manager = music_manager
        
    def create_button(self, text, position, callback, color=(200, 200, 200), hover_color=(150, 150, 150)):
        """
        Create a menu button with the given parameters
        
        Args:
            text: Text to display on the button
            position: (x, y) position for the button
            callback: Function to call when button is clicked
            color: Normal button color
            hover_color: Color when hovered
            
        Returns:
            Button object with render and check_click methods
        """
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        button_rect = pygame.Rect(
            position[0], 
            position[1],
            text_rect.width + self.padding * 2,
            text_rect.height + self.padding * 2
        )
        
        return Button(button_rect, text, self.font, callback, color, hover_color, 
                     self.sound_paths.get("click"), self.sound_paths.get("hover"))
    
    def create_main_menu_buttons(self, state):
        """Create all buttons for main menu"""
        buttons = {}
        
        # Calculate center for button placement
        screen_width, screen_height = self.screen.get_size()
        center_x = screen_width // 2
        start_y = screen_height // 3
        button_spacing = 70
        
        # Create the main menu buttons
        buttons["start_game"] = self.create_button("Start Game", (center_x - 100, start_y), lambda: None)
        buttons["settings"] = self.create_button("Settings", (center_x - 100, start_y + button_spacing), lambda: None)
        buttons["quit"] = self.create_button("Quit Game", (center_x - 100, start_y + button_spacing * 2), lambda: None)
        
        return buttons
    
    def create_settings_menu_buttons(self, state):
        """Create all buttons for settings menu"""
        buttons = {}
        
        # Calculate center for button placement
        screen_width, screen_height = self.screen.get_size()
        center_x = screen_width // 2
        start_y = screen_height // 3
        button_spacing = 70
        
        # Create settings buttons with current state
        fullscreen_text = f"Fullscreen: {'ON' if pygame.display.get_surface().get_flags() & pygame.FULLSCREEN else 'OFF'}"
        fps_text = f"FPS Counter: {'ON' if state.get('fps_display', False) else 'OFF'}"
        music_text = f"Music: {'ON' if state.get('music_enabled', True) else 'OFF'}"
        
        buttons["fullscreen"] = self.create_button(fullscreen_text, (center_x - 100, start_y), lambda: None)
        buttons["fps"] = self.create_button(fps_text, (center_x - 100, start_y + button_spacing), lambda: None)
        buttons["music_toggle"] = self.create_button(music_text, (center_x - 100, start_y + button_spacing * 2), lambda: None)
        
        # Add volume controls (assuming these are slider buttons)
        buttons["master_volume"] = self.create_button(f"Master Volume: {int(state.get('master_volume', 100))}%", 
                                             (center_x - 100, start_y + button_spacing * 3), lambda: None)
        buttons["music_volume"] = self.create_button(f"Music Volume: {int(state.get('music_volume', 100))}%", 
                                            (center_x - 100, start_y + button_spacing * 4), lambda: None)
        
        # Back button
        buttons["back"] = self.create_button("Back", (center_x - 100, start_y + button_spacing * 5), lambda: None)
        
        return buttons
