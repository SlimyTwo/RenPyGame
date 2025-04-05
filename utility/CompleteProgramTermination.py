import pygame
import sys

class ProgramTerminator:
    @classmethod
    def terminate(cls):
        print("Terminating game...")
        # Save state, stop music, fade out, etc.
        pygame.quit()
        sys.exit()