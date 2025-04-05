import pygame
from ui.ButtonUtility import RunButton

button_text = "Load Game"
button_id = "load"

def LoadGameButtonDrawingAndHandling(screen, font):
    width, height = screen.get_size()
    y_offset = -30
    button_rect = pygame.Rect(width // 2 - 100, height // 2 + y_offset - 40, 200, 80)

    RunButton(
        rect=button_rect,
        text=button_text,
        button_id=button_id,
        screen=screen,
        font=font,
        on_click=lambda: print("Load game clicked!")
    )
