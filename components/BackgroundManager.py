import pygame
import os

class BackgroundManager:
    """
    Manages loading, scaling, and drawing of background images.
    """
    def __init__(self, background_path=None):
        """
        Initialize the background manager with an optional path.
        
        Args:
            background_path: Path to the background image file
        """
        self.background_path = background_path or os.path.join("assets", "images", "MainMenuBackground.png")
        self.original_bg = None
        self.background_image = None
        self.bg_pos = (0, 0)
        self.default_color = (40, 44, 52)
    
    def load_and_scale(self, screen):
        """
        Load and scale the background image to fit the screen.
        
        Args:
            screen: The pygame surface to draw on
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Get screen dimensions
        screen_width, screen_height = screen.get_size()
        
        try:
            # Load original image
            if os.path.exists(self.background_path):
                self.original_bg = pygame.image.load(self.background_path)
                
                # Get original image dimensions
                bg_width, bg_height = self.original_bg.get_size()
                
                # Calculate scaling factor to fill the screen
                width_ratio = screen_width / bg_width
                height_ratio = screen_height / bg_height
                scale_factor = max(width_ratio, height_ratio)
                
                # Calculate new dimensions
                new_width = int(bg_width * scale_factor)
                new_height = int(bg_height * scale_factor)
                
                # Scale the image with the calculated dimensions
                self.background_image = pygame.transform.scale(self.original_bg, (new_width, new_height))
                
                # Calculate position to center the image
                bg_x = (screen_width - new_width) // 2
                bg_y = (screen_height - new_height) // 2
                self.bg_pos = (bg_x, bg_y)
                
                return True
            else:
                print(f"Background image not found: {self.background_path}")
                self.background_image = None
                self.bg_pos = (0, 0)
                return False
        except Exception as e:
            print(f"Error loading background: {e}")
            self.background_image = None
            self.bg_pos = (0, 0)
            return False
    
    def draw(self, screen, color=None):
        """
        Draw the background on the screen.
        
        Args:
            screen: The pygame surface to draw on
            color: Optional override for default background color
        """
        background_color = color if color is not None else self.default_color
        
        if self.background_image:
            screen.fill(background_color)  # Fill with background color first
            screen.blit(self.background_image, self.bg_pos)  # Draw the centered image
        else:
            screen.fill(background_color)
    
    def set_background_path(self, path):
        """
        Change the background image path.
        
        Args:
            path: New path to background image
        """
        self.background_path = path
        # Reset image data
        self.original_bg = None
        self.background_image = None
        self.bg_pos = (0, 0)
    
    def set_default_color(self, color):
        """
        Set the default background color.
        
        Args:
            color: RGB tuple for background color
        """
        self.default_color = color
