import pygame
from screens.SettingsScreen import ShowSettingsScreen
from ui.ButtonUtility import RunButton

button_text = "Settings"
button_id = "settings"
background_ref = None

# Track the updated screen across menus
updated_screen_ref = [None]  # Mutable wrapper

def SettingsButtonDrawingAndHandling(screen, font, background):
    global background_ref
    background_ref = background

    width, height = screen.get_size()
    y_offset = 30
    button_rect = pygame.Rect(width // 2 - 100, height // 2 + y_offset - 40, 200, 80)

    def on_click():
        updated_screen = ShowSettingsScreen(screen, font, background_ref)
        updated_screen_ref[0] = updated_screen  # Store for access outside

    RunButton(
        rect=button_rect,
        text=button_text,
        button_id=button_id,
        screen=screen,
        font=font,
        on_click=on_click
    )

# Optional: a helper to access updated screen after settings
def GetUpdatedScreen():
    return updated_screen_ref[0]
