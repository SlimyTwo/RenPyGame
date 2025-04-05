import pygame
import sys
from ButtonUtility import RunButton

button_text = "Quit"
button_id = "quit"

def QuitButtonDrawingAndHandling(screen, font):
    width, height = screen.get_size()
    y_offset = 90
    button_rect = pygame.Rect(width // 2 - 100, height // 2 + y_offset - 40, 200, 80)

    RunButton(
        rect=button_rect,
        text=button_text,
        button_id=button_id,
        screen=screen,
        font=font,
        on_click=ExitGame
    )

def ExitGame():
    pygame.time.delay(300)
    pygame.quit()
    sys.exit()
