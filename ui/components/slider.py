import logging
from typing import Optional, Callable, Tuple

import pygame
from ui.components.button import Button

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)


class SliderButton:
    """
    A slider control for adjusting numerical values in a pygame interface.

    Attributes:
        screen (pygame.Surface): The surface to draw the slider on.
        font (pygame.font.Font): The font used for rendering texts (label and value).
        rect (pygame.Rect): The rectangle representing the slider track.
        min_value (int): The minimum slider value.
        max_value (int): The maximum slider value.
        current_value (int): The current slider value.
        step (int): The step increment when changing values.
        label (Optional[str]): Optional label displayed above the slider.
        bg_color (Tuple[int, int, int]): Background color of the slider track.
        hover_color (Tuple[int, int, int]): Color of the slider when hovered.
        text_color (Tuple[int, int, int]): Color for rendering text.
        focus_color (Tuple[int, int, int]): Color of the slider track when in focus.
        disabled (bool): If True, the slider is disabled.
        tooltip (Optional[str]): Tooltip text shown when hovering.
        sound_path (Optional[str]): Path for the click sound.
        hover_sound_path (Optional[str]): Path for the hover sound.
        focus_sound_path (Optional[str]): Path for the focus sound.
        on_value_change (Optional[Callable[[int], None]]): Callback when the slider value changes.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font,
        x: int,
        y: int,
        width: int,
        height: int,
        min_value: int = 0,
        max_value: int = 100,
        current_value: int = 50,
        step: int = 1,
        label: Optional[str] = None,
        bg_color: Tuple[int, int, int] = (80, 80, 80),
        hover_color: Tuple[int, int, int] = (100, 100, 150),
        text_color: Tuple[int, int, int] = (220, 220, 220),
        focus_color: Tuple[int, int, int] = (120, 120, 200),
        disabled: bool = False,
        tooltip: Optional[str] = None,
        sound_path: Optional[str] = None,
        hover_sound_path: Optional[str] = None,
        focus_sound_path: Optional[str] = None,
    ) -> None:
        self.screen: pygame.Surface = screen
        self.font: pygame.font.Font = font
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.min_value: int = min_value
        self.max_value: int = max_value
        # Clamp the current value between min_value and max_value
        self.current_value: int = max(min_value, min(max_value, current_value))
        self.step: int = step
        self.label: Optional[str] = label
        self.bg_color: Tuple[int, int, int] = bg_color
        self.hover_color: Tuple[int, int, int] = hover_color
        self.text_color: Tuple[int, int, int] = text_color
        self.focus_color: Tuple[int, int, int] = focus_color
        self.disabled: bool = disabled
        self.tooltip: Optional[str] = tooltip
        self.sound_path: Optional[str] = sound_path
        self.hover_sound_path: Optional[str] = hover_sound_path
        self.focus_sound_path: Optional[str] = focus_sound_path

        # State flags
        self.is_hovered: bool = False
        self.is_dragging: bool = False
        self.has_focus: bool = False

        # Callback for value change events
        self.on_value_change: Optional[Callable[[int], None]] = None

        # Sound effects (initialized below)
        self.click_sound: Optional[pygame.mixer.Sound] = None
        self.hover_sound: Optional[pygame.mixer.Sound] = None
        self.focus_sound: Optional[pygame.mixer.Sound] = None

        # Try to load click sound
        if self.sound_path:
            try:
                self.click_sound = pygame.mixer.Sound(self.sound_path)
            except Exception as e:
                logging.exception(f"Could not load click sound '{self.sound_path}': {e}")

        # Try to load hover sound
        if self.hover_sound_path:
            try:
                self.hover_sound = pygame.mixer.Sound(self.hover_sound_path)
            except Exception as e:
                logging.exception(f"Could not load hover sound '{self.hover_sound_path}': {e}")

        # Try to load focus sound
        if self.focus_sound_path:
            try:
                self.focus_sound = pygame.mixer.Sound(self.focus_sound_path)
            except Exception as e:
                logging.exception(f"Could not load focus sound '{self.focus_sound_path}': {e}")

        # Register with global slider list for event handling
        Button.all_sliders.append(self)

    def draw(self) -> None:
        """
        Draw the slider track, handle, label, current value, and tooltip (if applicable).
        """
        # Determine track color based on focus and hover states
        track_color = self.focus_color if self.has_focus else self.bg_color
        if self.is_hovered and not self.disabled:
            track_color = self.hover_color

        # Draw the slider track with rounded corners
        border_radius: int = self.rect.height // 2
        pygame.draw.rect(self.screen, track_color, self.rect, border_radius=border_radius)

        # Calculate handle position relative to current value
        value_range: int = self.max_value - self.min_value
        value_percent: float = ((self.current_value - self.min_value) / value_range) if value_range > 0 else 0
        handle_x: int = self.rect.x + int(value_percent * self.rect.width)

        # Draw the slider handle
        handle_radius: int = self.rect.height - 4
        handle_color: Tuple[int, int, int] = (200, 200, 200) if not self.disabled else (150, 150, 150)
        pygame.draw.circle(
            self.screen, 
            handle_color, 
            (handle_x, self.rect.y + self.rect.height // 2),
            handle_radius // 2
        )

        # Draw label if provided
        if self.label:
            label_text = self.font.render(self.label, True, self.text_color)
            label_rect = label_text.get_rect(bottomleft=(self.rect.x, self.rect.y - 5))
            self.screen.blit(label_text, label_rect)

        # Draw the current value text
        value_text = self.font.render(str(self.current_value), True, self.text_color)
        value_rect = value_text.get_rect(topleft=(self.rect.x, self.rect.y + self.rect.height + 5))
        self.screen.blit(value_text, value_rect)

        # Draw tooltip if hovered and tooltip text is provided
        if self.is_hovered and self.tooltip and not self.disabled:
            tooltip_font = pygame.font.Font(None, 24)
            tooltip_text = tooltip_font.render(self.tooltip, True, (255, 255, 255))
            tooltip_rect = tooltip_text.get_rect(midbottom=(self.rect.centerx, self.rect.top - 10))
            # Draw a background for the tooltip
            padding: int = 5
            bg_rect = tooltip_rect.inflate(padding * 2, padding * 2)
            pygame.draw.rect(self.screen, (50, 50, 50), bg_rect, border_radius=5)
            self.screen.blit(tooltip_text, tooltip_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Process mouse and keyboard events for slider interactions.

        Returns:
            bool: True if the event was handled; False otherwise.
        """
        if self.disabled:
            return False

        handled: bool = False
        mouse_pos = pygame.mouse.get_pos()

        # Update hover state
        was_hovered: bool = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # When starting to hover, play hover sound if available
        if self.is_hovered and not was_hovered and self.hover_sound:
            self.hover_sound.play()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_dragging = True
                self.update_value(mouse_pos[0])
                if self.click_sound:
                    self.click_sound.play()
                handled = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                handled = True

        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                self.update_value(mouse_pos[0])
                handled = True

        # Handle keyboard input for accessibility when slider has focus
        elif event.type == pygame.KEYDOWN and self.has_focus:
            if event.key == pygame.K_LEFT:
                self.adjust_value(-self.step if self.step else -1)
                handled = True
            elif event.key == pygame.K_RIGHT:
                self.adjust_value(self.step if self.step else 1)
                handled = True

        return handled

    def update_value(self, x_pos: int) -> None:
        """
        Update the slider's current value based on the provided x-coordinate.

        Args:
            x_pos (int): The x-coordinate (typically from the mouse) relative to the slider.
        """
        value_range: int = self.max_value - self.min_value
        slider_width: int = self.rect.width
        # Clamp x position between 0 and slider width
        relative_x: int = max(0, min(slider_width, x_pos - self.rect.x))
        # Calculate new value based on relative position
        new_value: float = self.min_value + (relative_x / slider_width) * value_range

        # Snap the value to the nearest step if provided
        if self.step:
            new_value = round(new_value / self.step) * self.step

        # Clamp and update if value has changed
        clamped_value: int = round(max(self.min_value, min(self.max_value, new_value)))
        if clamped_value != self.current_value:
            self.current_value = clamped_value
            if self.on_value_change:
                self.on_value_change(self.current_value)

    def adjust_value(self, amount: int) -> None:
        """
        Adjust the slider value by a specified amount, clamped within valid range.

        Args:
            amount (int): The value to add (or subtract) from the current slider value.
        """
        new_value: int = max(self.min_value, min(self.max_value, self.current_value + amount))
        if new_value != self.current_value:
            self.current_value = new_value
            if self.on_value_change:
                self.on_value_change(self.current_value)

    def set_focus(self, focus: bool) -> None:
        """
        Set the slider's focus state. If gaining focus, play the focus sound if available.

        Args:
            focus (bool): True to give the slider focus; False to remove focus.
        """
        if focus and not self.has_focus and self.focus_sound:
            self.focus_sound.play()
        self.has_focus = focus
