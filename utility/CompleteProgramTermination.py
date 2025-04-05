import pygame
import sys

def SystemTermination():
    print("Terminating game...")
    # Save state, stop music, fade out, etc.
    pygame.quit()
    sys.exit()