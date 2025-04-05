import pygame
import sys

import WindowCreationHandler
from WindowCreationHandler import InitializeWindowCreation, DrawBackground
from StartButton import StartButtonDrawingAndHandling
from LoadGameButton import LoadGameButtonDrawingAndHandling
from SettingsButton import SettingsButtonDrawingAndHandling, GetUpdatedScreen
from QuitButton import QuitButtonDrawingAndHandling

def RunningPygameBasics():
    InitializeWindowCreation()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        DrawBackground()

        StartButtonDrawingAndHandling(WindowCreationHandler.screen, WindowCreationHandler.font)
        LoadGameButtonDrawingAndHandling(WindowCreationHandler.screen, WindowCreationHandler.font)
        SettingsButtonDrawingAndHandling(WindowCreationHandler.screen, WindowCreationHandler.font, WindowCreationHandler.background)
        QuitButtonDrawingAndHandling(WindowCreationHandler.screen, WindowCreationHandler.font)

        updated_screen = GetUpdatedScreen()
        if updated_screen:
            WindowCreationHandler.screen = updated_screen

        pygame.display.flip()

    pygame.quit()
    sys.exit()
