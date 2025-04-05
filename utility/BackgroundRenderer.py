import pygame
import utility.GlobalVariables as gv  # gv = global variable alias

def DrawMainMenuBackground():
    screen_width, screen_height = gv.screen.get_size()
    scaled_background = pygame.transform.scale(gv.background, (screen_width, screen_height))
    gv.screen.blit(scaled_background, (0, 0))
