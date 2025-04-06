import pygame

from utility.CompleteProgramTermination import ProgramTerminator
from screens.RunningPygameBasics import RunningPygameBasics
from screens.MainMenuGameLoop import RunMainMenuLoop

RunningPygameBasics()

RunMainMenuLoop()

ProgramTerminator.terminate()
