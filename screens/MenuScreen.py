import pygame
import os
from buttons.ButtonClass import Button
from components.BackgroundManager import BackgroundManager
from utility.SettingsManager import SettingsManager
from utility.MenuStateManager import MenuStateManager

# Colors
BACKGROUND = (40, 44, 52)
TEXT_COLOR = (220, 220, 220)

class MenuScreen:
    """Base class for menu screens with common functionality"""
    
    def __init__(self, screen, music_manager):
        """Initialize with common menu elements"""
        self.screen = screen
        self.music_manager = music_manager
        
        # Get screen dimensions
        self.screen_width, self.screen_height = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Common managers
        self.settings_manager = SettingsManager()
        self.menu_state_manager = MenuStateManager()
        
        # Load fonts
        self.button_font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
        # Initialize background manager
        self.background_manager = BackgroundManager()
        self.background_manager.load_and_scale(self.screen)
        
        # Sound paths dictionary
        self.sound_paths = {
            "click": os.path.join("assets", "audio", "click.wav"),
            "hover": os.path.join("assets", "audio", "hover.wav"),
            "focus": os.path.join("assets", "audio", "focus.wav")
        }
        
        # Settings
        self.fps_display_enabled = self.settings_manager.get_setting("fps_display", False)
        
        # Buttons dictionary - to be populated by child classes
        self.buttons = {}
    
    def handle_events(self):
        """Process pygame events common to all menu screens"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Handle window resize
            elif event.type == pygame.VIDEORESIZE:
                Button.all_buttons.clear()
                self.background_manager.load_and_scale(self.screen)
                self.screen_width, self.screen_height = self.screen.get_size()
                self.recreate_buttons()
                
            # Handle button events
            Button.update_all(event)
                
            # Handle global keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_F11:
                    # F11 to toggle fullscreen
                    self.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    # ESC to go back
                    self.handle_back()
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode - to be implemented by child classes"""
        pass
    
    def recreate_buttons(self):
        """Recreate all buttons - to be implemented by child classes"""
        pass
    
    def handle_back(self):
        """Handle back button or ESC key - to be implemented by child classes"""
        pass
    
    def draw_instructions(self, text):
        """Draw instructions at the bottom of the screen"""
        instructions = self.small_font.render(text, True, TEXT_COLOR)
        self.screen.blit(instructions, (self.screen_width // 2 - instructions.get_width() // 2, self.screen_height - 40))
    
    def draw_fps(self):
        """Draw FPS counter if enabled"""
        if self.fps_display_enabled:
            fps = int(self.clock.get_fps())
            fps_text = self.small_font.render(f"FPS: {fps}", True, (255, 255, 0))
            self.screen.blit(fps_text, (10, 10))
    
    def draw_title(self, title_text):
        """Draw screen title"""
        title_surface = self.title_font.render(title_text, True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 80))
        self.screen.blit(title_surface, title_rect)
    
    def draw(self):
        """Draw common UI elements"""
        # Draw background
        self.background_manager.draw(self.screen, BACKGROUND)
        
        # Draw FPS counter if enabled
        self.draw_fps()
        
        # Draw all buttons
        for button in self.buttons.values():
            button.draw()
    
    def update(self):
        """Update game state and refresh display"""
        pygame.display.flip()
        self.clock.tick(60)
    
    def run(self):
        """Main loop for the menu"""
        # Create buttons
        self.recreate_buttons()
        
        # Main loop
        while self.running:
            self.handle_events()
            self.draw()
            self.update()
        
        # Clear buttons before returning
        Button.all_buttons.clear()
        return True
