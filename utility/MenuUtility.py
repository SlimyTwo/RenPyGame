import pygame
import os
from components.BackgroundManager import BackgroundManager

# Create a default background manager for backward compatibility
_default_bg_manager = BackgroundManager()

def load_background_image(screen, bg_path=None):
    """
    Load and scale background image to fit the screen.
    
    Args:
        screen: The pygame surface to draw on
        bg_path: Optional custom path to background image. If None, uses default path.
    
    Returns:
        tuple: (background_image, bg_pos, original_bg)
    """
    # Update the background path if provided
    if bg_path is not None:
        _default_bg_manager.set_background_path(bg_path)
    
    # Load and scale the background
    _default_bg_manager.load_and_scale(screen)
    
    # Return the values in the same format as before for compatibility
    return _default_bg_manager.background_image, _default_bg_manager.bg_pos, _default_bg_manager.original_bg

def draw_background(screen, background_image, bg_pos, default_color=(40, 44, 52)):
    """
    Draw the background on the screen.
    
    Args:
        screen: The pygame surface to draw on
        background_image: The background image surface
        bg_pos: Position tuple for the background
        default_color: The fallback color if image is None
    """
    if background_image:
        screen.fill(default_color)  # Fill with background color first
        screen.blit(background_image, bg_pos)  # Draw the centered image
    else:
        screen.fill(default_color)
