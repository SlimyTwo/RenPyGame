import pygame
from ButtonUtility import RunButton

button_text = "Start Game"
button_id = "start"

def StartButtonDrawingAndHandling(screen, font):
    width, height = screen.get_size()
    y_offset = -90
    button_rect = pygame.Rect(width // 2 - 100, height // 2 + y_offset - 40, 200, 80)

    RunButton(
        rect=button_rect,
        text=button_text,
        button_id=button_id,
        screen=screen,
        font=font,
        on_click=lambda: print("Start game clicked!")
    )
