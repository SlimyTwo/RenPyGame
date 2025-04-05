import pygame

from screens.MainMenuSetup import ExecuteMainMenuSetup
from utility.CompleteProgramTermination import ProgramTerminator

pygame.init()

ExecuteMainMenuSetup()

ProgramTerminator.terminate()
