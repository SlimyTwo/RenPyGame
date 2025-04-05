import pygame

from engine import WindowCreationHandler
from engine.WindowCreationHandler import DrawBackground
from buttons.StartButton import StartButtonDrawingAndHandling
from buttons.LoadGameButton import LoadGameButtonDrawingAndHandling
from buttons.SettingsButton import SettingsButtonDrawingAndHandling, GetUpdatedScreen
from buttons.QuitButton import QuitButtonDrawingAndHandling
from utility.CompleteProgramTermination import SystemTermination

def RunMainMenuLoop():
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

    SystemTermination()
