from ui.ButtonClickHandler import handle_button_click
from ui.ButtonTextRenderer import draw_button_text

def RunButton(rect, text, button_id, screen, font, on_click):
    hovered = handle_button_click(rect, on_click, id=button_id)
    draw_button_text(screen, font, text, rect.center, hovered)
