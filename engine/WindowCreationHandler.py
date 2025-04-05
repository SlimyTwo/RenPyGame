import pygame
import utility.GlobalVariables as gv  # gv = global variable alias

def InitializeWindowCreation():
    pygame.init()
    pygame.mixer.init()

    # Create and store shared screen + font
    gv.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Fantasy Falls")
    gv.font = pygame.font.SysFont(None, 60)

    # Load and store background image
    gv.background = pygame.image.load("assets/Images/MainMenuBackground.png").convert()