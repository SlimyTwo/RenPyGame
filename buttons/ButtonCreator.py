import pygame
from buttons.ButtonClass import Button
from buttons.SliderClass import SliderButton  # Add import for the slider


def create_button(screen, font, text="Button", **kwargs):
    """
    Create a button with customizable parameters.

    Required params:
      screen: The pygame surface to draw on
      font: Font for button text
      text: Button text label

    Optional params (passed as kwargs):
      x, y: Direct position coordinates
      width, height: Button dimensions
      x_offset, y_offset: Position offsets from center
      on_click: Button click handler function
      music_manager: MusicManager instance for volume control
    """
    # Extract position parameters
    x = kwargs.get('x', None)
    y = kwargs.get('y', None)
    width = kwargs.get('width', 200)
    height = kwargs.get('height', 50)
    x_offset = kwargs.get('x_offset', 0)
    y_offset = kwargs.get('y_offset', 0)

    # Extract music_manager
    music_manager = kwargs.get('music_manager', None)

    # Create a safe button ID from the text (remove non-alphanumeric chars)
    button_id = kwargs.get('button_id', f"btn_{''.join(c for c in text if c.isalnum() or c == '_')}")

    # Handle string color names by converting to RGB tuples
    debug_color = kwargs.get('debug_color', (255, 0, 0))
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
        debug_color = color_map.get(debug_color.lower(), (255, 0, 0))

    # Create rect based on provided parameters
    screen_width, screen_height = screen.get_size()
    if x is not None and y is not None:
        # Use direct position if provided
        button_rect = pygame.Rect(x, y, width, height)
    else:
        # Center with offsets
        button_rect = pygame.Rect(
            screen_width // 2 - width // 2 + x_offset,
            screen_height // 2 + y_offset,
            width,
            height
        )

    # Handle shape parameters
    shape = kwargs.get('shape', 'rectangle')
    shape_params = kwargs.get('shape_params', None)

    # For circle shape, calculate radius if not provided
    if shape == "circle" and (not shape_params or "radius" not in shape_params):
        radius = min(width, height) // 2
        shape_params = shape_params or {}
        shape_params["radius"] = radius

    # For polygon shape, set default triangle if no points provided
    if shape == "polygon" and (not shape_params or "points" not in shape_params):
        # Default to a triangle as example
        center_x = button_rect.centerx
        center_y = button_rect.centery
        shape_params = shape_params or {}
        shape_params["points"] = [
            (center_x, center_y - height // 2),  # Top
            (center_x - width // 2, center_y + height // 2),  # Bottom left
            (center_x + width // 2, center_y + height // 2),  # Bottom right
        ]

    # Extract on_click handler
    on_click = kwargs.get('on_click', lambda: print(f"{text.splitlines()[0]} clicked!"))

    # Create the button with all parameters
    button = Button(
        rect=button_rect,
        text=text,
        button_id=button_id,
        screen=screen,
        font=font,
        on_click=on_click,
        music_manager=music_manager,  # Add music_manager
        bg_color=kwargs.get('bg_color', (120, 120, 120)),
        hover_color=kwargs.get('hover_color', (160, 160, 160)),
        text_color=kwargs.get('text_color', (255, 255, 255)),
        hover_text_color=kwargs.get('hover_text_color', None),
        border_color=kwargs.get('border_color', (50, 50, 50)),
        border_width=kwargs.get('border_width', 1),
        visible_background=kwargs.get('visible_background', True),
        debug_hitbox=kwargs.get('debug_hitbox', False),
        debug_color=debug_color,
        icon=kwargs.get('icon', None),
        tooltip=kwargs.get('tooltip', None),
        disabled=kwargs.get('disabled', False),
        animation_speed=kwargs.get('animation_speed', 5),
        hover_text=kwargs.get('hover_text', None),
        sound_path=kwargs.get('sound_path', None),
        hover_sound_path=kwargs.get('hover_sound_path', None),
        focus_sound_path=kwargs.get('focus_sound_path', None),
        text_align=kwargs.get('text_align', 'center'),
        shape=shape,
        shape_params=shape_params,
        badge_text=kwargs.get('badge_text', None),
        badge_color=kwargs.get('badge_color', (255, 0, 0)),
        badge_position=kwargs.get('badge_position', 'topright'),
        shortcut_key=kwargs.get('shortcut_key', None),
        toggle_mode=kwargs.get('toggle_mode', False),
        toggled=kwargs.get('toggled', False),
        toggle_color=kwargs.get('toggle_color', (160, 160, 200)),
        focus_color=kwargs.get('focus_color', (200, 200, 255)),
        focus_border_color=kwargs.get('focus_border_color', (100, 100, 255)),
        translation_func=kwargs.get('translation_func', None)
    )

    # Add to button group if provided
    button_group = kwargs.get('button_group', None)
    if button_group:
        button_group.add(button)

    return button


def create_slider(screen, font, **kwargs):
    """
    Create a slider with customizable parameters.

    Required params:
      screen: The pygame surface to draw on
      font: Font for value text

    Optional params (passed as kwargs):
      x, y: Direct position coordinates
      width, height: Slider dimensions
      x_offset, y_offset: Position offsets from center
      min_value, max_value, current_value: Slider range and position
      music_manager: MusicManager instance for volume control
    """
    # Extract basic parameters
    x = kwargs.get('x', None)
    y = kwargs.get('y', None)
    width = kwargs.get('width', 200)
    height = kwargs.get('height', 30)
    x_offset = kwargs.get('x_offset', 0)
    y_offset = kwargs.get('y_offset', 0)

    # Extract slider specific parameters
    min_value = kwargs.get('min_value', 0)
    max_value = kwargs.get('max_value', 100)
    current_value = kwargs.get('current_value', 50)
    step = kwargs.get('step', 1)
    label = kwargs.get('label', None)

    # Remove music_manager from kwargs so it won't be passed to SliderButton
    if 'music_manager' in kwargs:
        kwargs.pop('music_manager')

    # Calculate position
    screen_width, screen_height = screen.get_size()
    if x is not None and y is not None:
        # Use direct position if provided
        slider_x, slider_y = x, y
    else:
        # Center with offsets
        slider_x = screen_width // 2 - width // 2 + x_offset
        slider_y = screen_height // 2 + y_offset

    # Create the slider
    slider = SliderButton(
        screen=screen,
        font=font,
        x=slider_x,
        y=slider_y,
        width=width,
        height=height,
        min_value=min_value,
        max_value=max_value,
        current_value=current_value,
        step=step,
        label=label,
        **{k: v for k, v in kwargs.items() if k not in ['x', 'y', 'width', 'height',
                                                        'x_offset', 'y_offset',
                                                        'min_value', 'max_value',
                                                        'current_value', 'step', 'label']}
    )

    return slider