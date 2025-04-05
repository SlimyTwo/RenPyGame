import pygame
import utility.GlobalVariables as gv

from engine import DrawMainMenuBackground
from buttons.StartButton import StartButtonDrawingAndHandling
from buttons.LoadGameButton import LoadGameButtonDrawingAndHandling
from buttons.SettingsButton import SettingsButtonDrawingAndHandling, GetUpdatedScreen
from buttons.QuitButton import QuitButtonDrawingAndHandling
from utility.CompleteProgramTermination import ProgramTerminator

def RunMainMenuLoop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        DrawMainMenuBackground()

        StartButtonDrawingAndHandling(gv.screen, gv.font)
        LoadGameButtonDrawingAndHandling(gv.screen, gv.font)
        SettingsButtonDrawingAndHandling(gv.screen, gv.font, gv.background)
        QuitButtonDrawingAndHandling(gv.screen, gv.font)

        updated_screen = GetUpdatedScreen()
        if updated_screen:
            gv.screen = updated_screen

        pygame.display.flip()

    ProgramTerminator.terminate()
