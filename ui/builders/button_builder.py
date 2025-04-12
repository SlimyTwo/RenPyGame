# button_builder.py

import logging
from typing import Any, Dict, Optional

import pygame
from ui.components.button import Button

logging.basicConfig(level=logging.DEBUG)


class ButtonBuilder:
    """
    A builder class to configure and create Button instances step by step.
    This is similar to create_button(...) in button_factory.py, but uses
    a chainable, object-oriented approach.
    """

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, text: str = "Button"):
        """
        Initialize the builder with required basics. You can add additional
        required parameters here if needed.
        """
        self.screen = screen
        self.font = font
        self.text = text

        # Default values mirroring your create_button(...) function
        self.x: Optional[int] = None
        self.y: Optional[int] = None
        self.width: int = 200
        self.height: int = 50
        self.x_offset: int = 0
        self.y_offset: int = 0

        self.on_click: Optional[Any] = None
        self.music_manager: Optional[Any] = None
        self.button_id: Optional[str] = None

        self.debug_color: Any = (255, 0, 0)
        self.debug_hitbox: bool = False

        self.bg_color: tuple = (120, 120, 120)
        self.hover_color: tuple = (160, 160, 160)
        self.text_color: tuple = (255, 255, 255)
        self.hover_text_color: Optional[tuple] = None
        self.border_color: tuple = (50, 50, 50)
        self.border_width: int = 1
        self.visible_background: bool = True

        self.icon: Optional[pygame.Surface] = None
        self.tooltip: Optional[str] = None
        self.disabled: bool = False
        self.animation_speed: int = 5
        self.hover_text: Optional[str] = None

        self.sound_path: Optional[str] = None
        self.hover_sound_path: Optional[str] = None

        self.text_align: str = "center"

        self.shape: str = "rectangle"
        self.shape_params: Optional[Dict[str, Any]] = None

        self.badge_text: Optional[str] = None
        self.badge_color: tuple = (255, 0, 0)
        self.badge_position: str = "topright"

        self.shortcut_key: Optional[int] = None

        self.toggle_mode: bool = False
        self.toggled: bool = False
        self.toggle_color: tuple = (160, 160, 200)

        self.translation_func: Optional[Any] = None

    # ----- Chainable setters for each field -----
    def set_position(self, x: int, y: int) -> "ButtonBuilder":
        self.x = x
        self.y = y
        return self

    def set_size(self, width: int, height: int) -> "ButtonBuilder":
        self.width = width
        self.height = height
        return self

    def set_offsets(self, x_offset: int, y_offset: int) -> "ButtonBuilder":
        self.x_offset = x_offset
        self.y_offset = y_offset
        return self

    def set_on_click(self, callback) -> "ButtonBuilder":
        self.on_click = callback
        return self

    def set_music_manager(self, manager) -> "ButtonBuilder":
        self.music_manager = manager
        return self

    def set_button_id(self, button_id: str) -> "ButtonBuilder":
        self.button_id = button_id
        return self

    def set_debug_color(self, color) -> "ButtonBuilder":
        self.debug_color = color
        return self

    def set_debug_hitbox(self, enabled: bool) -> "ButtonBuilder":
        self.debug_hitbox = enabled
        return self

    def set_background_color(self, color: tuple) -> "ButtonBuilder":
        self.bg_color = color
        return self

    def set_hover_color(self, color: tuple) -> "ButtonBuilder":
        self.hover_color = color
        return self

    def set_text_color(self, color: tuple) -> "ButtonBuilder":
        self.text_color = color
        return self

    def set_hover_text_color(self, color: tuple) -> "ButtonBuilder":
        self.hover_text_color = color
        return self

    def set_border_color(self, color: tuple) -> "ButtonBuilder":
        self.border_color = color
        return self

    def set_border_width(self, width: int) -> "ButtonBuilder":
        self.border_width = width
        return self

    def set_is_background_visible(self, visible: bool) -> "ButtonBuilder":
        self.visible_background = visible
        return self

    def set_icon(self, icon: pygame.Surface) -> "ButtonBuilder":
        self.icon = icon
        return self

    def set_tooltip(self, tooltip: str) -> "ButtonBuilder":
        self.tooltip = tooltip
        return self

    def set_disabled(self, disabled: bool) -> "ButtonBuilder":
        self.disabled = disabled
        return self

    def set_animation_speed(self, speed: int) -> "ButtonBuilder":
        self.animation_speed = speed
        return self

    def set_hover_text(self, text: str) -> "ButtonBuilder":
        self.hover_text = text
        return self

    def set_sounds(self, click_sound: str, hover_sound: str = None) -> "ButtonBuilder":
        self.sound_path = click_sound
        self.hover_sound_path = hover_sound
        return self

    def set_text_align(self, align: str) -> "ButtonBuilder":
        self.text_align = align
        return self

    def set_shape(self, shape: str, shape_params: Optional[Dict[str, Any]] = None) -> "ButtonBuilder":
        self.shape = shape
        self.shape_params = shape_params
        return self

    def set_badge(self, badge_text: str, badge_color: tuple = (255, 0, 0), badge_position: str = "topright") -> "ButtonBuilder":
        self.badge_text = badge_text
        self.badge_color = badge_color
        self.badge_position = badge_position
        return self

    def set_shortcut_key(self, key: int) -> "ButtonBuilder":
        self.shortcut_key = key
        return self

    def set_toggle_mode(self, toggle_mode: bool, toggled: bool = False, toggle_color: tuple = (160, 160, 200)) -> "ButtonBuilder":
        self.toggle_mode = toggle_mode
        self.toggled = toggled
        self.toggle_color = toggle_color
        return self

    def set_translation_func(self, func) -> "ButtonBuilder":
        self.translation_func = func
        return self


    @staticmethod
    def default_button(screen: pygame.Surface, font: pygame.font.Font, text: str = "Default Button") -> "ButtonBuilder":
        """
        Creates a ButtonBuilder instance with default styling preset.
        
        Args:
            screen: The pygame surface to draw on
            font: The font to use for text rendering
            text: Button text
            
        Returns:
            A pre-configured ButtonBuilder instance
        """
        return (ButtonBuilder(screen, font, text)
                .set_is_background_visible(True)
                .set_background_color((0, 0, 0))
                .set_size(500, 70)
                )

    # ----- FINAL BUILD METHOD -----
    def build(self) -> Button:
        """
        Create the Button instance, applying any logic that was in create_button(...).
        Similar to your create_button in button_factory.py, but we use self fields
        instead of kwargs.
        """
        # Determine final x,y based on offsets if x,y not explicitly set
        screen_width, screen_height = self.screen.get_size()
        if self.x is not None and self.y is not None:
            button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        else:
            button_rect = pygame.Rect(
                screen_width // 2 - self.width // 2 + self.x_offset,
                screen_height // 2 + self.y_offset,
                self.width,
                self.height
            )

        # If debug_color is a string, you could do a color_map lookup here if needed
        # for now, assume it's already an RGB tuple

        # Generate an ID if none was supplied
        if not self.button_id:
            safe_text = "".join(c for c in self.text if c.isalnum() or c == '_')
            self.button_id = f"btn_{safe_text}"

        # Create the Button instance
        btn = Button(
            rect=button_rect,
            text=self.text,
            button_id=self.button_id,
            screen=self.screen,
            font=self.font,
            on_click=self.on_click or (lambda: logging.info(f"{self.text} clicked!")),
            music_manager=self.music_manager,
            bg_color=self.bg_color,
            hover_color=self.hover_color,
            text_color=self.text_color,
            hover_text_color=self.hover_text_color,
            border_color=self.border_color,
            border_width=self.border_width,
            visible_background=self.visible_background,
            debug_hitbox=self.debug_hitbox,
            debug_color=self.debug_color,
            icon=self.icon,
            tooltip=self.tooltip,
            disabled=self.disabled,
            animation_speed=self.animation_speed,
            hover_text=self.hover_text,
            sound_path=self.sound_path,
            hover_sound_path=self.hover_sound_path,
            text_align=self.text_align,
            shape=self.shape,
            shape_params=self.shape_params,
            badge_text=self.badge_text,
            badge_color=self.badge_color,
            badge_position=self.badge_position,
            shortcut_key=self.shortcut_key,
            toggle_mode=self.toggle_mode,
            toggled=self.toggled,
            toggle_color=self.toggle_color,
            translation_func=self.translation_func
        )

        return btn
