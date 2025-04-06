import pygame
from buttons.ButtonClass import Button, ButtonGroup


def create_test_button(screen, font, width=200, height=80, y_offset=50, text="Test Button",
                       visible_background=True, debug_hitbox=False, debug_color=(255, 0, 0),
                       icon=None, tooltip=None, disabled=False, button_group=None):
    """
    Create a test button with customizable parameters for demonstration purposes.

    Args:
        screen: pygame surface to draw on
        font: pygame font for text
        width: Button width in pixels
        height: Button height in pixels
        y_offset: Vertical offset from screen center
        text: Text to display on button
        visible_background: Whether to draw the button background
        debug_hitbox: Whether to display a thin outline showing the button's hitbox
        debug_color: Color for the debug hitbox outline (RGB tuple or color name)
        icon: Optional pygame Surface to display as an icon
        tooltip: Optional text to display when hovering
        disabled: Whether the button is disabled
        button_group: Optional ButtonGroup this button belongs to
    """
    # Handle string color names (like "Green") by converting to RGB tuples
    if isinstance(debug_color, str):
        color_map = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "yellow": (255, 255, 0),
            "purple": (128, 0, 128),
            "orange": (255, 165, 0),
            "cyan": (0, 255, 255),
            "magenta": (255, 0, 255)
        }
        debug_color = color_map.get(debug_color.lower(), (255, 0, 0))  # Default to red if not found

    screen_width, screen_height = screen.get_size()
    button_rect = pygame.Rect(
        screen_width // 2 - width // 2,  # Center horizontally
        screen_height // 2 + y_offset,  # Position vertically with offset
        width,  # Custom width
        height  # Custom height
    )

    button = Button(
        rect=button_rect,
        text=text,
        button_id=f"test_{text}",
        screen=screen,
        font=font,
        on_click=lambda: print(f"{text} clicked!"),
        bg_color=(120, 120, 120),
        hover_color=(160, 160, 160),
        border_color=(50, 50, 50),
        visible_background=visible_background,
        debug_hitbox=debug_hitbox,
        debug_color=debug_color,
        icon=icon,
        tooltip=tooltip,
        disabled=disabled
    )

    if button_group:
        button_group.add(button)

    return button