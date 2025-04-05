import pygame

# Global variables
screen = None
font = None

def InitializeWindowCreation():
    global screen, font
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Fantasy Falls")
    font = pygame.font.SysFont(None, 60)
