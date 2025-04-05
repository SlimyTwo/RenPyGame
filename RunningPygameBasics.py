import pygame
import sys

import WindowCreationHandler
from WindowCreationHandler import InitializeWindowCreation
from StartButton import StartButtonFunctionality
from LoadGameButton import LoadGameButtonFunctionality
from SettingsButton import SettingsButtonFunctionality, GetUpdatedScreen
from QuitButton import QuitButtonFunctionality

def RunningPygameBasics():
    InitializeWindowCreation()

    original_background = pygame.image.load("images\\MainMenuBackground.png").convert()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen_width, screen_height = WindowCreationHandler.screen.get_size()
        scaled_background = pygame.transform.scale(original_background, (screen_width, screen_height))
        WindowCreationHandler.screen.blit(scaled_background, (0, 0))

        StartButtonFunctionality(WindowCreationHandler.screen, WindowCreationHandler.font)
        LoadGameButtonFunctionality(WindowCreationHandler.screen, WindowCreationHandler.font)
        SettingsButtonFunctionality(WindowCreationHandler.screen, WindowCreationHandler.font, original_background)
        QuitButtonFunctionality(WindowCreationHandler.screen, WindowCreationHandler.font)

        updated_screen = GetUpdatedScreen()
        if updated_screen:
            WindowCreationHandler.screen = updated_screen

        pygame.display.flip()

    pygame.quit()
    sys.exit()
