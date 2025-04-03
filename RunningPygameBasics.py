import pygame
import sys

from StartButton import StartButtonFunctionality
from LoadGameButton import LoadGameButtonFunctionality
from SettingsButton import SettingsButtonFunctionality, GetUpdatedScreen
from QuitButton import QuitButtonFunctionality

def RunningPygameBasics():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Fantasy Falls")
    font = pygame.font.SysFont(None, 60)

    original_background = pygame.image.load("images\\background.png").convert()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen_width, screen_height = screen.get_size()
        scaled_background = pygame.transform.scale(original_background, (screen_width, screen_height))
        screen.blit(scaled_background, (0, 0))

        StartButtonFunctionality(screen, font)
        LoadGameButtonFunctionality(screen, font)
        SettingsButtonFunctionality(screen, font, original_background)
        QuitButtonFunctionality(screen, font)

        updated_screen = GetUpdatedScreen()
        if updated_screen:
            screen = updated_screen

        pygame.display.flip()

    pygame.quit()
    sys.exit()
