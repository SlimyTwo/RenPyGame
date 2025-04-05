import pygame
import sys

import WindowCreationHandler
from WindowCreationHandler import InitializeWindowCreation, DrawBackground
from StartButton import StartButtonFunctionality
from LoadGameButton import LoadGameButtonFunctionality
from SettingsButton import SettingsButtonFunctionality, GetUpdatedScreen
from QuitButton import QuitButtonFunctionality

def RunningPygameBasics():
    InitializeWindowCreation()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        DrawBackground()

        StartButtonFunctionality(WindowCreationHandler.screen, WindowCreationHandler.font)
        LoadGameButtonFunctionality(WindowCreationHandler.screen, WindowCreationHandler.font)
        SettingsButtonFunctionality(WindowCreationHandler.screen, WindowCreationHandler.font, WindowCreationHandler.background)
        QuitButtonFunctionality(WindowCreationHandler.screen, WindowCreationHandler.font)

        updated_screen = GetUpdatedScreen()
        if updated_screen:
            WindowCreationHandler.screen = updated_screen

        pygame.display.flip()

    pygame.quit()
    sys.exit()
