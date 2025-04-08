import pygame

class TextCache:
    """
    A utility class for caching rendered text surfaces to improve performance.
    """
    def __init__(self):
        # Cache structure: {(text, font, color, antialias): rendered_surface}
        self.cache = {}
        
    def render_text(self, font, text, color=(255, 255, 255), antialias=True):
        """
        Render text using a cached surface if available, or create and cache a new one.
        
        Args:
            font: pygame Font object
            text: String to render
            color: RGB color tuple (default: white)
            antialias: Whether to use antialiasing (default: True)
            
        Returns:
            Rendered text surface
        """
        # Create a unique key for this text rendering
        cache_key = (text, font, color, antialias)
        
        # Return cached surface if it exists
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Render new surface and cache it
        text_surface = font.render(text, antialias, color)
        self.cache[cache_key] = text_surface
        return text_surface
    
    def clear(self):
        """Clear the text cache"""
        self.cache.clear()
        
    def clear_for_text(self, text):
        """Remove all cached entries for a specific text string"""
        keys_to_remove = [key for key in self.cache.keys() if key[0] == text]
        for key in keys_to_remove:
            del self.cache[key]


# Create a global instance for easy access
global_text_cache = TextCache()
