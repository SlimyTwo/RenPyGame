import pygame
from buttons.ButtonClass import Button  # Remove ButtonGroup from import


def create_button(screen, font, width=200, height=80, y_offset=50, x_offset=0, text="Button",
                  hover_text=None, hover_text_color=None,  # Added hover_text_color parameter
                  visible_background=True, debug_hitbox=False, debug_color=(255, 0, 0),
                  icon=None, tooltip=None, disabled=False, button_group=None,
                  sound_path=None, hover_sound_path=None, focus_sound_path=None,
                  text_align="center", shape="rectangle", shape_params=None,
                  badge_text=None, badge_color=(255, 0, 0), badge_position="topright",
                  shortcut_key=None, toggle_mode=False, toggled=False, toggle_color=(160, 160, 200),
                  focus_color=(200, 200, 255), focus_border_color=(100, 100, 255),
                  bg_color=(120, 120, 120), hover_color=(160, 160, 160), text_color=(255, 255, 255),
                  border_color=(50, 50, 50), translation_func=None, animation_speed=5):
    """
    Create a button with customizable parameters.
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

    # Create a safe button ID from the text (remove non-alphanumeric chars)
    button_id = f"btn_{''.join(c for c in text if c.isalnum() or c == '_')}"

    screen_width, screen_height = screen.get_size()
    button_rect = pygame.Rect(
        screen_width // 2 - width // 2 + x_offset,  # Center horizontally with offset
        screen_height // 2 + y_offset,  # Position vertically with offset
        width,  # Custom width
        height  # Custom height
    )

    # For circle shape, calculate radius if not provided
    if shape == "circle" and (not shape_params or "radius" not in shape_params):
        radius = min(width, height) // 2
        shape_params = shape_params or {}
        shape_params["radius"] = radius

    # For polygon shape, set default triangle if no points provided
    if shape == "polygon" and (not shape_params or "points" not in shape_params):
        # Default to a triangle as example
        center_x = screen_width // 2
        center_y = screen_height // 2 + y_offset
        shape_params = shape_params or {}
        shape_params["points"] = [
            (center_x, center_y - height // 2),  # Top
            (center_x - width // 2, center_y + height // 2),  # Bottom left
            (center_x + width // 2, center_y + height // 2)  # Bottom right
        ]

    button = Button(
        rect=button_rect,
        text=text,
        button_id=button_id,
        screen=screen,
        font=font,
        on_click=lambda: print(f"{text.splitlines()[0]} clicked!"),
        bg_color=bg_color,
        hover_color=hover_color,
        text_color=text_color,
        hover_text_color=hover_text_color,  # Pass through the hover text color
        border_color=border_color,
        visible_background=visible_background,
        debug_hitbox=debug_hitbox,
        debug_color=debug_color,
        icon=icon,
        tooltip=tooltip,
        disabled=disabled,
        animation_speed=animation_speed,
        hover_text=hover_text,  # Pass through the hover_text parameter

        # Feature parameters
        sound_path=sound_path,
        hover_sound_path=hover_sound_path,
        focus_sound_path=focus_sound_path,
        text_align=text_align,
        shape=shape,
        shape_params=shape_params,
        badge_text=badge_text,
        badge_color=badge_color,
        badge_position=badge_position,
        shortcut_key=shortcut_key,
        toggle_mode=toggle_mode,
        toggled=toggled,
        toggle_color=toggle_color,
        focus_color=focus_color,
        focus_border_color=focus_border_color,
        translation_func=translation_func
    )

    if button_group:
        button_group.add(button)

    return button