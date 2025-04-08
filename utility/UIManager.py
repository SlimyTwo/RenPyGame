import pygame
from buttons.ButtonClass import Button
from components.BackgroundManager import BackgroundManager
from utility.SettingsManager import SettingsManager

class UIManager:
    """Manages UI screens, transitions, and global UI state"""
    
    def __init__(self):
        """Initialize the UI Manager"""
        self.screen = pygame.display.get_surface()
        self.settings_manager = SettingsManager()
        self.background_manager = BackgroundManager()
        
        # Track current screen/state
        self.current_screen = None
        self.previous_screen = None
        
        # Animation/transition variables
        self.in_transition = False
        self.transition_progress = 0
        self.transition_type = None  # fade, slide, etc.
        
        # Apply saved settings on init
        self._apply_saved_settings()
    
    def _apply_saved_settings(self):
        """Apply saved settings like resolution and fullscreen mode"""
        # Apply fullscreen setting
        is_fullscreen = self.settings_manager.get_setting("fullscreen", False)
        current_is_fullscreen = bool(self.screen.get_flags() & pygame.FULLSCREEN)
        
        if is_fullscreen != current_is_fullscreen:
            if is_fullscreen:
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    
    def get_fps_display_enabled(self):
        """Get whether FPS display is enabled from settings"""
        return self.settings_manager.get_setting("fps_display", False)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode and save the setting"""
        current_is_fullscreen = bool(self.screen.get_flags() & pygame.FULLSCREEN)
        is_fullscreen = not current_is_fullscreen
        
        # Save setting
        self.settings_manager.set_setting("fullscreen", is_fullscreen)
        
        # Apply setting
        if is_fullscreen:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        
        # Update the screen reference
        self.screen = pygame.display.get_surface()
        
        # Reload background to match new dimensions
        self.background_manager.load_and_scale(self.screen)
        
        return is_fullscreen
    
    def set_fps_display(self, enabled):
        """Set whether FPS display is enabled"""
        self.settings_manager.set_setting("fps_display", enabled)
    
    def transition_to(self, new_screen, transition_type="fade"):
        """Begin transition to a new screen"""
        self.previous_screen = self.current_screen
        self.current_screen = new_screen
        self.transition_type = transition_type
        self.in_transition = True
        self.transition_progress = 0
        
        # Clear all buttons when transitioning screens
        Button.all_buttons.clear()
    
    def draw_background(self, color=(40, 44, 52)):
        """Draw the background using the background manager"""
        self.background_manager.draw(self.screen, color)
    
    def update_transition(self):
        """Update transition animation if in progress"""
        if not self.in_transition:
            return False
            
        # Simple implementation - increase progress
        self.transition_progress += 0.05
        
        if self.transition_progress >= 1.0:
            self.in_transition = False
            self.transition_progress = 0
            return True
        
        # Draw transition effect based on type
        if self.transition_type == "fade":
            # Create a semi-transparent overlay
            alpha = int(255 * self.transition_progress)
            overlay = pygame.Surface(self.screen.get_size())
            overlay.fill((0, 0, 0))
            overlay.set_alpha(alpha)
            self.screen.blit(overlay, (0, 0))
        
        return False
