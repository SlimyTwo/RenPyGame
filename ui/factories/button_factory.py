import logging
from typing import Any, Dict, Optional

import pygame
from ui.components.button import Button
from ui.components.slider import SliderButton

logging.basicConfig(level=logging.DEBUG)


def create_button(screen: pygame.Surface, font: pygame.font.Font, text: str = "Button", **kwargs: Any) -> Button:
    """
    Create a button with customizable parameters.

    Required parameters:
      screen: The pygame surface to draw on.
      font: The font for the button text.
      text: The text displayed on the button.

    Optional kwargs include:
      x, y: Direct position coordinates.
      width, height: Button dimensions.
      x_offset, y_offset: Position offsets from the screen's center.
      on_click: The callback function to execute on a click.
      music_manager: MusicManager instance for sound management.
      [Plus many other style or behavior overrides.]

    Returns:
      An instance of Button.
    """
    # Position and size parameters
    x: Optional[int] = kwargs.get('x', None)
    y: Optional[int] = kwargs.get('y', None)
    width: int = kwargs.get('width', 200)
    height: int = kwargs.get('height', 50)
    x_offset: int = kwargs.get('x_offset', 0)
    y_offset: int = kwargs.get('y_offset', 0)

    # Extract the music_manager dependency if provided
    music_manager = kwargs.get('music_manager', None)

    # Create a safe button ID from the text (remove non-alphanumeric characters)
    button_id: str = kwargs.get('button_id', f"btn_{''.join(c for c in text if c.isalnum() or c == '_')}")

    # Convert debug_color string to an RGB tuple if needed
    debug_color: Any = kwargs.get('debug_color', (255, 0, 0))
    if isinstance(debug_color, str):
        color_map: Dict[str, Any] = {
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

    # Determine the button rectangle based on direct coordinates or centering with offsets
    screen_width, screen_height = screen.get_size()
    if x is not None and y is not None:
        button_rect = pygame.Rect(x, y, width, height)
    else:
        button_rect = pygame.Rect(
            screen_width // 2 - width // 2 + x_offset,
            screen_height // 2 + y_offset,
            width,
            height
        )

    # Handle shape parameters (rectangle, circle, polygon)
    shape: str = kwargs.get('shape', 'rectangle')
    shape_params: Optional[Dict[str, Any]] = kwargs.get('shape_params', None)

    # For circle shape, calculate default radius if not provided
    if shape == "circle" and (not shape_params or "radius" not in shape_params):
        radius = min(width, height) // 2
        shape_params = shape_params or {}
        shape_params["radius"] = radius

    # For polygon shape, set default triangle if no points provided
    if shape == "polygon" and (not shape_params or "points" not in shape_params):
        center_x = button_rect.centerx
        center_y = button_rect.centery
        shape_params = shape_params or {}
        shape_params["points"] = [
            (center_x, center_y - height // 2),         # Top
            (center_x - width // 2, center_y + height // 2),  # Bottom left
            (center_x + width // 2, center_y + height // 2),  # Bottom right
        ]

    # Extract on_click handler; default just prints a message
    on_click = kwargs.get('on_click', lambda: logging.info(f"{text.splitlines()[0]} clicked!"))

    # Create the button instance with all parameters
    button = Button(
        rect=button_rect,
        text=text,
        button_id=button_id,
        screen=screen,
        font=font,
        on_click=on_click,
        music_manager=music_manager,
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

    # Add the button to a group if a button_group instance is passed
    button_group = kwargs.get('button_group', None)
    if button_group:
        button_group.add(button)

    return button


def create_slider(screen: pygame.Surface, font: pygame.font.Font, **kwargs: Any) -> SliderButton:
    """
    Create a slider with customizable parameters.

    Required parameters:
      screen: The pygame surface to draw on.
      font: The font used for slider value text.

    Optional kwargs include:
      x, y: Direct position coordinates.
      width, height: Slider dimensions.
      x_offset, y_offset: Position offsets from center.
      min_value, max_value, current_value: The slider's numerical range and current position.
      label: An optional label text for the slider.
      music_manager: This key is removed for slider instantiation.
      [Other customizations may be provided.]

    Returns:
      An instance of SliderButton.
    """
    # Basic positioning and size parameters
    x: Optional[int] = kwargs.get('x', None)
    y: Optional[int] = kwargs.get('y', None)
    width: int = kwargs.get('width', 200)
    height: int = kwargs.get('height', 30)
    x_offset: int = kwargs.get('x_offset', 0)
    y_offset: int = kwargs.get('y_offset', 0)

    # Slider specific parameters
    min_value: int = kwargs.get('min_value', 0)
    max_value: int = kwargs.get('max_value', 100)
    current_value: int = kwargs.get('current_value', 50)
    step: int = kwargs.get('step', 1)
    label: Optional[str] = kwargs.get('label', None)

    # Remove music_manager from kwargs so it is not passed to SliderButton constructor.
    kwargs.pop('music_manager', None)

    # Calculate slider position either directly or using center offsets
    screen_width, screen_height = screen.get_size()
    if x is not None and y is not None:
        slider_x, slider_y = x, y
    else:
        slider_x = screen_width // 2 - width // 2 + x_offset
        slider_y = screen_height // 2 + y_offset

    # Create the slider, forwarding any extra kwargs that are not explicitly extracted.
    extra_kwargs = {
        k: v for k, v in kwargs.items()
        if k not in ['x', 'y', 'width', 'height', 'x_offset', 'y_offset', 'min_value', 'max_value', 'current_value', 'step', 'label']
    }
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
        **extra_kwargs
    )
    return slider
