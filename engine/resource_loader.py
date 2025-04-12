# """Resource manager for game assets."""
# import pygame
#
# class ResourceManager:
#     def __init__(self):
#         self.images = {}
#         self.fonts = {}
#         self.sounds = {}
#
#     def load_image(self, name, path, convert=True):
#         """Load an image and store it with the given name."""
#         try:
#             if convert:
#                 image = pygame.image.load(path).convert()
#             else:
#                 image = pygame.image.load(path).convert_alpha()
#             self.images[name] = image
#             return image
#         except pygame.error as e:
#             print(f"Error loading image {path}: {e}")
#             return None
#
#     def get_image(self, name):
#         """Get a previously loaded image."""
#         return self.images.get(name)
#
#     def load_font(self, name, font_name, size):
#         """Load a font and store it with the given name."""
#         try:
#             font = pygame.font.SysFont(font_name, size)
#             self.fonts[name] = font
#             return font
#         except pygame.error as e:
#             print(f"Error loading font {font_name}: {e}")
#             return None
#
#     def get_font(self, name):
#         """Get a previously loaded font."""
#         return self.fonts.get(name)
