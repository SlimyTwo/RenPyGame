import pygame

from utility.CompleteProgramTermination import ProgramTerminator
from screens.RunningPygameBasics import RunningPygameBasics
from screens.MainMenuGameLoop import RunMainMenuLoop

pygame.init()

RunningPygameBasics()

RunMainMenuLoop()

ProgramTerminator.terminate()
