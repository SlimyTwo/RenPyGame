import pygame
from typing import Callable, Tuple, Optional, Union


class Button:
    # Class variable for the sound - loaded once for all buttons
    click_sound = None

    def __init__(self, rect, text, button_id, screen, font, on_click,
                 bg_color=(100, 100, 100), hover_color=(150, 150, 150), text_color=(255, 255, 255),
                 border_color=(30, 30, 30), sound_path="assets/audio/click.wav",
                 visible_background=True, debug_hitbox=False, debug_color=(255, 0, 0),
                 icon=None, tooltip=None, tooltip_font=None, disabled=False,
                 disabled_color=(80, 80, 80), disabled_text_color=(150, 150, 150),
                 animation_speed=5, group=None):
        """
        Initialize a button with position, size, and behavior.

        Args:
            rect: pygame.Rect for button position and size
            text: Text to display on button
            button_id: Unique identifier for the button
            screen: pygame surface to draw on
            font: pygame font for text
            on_click: Function to call when button is clicked
            bg_color: Button background color (RGB tuple)
            hover_color: Button color when hovered (RGB tuple)
            text_color: Text color (RGB tuple)
            border_color: Color of button border (RGB tuple)
            sound_path: Path to the click sound file
            visible_background: Whether to draw the button background
            debug_hitbox: Whether to display a thin outline showing the button's hitbox
            debug_color: Color for the debug hitbox outline
            icon: Optional pygame Surface to display as an icon
            tooltip: Optional text to display when hovering
            tooltip_font: Font for tooltip text (uses button font if None)
            disabled: Whether the button is disabled
            disabled_color: Background color when disabled
            disabled_text_color: Text color when disabled
            animation_speed: Speed of hover/click animations (higher is faster)
            group: Optional button group this button belongs to
        """
        self.rect = rect
        self.text = text
        self.id = button_id
        self.screen = screen
        self.font = font
        self.on_click = on_click
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.hovered = False
        self.visible_background = visible_background
        self.debug_hitbox = debug_hitbox
        self.debug_color = debug_color

        # New features
        self.icon = icon
        self.tooltip = tooltip
        self.tooltip_font = tooltip_font or font
        self.disabled = disabled
        self.disabled_color = disabled_color
        self.disabled_text_color = disabled_text_color
        self.animation_speed = animation_speed
        self.group = group
        self.current_color = bg_color
        self.clicked = False
        self.tooltip_visible = False
        self.tooltip_alpha = 0

        # Load the sound if not already loaded
        if Button.click_sound is None and sound_path:
            try:
                Button.click_sound = pygame.mixer.Sound(sound_path)
            except pygame.error:
                print(f"Warning: Could not load sound file: {sound_path}")
                Button.click_sound = None

    def handle_event(self, event):
        """Process pygame events for this button"""
        if self.disabled:
            return False

        mouse_pos = pygame.mouse.get_pos()
        old_hovered = self.hovered
        self.hovered = self.rect.collidepoint(mouse_pos)

        # Handle tooltip visibility
        if self.hovered and not old_hovered and self.tooltip:
            self.tooltip_visible = True
        elif not self.hovered and old_hovered and self.tooltip:
            self.tooltip_visible = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            self.clicked = True
            # Play click sound
            if Button.click_sound:
                Button.click_sound.play()

            if self.on_click:
                result = self.on_click()

                # Handle button groups (radio button behavior)
                if self.group:
                    for button in self.group.buttons:
                        if button != self:
                            button.selected = False
                    self.selected = True

                return result
            return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False

        return False

    def draw(self):
        """Draw the button on the screen"""
        # Determine the correct color based on state
        if self.disabled:
            target_color = self.disabled_color
        elif self.clicked and self.hovered:
            # Darker when clicked
            r = max(0, self.hover_color[0] - 30)
            g = max(0, self.hover_color[1] - 30)
            b = max(0, self.hover_color[2] - 30)
            target_color = (r, g, b)
        elif self.hovered:
            target_color = self.hover_color
        else:
            target_color = self.bg_color

        # Smooth color transition animation
        if self.current_color != target_color:
            r = self._animate_value(self.current_color[0], target_color[0])
            g = self._animate_value(self.current_color[1], target_color[1])
            b = self._animate_value(self.current_color[2], target_color[2])
            self.current_color = (r, g, b)

        # Draw button background if visible
        if self.visible_background:
            pygame.draw.rect(self.screen, self.current_color, self.rect, border_radius=5)
            pygame.draw.rect(self.screen, self.border_color, self.rect, 2, border_radius=5)
        elif self.debug_hitbox:
            # If background is invisible but debug is on, show the hitbox
            pygame.draw.rect(self.screen, self.debug_color, self.rect, 1, border_radius=5)

        # Always draw debug outline if enabled and background is visible
        if self.debug_hitbox and self.visible_background:
            pygame.draw.rect(self.screen, self.debug_color, self.rect, 1, border_radius=5)

        # Determine text color based on disabled state
        text_color = self.disabled_text_color if self.disabled else self.text_color

        # Calculate positions for icon and text
        if self.icon:
            # If we have an icon, position it and the text side by side
            icon_rect = self.icon.get_rect()
            total_width = icon_rect.width + 10 + self.font.size(self.text)[0]

            icon_x = self.rect.centerx - total_width // 2
            icon_y = self.rect.centery - icon_rect.height // 2

            text_surf = self.font.render(self.text, True, text_color)
            text_rect = text_surf.get_rect(midleft=(icon_x + icon_rect.width + 10, self.rect.centery))

            # Draw the icon and text
            self.screen.blit(self.icon, (icon_x, icon_y))
            self.screen.blit(text_surf, text_rect)
        else:
            # Just draw the text centered
            text_surf = self.font.render(self.text, True, text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            self.screen.blit(text_surf, text_rect)

        # Draw tooltip if needed
        if self.tooltip_visible and self.tooltip:
            self._draw_tooltip()

    def _animate_value(self, current, target):
        """Animate a single value toward a target"""
        if current < target:
            return min(current + self.animation_speed, target)
        elif current > target:
            return max(current - self.animation_speed, target)
        return current

    def _draw_tooltip(self):
        """Draw tooltip when hovering"""
        if self.tooltip_alpha < 255:
            self.tooltip_alpha = min(255, self.tooltip_alpha + 15)

        tooltip_surf = self.tooltip_font.render(self.tooltip, True, (255, 255, 255))
        tooltip_rect = tooltip_surf.get_rect()
        padding = 5

        # Create background surface with alpha
        background = pygame.Surface((tooltip_rect.width + padding * 2, tooltip_rect.height + padding * 2))
        background.fill((0, 0, 0))
        background.set_alpha(min(200, self.tooltip_alpha))

        # Position tooltip above the button
        tooltip_pos = (
            self.rect.centerx - (tooltip_rect.width + padding * 2) // 2,
            self.rect.top - tooltip_rect.height - padding * 2 - 5
        )

        # Draw tooltip background and text
        self.screen.blit(background, tooltip_pos)
        self.screen.blit(tooltip_surf, (tooltip_pos[0] + padding, tooltip_pos[1] + padding))

    def set_disabled(self, disabled):
        """Enable or disable the button"""
        self.disabled = disabled

    def update(self, event=None):
        """Update and draw the button in one call"""
        if event:
            self.handle_event(event)
        self.draw()
        return self.hovered


class ButtonGroup:
    """Group buttons together for radio-button style behavior"""

    def __init__(self, allow_unselect=False):
        self.buttons = []
        self.selected = None
        self.allow_unselect = allow_unselect

    def add(self, button):
        """Add a button to this group"""
        self.buttons.append(button)
        button.group = self
        button.selected = False

    def get_selected(self):
        """Get the currently selected button"""
        for button in self.buttons:
            if getattr(button, 'selected', False):
                return button
        return None