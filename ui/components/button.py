import logging
from typing import Any, Callable, Dict, List, Optional, Tuple

import pygame
from engine.music import MusicManager

logging.basicConfig(level=logging.DEBUG)


class Button:
    """
    A versatile button class for pygame interfaces with advanced features.

    Class Attributes:
      instances: Buttons with textual labels.
      all_buttons: All button instances used for keyboard navigation.
      focused_button: The currently focused button.
      all_sliders: Slider instances for keyboard navigation.
    """
    instances: List["Button"] = []
    all_buttons: List["Button"] = []
    focused_button: Optional["Button"] = None
    all_sliders: List[Any] = []  # List of slider instances (type from SliderButton if desired)

    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        button_id: str,
        screen: pygame.Surface,
        font: pygame.font.Font,
        on_click: Optional[Callable[[], Any]] = None,
        bg_color: Tuple[int, int, int] = (100, 100, 100),
        hover_color: Tuple[int, int, int] = (150, 150, 150),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        hover_text_color: Optional[Tuple[int, int, int]] = None,
        border_color: Tuple[int, int, int] = (200, 200, 200),
        border_width: int = 1,
        visible_background: bool = True,
        debug_hitbox: bool = False,
        debug_color: Tuple[int, int, int] = (255, 0, 0),
        icon: Optional[pygame.Surface] = None,
        tooltip: Optional[str] = None,
        disabled: bool = False,
        sound_path: Optional[str] = None,
        hover_sound_path: Optional[str] = None,
        focus_sound_path: Optional[str] = None,
        text_align: str = "center",
        shape: str = "rectangle",
        shape_params: Optional[Dict[str, Any]] = None,
        badge_text: Optional[str] = None,
        badge_color: Tuple[int, int, int] = (255, 0, 0),
        badge_position: str = "topright",
        shortcut_key: Optional[int] = None,
        toggle_mode: bool = False,
        toggled: bool = False,
        toggle_color: Tuple[int, int, int] = (160, 160, 200),
        focus_color: Tuple[int, int, int] = (200, 200, 255),
        focus_border_color: Tuple[int, int, int] = (100, 100, 255),
        translation_func: Optional[Callable[[str], str]] = None,
        animation_speed: int = 5,
        hover_text: Optional[str] = None,
        music_manager: Optional[MusicManager] = None
    ) -> None:
        """Initialize a new Button instance with advanced features."""
        self.rect = rect
        self.original_text = text
        self.hover_text = hover_text or text
        self.text = text
        self.id = button_id
        self.screen = screen
        self.font = font
        self.on_click = on_click
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hover_text_color = hover_text_color or text_color
        self.border_color = border_color
        self.border_width = border_width
        self.visible_background = visible_background
        self.show_hitbox = debug_hitbox
        self.hitbox_color = debug_color
        self.icon = icon
        self.tooltip = tooltip
        self.disabled = disabled
        self.animation_speed = animation_speed

        # State flags
        self.hovered: bool = False
        self.clicked: bool = False
        self.focused: bool = False

        # Animation state
        self.hover_alpha: int = 0
        self.tooltip_alpha: int = 0
        self.click_effect: int = 0

        # Advanced features
        self.tooltip_font = pygame.font.Font(None, 20)
        self.sound_path = sound_path
        self.hover_sound_path = hover_sound_path
        self.focus_sound_path = focus_sound_path
        self.sounds_loaded: bool = False
        self.text_align = text_align
        self.shape = shape
        self.shape_params = shape_params or {}
        self.badge_text = badge_text
        self.badge_color = badge_color
        self.badge_position = badge_position
        self.shortcut_key = shortcut_key
        self.toggle_mode = toggle_mode
        self.toggled = toggled
        self.toggle_color = toggle_color
        self.focus_color = focus_color
        self.focus_border_color = focus_border_color
        self.translation_func = translation_func
        self.group: Optional["ButtonGroup"] = None

        # Music manager for playing sounds (if provided)
        self.music_manager = music_manager

        # Add to global tracking lists
        Button.all_buttons.append(self)
        Button.instances.append(self)

        # Load sound effects if possible
        self._load_sounds()

    def _load_sounds(self) -> None:
        """Load sound effects if available; log errors if they occur."""
        if not pygame.mixer.get_init():
            logging.debug("Pygame mixer not initialized; skipping sound loading.")
            return

        try:
            self.click_sound = pygame.mixer.Sound(self.sound_path) if self.sound_path else None
            self.hover_sound = pygame.mixer.Sound(self.hover_sound_path) if self.hover_sound_path else None
            self.focus_sound = pygame.mixer.Sound(self.focus_sound_path) if self.focus_sound_path else None
            self.sounds_loaded = True
        except Exception as e:
            logging.exception(f"Error loading sounds for button '{self.id}': {e}")

    def draw(self) -> None:
        """Draw the button on the screen with appropriate visual effects."""
        # Select colors based on state
        if self.disabled:
            bg_color = tuple(max(0, c - 50) for c in self.bg_color)
            border_color = tuple(max(0, c - 50) for c in self.border_color)
            text_color = tuple(max(0, c - 100) for c in self.text_color)
        elif self.toggled and self.toggle_mode:
            bg_color = self.toggle_color
            border_color = self.border_color
            text_color = self.text_color
        elif self.focused:
            bg_color = self.focus_color
            border_color = self.focus_border_color
            text_color = self.text_color
        elif self.hovered:
            bg_color = self.hover_color
            border_color = self.border_color
            text_color = self.hover_text_color
        else:
            bg_color = self.bg_color
            border_color = self.border_color
            text_color = self.text_color

        # Draw the button background by shape
        if self.visible_background:
            if self.shape == "rectangle":
                pygame.draw.rect(self.screen, bg_color, self.rect, border_radius=5)
                if self.border_width > 0:
                    pygame.draw.rect(self.screen, border_color, self.rect, width=self.border_width, border_radius=5)
            elif self.shape == "circle":
                radius = self.shape_params.get("radius", min(self.rect.width, self.rect.height) // 2)
                pygame.draw.circle(self.screen, bg_color, self.rect.center, radius)
                if self.border_width > 0:
                    pygame.draw.circle(self.screen, border_color, self.rect.center, radius, width=self.border_width)
            elif self.shape == "polygon":
                points = self.shape_params.get("points", [])
                if points:
                    pygame.draw.polygon(self.screen, bg_color, points)
                    if self.border_width > 0:
                        pygame.draw.polygon(self.screen, border_color, points, width=self.border_width)

        # Optionally draw a semi-transparent hitbox for debugging
        if self.show_hitbox:
            hitbox_color = self.hitbox_color + ((100,) if len(self.hitbox_color) == 3 else ())
            hitbox_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            pygame.draw.rect(hitbox_surface, hitbox_color, hitbox_surface.get_rect(), width=1, border_radius=5)
            self.screen.blit(hitbox_surface, self.rect)

        # Determine the text to display (hover or normal)
        current_text = self.hover_text if self.hovered else self.original_text
        self._draw_text(current_text, text_color)

        # Draw icon if provided
        if self.icon:
            icon_rect = self.icon.get_rect(center=self.rect.center)
            if self.text:
                if self.text_align == "left":
                    icon_rect.left = self.rect.left + 10
                elif self.text_align == "right":
                    icon_rect.right = self.rect.right - 10
                else:
                    icon_rect.centerx = self.rect.centerx - len(self.text) * 4
            self.screen.blit(self.icon, icon_rect)

        # Draw badge if available
        if self.badge_text:
            self._draw_badge()

        # Draw tooltip if hovering
        if self.hovered and self.tooltip:
            self._draw_tooltip()

    def _draw_text(self, text: str, text_color: Tuple[int, int, int]) -> None:
        """Draw text on the button, handling multiline cases and alignment."""
        if not text:
            return

        lines = text.split('\n')
        line_spacing = 2
        total_height = sum(self.font.size(line)[1] for line in lines) + (line_spacing * (len(lines) - 1))
        y = self.rect.centery - total_height // 2

        for line in lines:
            text_surf = self.font.render(line, True, text_color)
            text_rect = text_surf.get_rect()
            if self.text_align == "left":
                text_rect.left = self.rect.left + 10
            elif self.text_align == "right":
                text_rect.right = self.rect.right - 10
            else:
                text_rect.centerx = self.rect.centerx
            text_rect.y = y
            self.screen.blit(text_surf, text_rect)
            y += text_rect.height + line_spacing

    def _draw_badge(self) -> None:
        """Draw a notification badge on the button."""
        badge_font = pygame.font.Font(None, 20)
        badge_surf = badge_font.render(str(self.badge_text), True, (255, 255, 255))
        badge_rect = badge_surf.get_rect()

        padding = 4
        badge_bg_width = max(badge_rect.width + padding * 2, badge_rect.height + padding)
        badge_bg_height = badge_rect.height + padding

        if self.badge_position == "topleft":
            badge_x = self.rect.left - badge_bg_width // 2
            badge_y = self.rect.top - badge_bg_height // 2
        elif self.badge_position == "topright":
            badge_x = self.rect.right - badge_bg_width // 2
            badge_y = self.rect.top - badge_bg_height // 2
        elif self.badge_position == "bottomleft":
            badge_x = self.rect.left - badge_bg_width // 2
            badge_y = self.rect.bottom - badge_bg_height // 2
        else:  # bottomright
            badge_x = self.rect.right - badge_bg_width // 2
            badge_y = self.rect.bottom - badge_bg_height // 2

        if abs(badge_bg_width - badge_bg_height) <= 2:
            radius = max(badge_bg_width, badge_bg_height) // 2
            pygame.draw.circle(self.screen, self.badge_color, (badge_x + badge_bg_width // 2, badge_y + badge_bg_height // 2), radius)
        else:
            badge_bg_rect = pygame.Rect(badge_x, badge_y, badge_bg_width, badge_bg_height)
            pygame.draw.rect(self.screen, self.badge_color, badge_bg_rect, border_radius=badge_bg_height // 2)

        badge_text_rect = badge_surf.get_rect(center=(badge_x + badge_bg_width // 2, badge_y + badge_bg_height // 2))
        self.screen.blit(badge_surf, badge_text_rect)

    def _draw_tooltip(self) -> None:
        """Draw a tooltip when the button is hovered over."""
        if self.tooltip_alpha < 255:
            self.tooltip_alpha = min(255, self.tooltip_alpha + 15)
        tooltip_surf = self.tooltip_font.render(self.tooltip, True, (255, 255, 255))
        tooltip_rect = tooltip_surf.get_rect()
        padding = 5
        background = pygame.Surface((tooltip_rect.width + padding * 2, tooltip_rect.height + padding * 2))
        background.fill((0, 0, 0))
        background.set_alpha(min(200, self.tooltip_alpha))
        tooltip_pos = (
            self.rect.centerx - (tooltip_rect.width + padding * 2) // 2,
            self.rect.top - tooltip_rect.height - padding * 2 - 5
        )
        self.screen.blit(background, tooltip_pos)
        self.screen.blit(tooltip_surf, (tooltip_pos[0] + padding, tooltip_pos[1] + padding))

    def _animate_value(self, current: int, target: int) -> int:
        """Animate a numerical value toward a target value."""
        if current < target:
            return min(current + self.animation_speed, target)
        elif current > target:
            return max(current - self.animation_speed, target)
        return current

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events (mouse and keyboard) for the button.

        Returns True if the event caused a state change.
        """
        if self.disabled:
            return False

        result = False
        mouse_pos = pygame.mouse.get_pos()

        # Determine whether the mouse hovers over the button based on its shape.
        if self.shape == "rectangle":
            is_hovering = self.rect.collidepoint(mouse_pos)
        elif self.shape == "circle":
            center = self.rect.center
            radius = self.shape_params.get("radius", min(self.rect.width, self.rect.height) // 2)
            dx = center[0] - mouse_pos[0]
            dy = center[1] - mouse_pos[1]
            is_hovering = (dx * dx + dy * dy) <= (radius * radius)
        elif self.shape == "polygon":
            points = self.shape_params.get("points", [])
            minx = min(p[0] for p in points)
            miny = min(p[1] for p in points)
            maxx = max(p[0] for p in points)
            maxy = max(p[1] for p in points)
            bounding_rect = pygame.Rect(minx, miny, maxx - minx, maxy - miny)
            is_hovering = bounding_rect.collidepoint(mouse_pos)
            if is_hovering and len(points) > 2:
                is_hovering = self._point_in_polygon(mouse_pos, points)
        else:
            is_hovering = self.rect.collidepoint(mouse_pos)

        was_hovering = self.hovered
        self.hovered = is_hovering

        if is_hovering and not was_hovering:
            if self.hover_sound and self.sounds_loaded:
                if self.music_manager:
                    self.music_manager.play_sound(self.hover_sound)
                else:
                    self.hover_sound.play()
            result = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if is_hovering:
                self.clicked = True
                result = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.clicked and is_hovering:
                if self.click_sound and self.sounds_loaded:
                    if self.music_manager:
                        self.music_manager.play_sound(self.click_sound)
                    else:
                        self.click_sound.play()
                if self.toggle_mode:
                    if self.group:
                        for btn in self.group.buttons:
                            if btn != self:
                                btn.toggled = False
                        self.toggled = True
                        self.group.selected = self
                    else:
                        self.toggled = not self.toggled
                if self.on_click:
                    self.on_click()
                result = True
            self.clicked = False

        elif event.type == pygame.KEYDOWN:
            if self.shortcut_key and event.key == self.shortcut_key:
                if self.click_sound and self.sounds_loaded:
                    if self.music_manager:
                        self.music_manager.play_sound(self.click_sound)
                    else:
                        self.click_sound.play()
                if self.on_click:
                    self.on_click()
                result = True
            elif self.focused and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                if self.click_sound and self.sounds_loaded:
                    if self.music_manager:
                        self.music_manager.play_sound(self.click_sound)
                    else:
                        self.click_sound.play()
                if self.toggle_mode:
                    if self.group:
                        for btn in self.group.buttons:
                            if btn != self:
                                btn.toggled = False
                        self.toggled = True
                        self.group.selected = self
                    else:
                        self.toggled = not self.toggled
                if self.on_click:
                    self.on_click()
                result = True
            elif event.key == pygame.K_TAB:
                current_index = -1
                for i, btn in enumerate(Button.all_buttons):
                    if btn.focused:
                        current_index = i
                        btn.set_focus(False)
                        break
                next_index = 0
                if current_index >= 0:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        next_index = (current_index - 1) % len(Button.all_buttons)
                    else:
                        next_index = (current_index + 1) % len(Button.all_buttons)
                original_next = next_index
                while Button.all_buttons[next_index].disabled:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        next_index = (next_index - 1) % len(Button.all_buttons)
                    else:
                        next_index = (next_index + 1) % len(Button.all_buttons)
                    if next_index == original_next:
                        break
                if not Button.all_buttons[next_index].disabled:
                    Button.all_buttons[next_index].set_focus(True)
                    result = True

        return result

    def _point_in_polygon(self, point: Tuple[int, int], vertices: List[Tuple[int, int]]) -> bool:
        """
        Check if a point is inside a polygon using the ray casting algorithm.
        """
        x, y = point
        n = len(vertices)
        inside = False
        p1x, p1y = vertices[0]
        for i in range(1, n + 1):
            p2x, p2y = vertices[i % n]
            if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def set_focus(self, focused: bool) -> bool:
        """
        Set keyboard focus to this button.
        Returns True if focus was updated.
        """
        if self.disabled:
            return False

        if focused and not self.focused:
            for btn in Button.all_buttons:
                if btn != self:
                    btn.focused = False
            self.focused = True
            Button.focused_button = self
            if self.focus_sound and self.sounds_loaded:
                if self.music_manager:
                    self.music_manager.play_sound(self.focus_sound)
                else:
                    self.focus_sound.play()
            return True
        elif not focused and self.focused:
            self.focused = False
            if Button.focused_button == self:
                Button.focused_button = None
            return True
        return False

    def set_disabled(self, disabled: bool) -> None:
        """Enable or disable the button."""
        self.disabled = disabled
        if disabled and self.focused:
            self.set_focus(False)

    def set_toggle(self, toggled: bool) -> None:
        """Set the toggle state for a toggle button."""
        if self.toggle_mode:
            self.toggled = toggled

    def set_badge(self, text: str) -> None:
        """Set or update the badge text displayed on the button."""
        self.badge_text = text

    def set_tooltip(self, text: str) -> None:
        """Set or update the tooltip text for the button."""
        self.tooltip = text
        if self.translation_func and text:
            self.tooltip = self.translation_func(text)

    def set_text(self, text: str) -> None:
        """Update the button's primary text."""
        self.original_text = text
        if self.translation_func and text:
            self.text = self.translation_func(text)
        else:
            self.text = text

    def set_hover_text(self, text: str) -> None:
        """Update the button's text when hovered."""
        self.hover_text = text

    def update(self, event: Optional[pygame.event.Event] = None) -> bool:
        """
        Update the button state and draw it.

        Optionally handles an event before drawing.

        Returns:
          True if the button state (e.g., hover) changed.
        """
        if event:
            self.handle_event(event)
        self.draw()
        return self.hovered

    @classmethod
    def update_all(cls, event: Optional[pygame.event.Event] = None) -> bool:
        """
        Update all tracked buttons (and sliders) with an event.

        Returns:
          True if any button or slider state changed.
        """
        result = False
        for button in cls.all_buttons:
            if event and button.handle_event(event):
                result = True
        for slider in cls.all_sliders:
            if event and slider.handle_event(event):
                result = True
        return result

    @staticmethod
    def clear_all() -> None:
        """Clear all button and slider tracking lists."""
        Button.all_buttons.clear()
        Button.instances.clear()
        Button.focused_button = None
        Button.all_sliders.clear()


class ButtonGroup:
    """
    Group buttons together for radio-button style behavior.
    """
    def __init__(self, allow_unselect: bool = False) -> None:
        """
        Create a button group for radio-style button behavior.

        Args:
          allow_unselect: If True, clicking a selected button will deselect it.
        """
        self.buttons: List[Button] = []
        self.selected: Optional[Button] = None
        self.allow_unselect = allow_unselect

    def add(self, button: Button) -> None:
        """Add a button to this group."""
        self.buttons.append(button)
        button.group = self
        button.selected = False
        if len(self.buttons) == 1 and not self.selected:
            button.selected = True
            self.selected = button

    def get_selected(self) -> Optional[Button]:
        """Retrieve the currently selected button in the group."""
        for button in self.buttons:
            if getattr(button, 'selected', False):
                return button
        return None

    def select(self, button_id: str) -> bool:
        """
        Select a button by its ID.

        Returns:
          True if a button was successfully selected, False otherwise.
        """
        found = False
        for button in self.buttons:
            if button.id == button_id:
                button.selected = True
                self.selected = button
                found = True
            else:
                button.selected = False
        return found

    def clear_selection(self) -> bool:
        """
        Clear the current selection if allowed.

        Returns:
          True if the selection was cleared, False otherwise.
        """
        if self.allow_unselect:
            for button in self.buttons:
                button.selected = False
            self.selected = None
            return True
        return False
