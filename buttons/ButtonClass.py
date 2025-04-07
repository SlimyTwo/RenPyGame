import pygame


class Button:
    """A versatile button class for pygame interfaces with advanced features"""

    all_buttons = []  # Track all button instances for keyboard navigation

    def __init__(self, rect, text, button_id, screen, font, on_click=None,
                 bg_color=(100, 100, 100), hover_color=(150, 150, 150),
                 text_color=(255, 255, 255), hover_text_color=None, border_color=(200, 200, 200),
                 border_width=1, visible_background=True,
                 debug_hitbox=False, debug_color=(255, 0, 0),
                 icon=None, tooltip=None, disabled=False,
                 sound_path=None, hover_sound_path=None, focus_sound_path=None,
                 text_align="center", shape="rectangle", shape_params=None,
                 badge_text=None, badge_color=(255, 0, 0), badge_position="topright",
                 shortcut_key=None, toggle_mode=False, toggled=False, toggle_color=(160, 160, 200),
                 focus_color=(200, 200, 255), focus_border_color=(100, 100, 255),
                 translation_func=None, animation_speed=5, hover_text=None):
        """Initialize a new button"""
        self.rect = rect
        self.original_text = text
        self.hover_text = hover_text or text  # New parameter for text when hovering
        self.text = text
        self.id = button_id
        self.screen = screen
        self.font = font
        self.on_click = on_click
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hover_text_color = hover_text_color or text_color  # Added hover text color
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
        self.hovered = False
        self.clicked = False
        self.focused = False

        # Animation state
        self.hover_alpha = 0
        self.tooltip_alpha = 0
        self.click_effect = 0

        # Advanced features
        self.tooltip_font = pygame.font.Font(None, 20)  # Smaller font for tooltip
        self.sound_path = sound_path
        self.hover_sound_path = hover_sound_path
        self.focus_sound_path = focus_sound_path
        self.sounds_loaded = False
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
        self.group = None

        # Add to global button list for keyboard navigation
        Button.all_buttons.append(self)

        # Load sounds if paths are provided
        self._load_sounds()

    def _load_sounds(self):
        """Load sound effects if pygame mixer is available"""
        if not pygame.mixer.get_init():
            return

        try:
            self.click_sound = None
            self.hover_sound = None
            self.focus_sound = None

            if self.sound_path:
                self.click_sound = pygame.mixer.Sound(self.sound_path)
                self.click_sound.set_volume(0.5)

            if self.hover_sound_path:
                self.hover_sound = pygame.mixer.Sound(self.hover_sound_path)
                self.hover_sound.set_volume(0.3)

            if self.focus_sound_path:
                self.focus_sound = pygame.mixer.Sound(self.focus_sound_path)
                self.focus_sound.set_volume(0.3)

            self.sounds_loaded = True
        except Exception as e:
            print(f"Error loading sounds: {e}")

    def draw(self):
        """Draw the button on the screen"""
        if self.disabled:
            # Use darker colors for disabled state
            bg_color = tuple(max(0, c - 50) for c in self.bg_color)
            border_color = tuple(max(0, c - 50) for c in self.border_color)
            text_color = tuple(max(0, c - 100) for c in self.text_color)
        elif self.toggled and self.toggle_mode:
            # Use toggle colors for toggled state
            bg_color = self.toggle_color
            border_color = self.border_color
            text_color = self.text_color
        elif self.focused:
            # Use focus colors when keyboard focused
            bg_color = self.focus_color
            border_color = self.focus_border_color
            text_color = self.text_color
        elif self.hovered:
            # Use hover colors when mouse is over button
            bg_color = self.hover_color
            border_color = self.border_color
            text_color = self.hover_text_color  # Use hover text color when hovering
        else:
            # Use normal colors
            bg_color = self.bg_color
            border_color = self.border_color
            text_color = self.text_color

        # Draw button background based on shape
        if self.visible_background:
            if self.shape == "rectangle":
                # Standard rectangular button
                pygame.draw.rect(self.screen, bg_color, self.rect, border_radius=5)
                if self.border_width > 0:
                    pygame.draw.rect(self.screen, border_color, self.rect,
                                     width=self.border_width, border_radius=5)
            elif self.shape == "circle":
                # Circular button
                radius = self.shape_params.get("radius", min(self.rect.width, self.rect.height) // 2)
                center = self.rect.center
                pygame.draw.circle(self.screen, bg_color, center, radius)
                if self.border_width > 0:
                    pygame.draw.circle(self.screen, border_color, center,
                                       radius, width=self.border_width)
            elif self.shape == "polygon":
                # Polygon button (e.g., triangle)
                points = self.shape_params.get("points", [])
                if points:
                    pygame.draw.polygon(self.screen, bg_color, points)
                    if self.border_width > 0:
                        pygame.draw.polygon(self.screen, border_color,
                                            points, width=self.border_width)

        # Draw debug hitbox if requested
        if self.show_hitbox:
            if isinstance(self.hitbox_color, tuple) and len(self.hitbox_color) >= 3:
                # Convert RGB to RGBA if needed
                if len(self.hitbox_color) == 3:
                    hitbox_color = self.hitbox_color + (100,)  # Add alpha channel
                else:
                    hitbox_color = self.hitbox_color

                # Draw semi-transparent hitbox outline
                hitbox_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                pygame.draw.rect(hitbox_surface, hitbox_color,
                                 hitbox_surface.get_rect(), width=1, border_radius=5)
                self.screen.blit(hitbox_surface, self.rect)

        # Determine which text to use (hover text or original)
        current_text = self.hover_text if self.hovered else self.original_text

        # Draw text with appropriate color and alignment
        self._draw_text(current_text, text_color)

        # Draw icon if provided
        if self.icon:
            icon_rect = self.icon.get_rect(center=self.rect.center)
            # Adjust icon position based on text alignment
            if self.text:
                if self.text_align == "left":
                    icon_rect.left = self.rect.left + 10
                    self.screen.blit(self.icon, icon_rect)
                elif self.text_align == "right":
                    icon_rect.right = self.rect.right - 10
                    self.screen.blit(self.icon, icon_rect)
                else:  # center or default
                    # Place icon to the left of text
                    icon_rect.centerx = self.rect.centerx - len(self.text) * 4
                    self.screen.blit(self.icon, icon_rect)
            else:
                # If no text, center the icon
                self.screen.blit(self.icon, icon_rect)

        # Draw badge if needed
        if self.badge_text:
            self._draw_badge()

        # Draw tooltip if hovering
        if self.hovered and self.tooltip:
            self._draw_tooltip()

    def _draw_text(self, text, text_color):
        """Draw text on the button, handling multiline text with alignment"""
        if not text:
            return

        # Handle multiline text by splitting on newlines
        lines = text.split('\n')
        line_spacing = 2

        # Measure total text height
        total_height = sum(self.font.size(line)[1] for line in lines) + (line_spacing * (len(lines) - 1))

        # Initial Y position (centered vertically)
        y = self.rect.centery - total_height // 2

        for line in lines:
            text_surf = self.font.render(line, True, text_color)
            text_rect = text_surf.get_rect()

            # Align text horizontally based on setting
            if self.text_align == "left":
                text_rect.left = self.rect.left + 10
            elif self.text_align == "right":
                text_rect.right = self.rect.right - 10
            else:  # center or default
                text_rect.centerx = self.rect.centerx

            text_rect.y = y
            self.screen.blit(text_surf, text_rect)

            # Move down for next line
            y += text_rect.height + line_spacing

    def _draw_badge(self):
        """Draw notification badge on button"""
        # Render badge text
        badge_font = pygame.font.Font(None, 20)  # Smaller font for badge
        badge_surf = badge_font.render(str(self.badge_text), True, (255, 255, 255))
        badge_rect = badge_surf.get_rect()

        # Size badge background to fit text with padding
        padding = 4
        badge_bg_width = max(badge_rect.width + padding * 2,
                             badge_rect.height + padding)  # Make it at least as wide as it is tall
        badge_bg_height = badge_rect.height + padding

        # Determine badge position based on setting
        if self.badge_position == "topleft":
            badge_x, badge_y = self.rect.left - badge_bg_width // 2, self.rect.top - badge_bg_height // 2
        elif self.badge_position == "topright":
            badge_x, badge_y = self.rect.right - badge_bg_width // 2, self.rect.top - badge_bg_height // 2
        elif self.badge_position == "bottomleft":
            badge_x, badge_y = self.rect.left - badge_bg_width // 2, self.rect.bottom - badge_bg_height // 2
        else:  # bottomright
            badge_x, badge_y = self.rect.right - badge_bg_width // 2, self.rect.bottom - badge_bg_height // 2

        # Draw badge background (circle if square enough, else rounded rect)
        if abs(badge_bg_width - badge_bg_height) <= 2:
            # Nearly square, use a circle
            radius = max(badge_bg_width, badge_bg_height) // 2
            pygame.draw.circle(self.screen, self.badge_color,
                               (badge_x + badge_bg_width // 2, badge_y + badge_bg_height // 2), radius)
        else:
            # Rectangular, use rounded rect
            badge_bg_rect = pygame.Rect(badge_x, badge_y, badge_bg_width, badge_bg_height)
            pygame.draw.rect(self.screen, self.badge_color, badge_bg_rect, border_radius=badge_bg_height // 2)

        # Draw badge text centered on badge
        badge_text_rect = badge_surf.get_rect(center=(badge_x + badge_bg_width // 2, badge_y + badge_bg_height // 2))
        self.screen.blit(badge_surf, badge_text_rect)

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

    def _animate_value(self, current, target):
        """Animate a single value toward a target"""
        if current < target:
            return min(current + self.animation_speed, target)
        elif current > target:
            return max(current - self.animation_speed, target)
        return current

    def handle_event(self, event):
        """Handle pygame events for the button"""
        if self.disabled:
            return False

        result = False
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is over the button based on shape
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
            # Simple bounding box check first for optimization
            minx = min(p[0] for p in points)
            miny = min(p[1] for p in points)
            maxx = max(p[0] for p in points)
            maxy = max(p[1] for p in points)
            bounding_rect = pygame.Rect(minx, miny, maxx - minx, maxy - miny)
            is_hovering = bounding_rect.collidepoint(mouse_pos)

            # More accurate polygon check if bounding box hit
            if is_hovering and len(points) > 2:
                is_hovering = self._point_in_polygon(mouse_pos, points)
        else:
            # Default to rectangle
            is_hovering = self.rect.collidepoint(mouse_pos)

        # Handle hover state change
        was_hovering = self.hovered
        self.hovered = is_hovering

        if is_hovering and not was_hovering:
            # Just started hovering
            if self.hover_sound and self.sounds_loaded:
                self.hover_sound.play()
            result = True

        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if is_hovering:
                self.clicked = True
                result = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.clicked and is_hovering:
                # Successful click
                if self.click_sound and self.sounds_loaded:
                    self.click_sound.play()

                if self.toggle_mode:
                    # Toggle on/off if it's a toggle button
                    if self.group:
                        # Radio button behavior in group
                        for btn in self.group.buttons:
                            if btn != self:
                                btn.toggled = False
                        self.toggled = True
                        self.group.selected = self
                    else:
                        # Normal toggle behavior
                        self.toggled = not self.toggled

                # Call the click handler if provided
                if self.on_click:
                    self.on_click()

                result = True

            self.clicked = False

        # Handle keyboard events
        elif event.type == pygame.KEYDOWN:
            # Shortcut key
            if self.shortcut_key and event.key == self.shortcut_key:
                if self.click_sound and self.sounds_loaded:
                    self.click_sound.play()

                if self.on_click:
                    self.on_click()
                result = True

            # Enter key for focused button
            elif self.focused and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                if self.click_sound and self.sounds_loaded:
                    self.click_sound.play()

                if self.toggle_mode:
                    # Toggle on/off if it's a toggle button
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

            # Tab key navigation
            elif event.key == pygame.K_TAB:
                # Find current focused button
                current_index = -1
                for i, btn in enumerate(Button.all_buttons):
                    if btn.focused:
                        current_index = i
                        btn.set_focus(False)
                        break

                # Move to next or previous button
                next_index = 0
                if current_index >= 0:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:  # Shift+Tab = backward
                        next_index = (current_index - 1) % len(Button.all_buttons)
                    else:  # Tab = forward
                        next_index = (current_index + 1) % len(Button.all_buttons)

                # Skip disabled buttons
                original_next = next_index
                while Button.all_buttons[next_index].disabled:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        next_index = (next_index - 1) % len(Button.all_buttons)
                    else:
                        next_index = (next_index + 1) % len(Button.all_buttons)

                    # If we've checked all buttons and they're all disabled, stop
                    if next_index == original_next:
                        break

                # Set focus on the next button if not disabled
                if not Button.all_buttons[next_index].disabled:
                    Button.all_buttons[next_index].set_focus(True)
                    result = True

        return result

    def _point_in_polygon(self, point, vertices):
        """Check if a point is inside a polygon using the ray casting algorithm"""
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

    def set_focus(self, focused):
        """Set keyboard focus to this button"""
        if self.disabled:
            return False

        if focused and not self.focused:
            # Remove focus from all other buttons
            for btn in Button.all_buttons:
                if btn != self:
                    btn.focused = False

            # Set focus on this button
            self.focused = True
            if self.focus_sound and self.sounds_loaded:
                self.focus_sound.play()
            return True
        elif not focused and self.focused:
            self.focused = False
            return True

        return False

    def set_disabled(self, disabled):
        """Enable or disable the button"""
        self.disabled = disabled
        if disabled and self.focused:
            self.set_focus(False)

    def set_toggle(self, toggled):
        """Set the toggle state if this is a toggle button"""
        if self.toggle_mode:
            self.toggled = toggled

    def set_badge(self, text):
        """Set or update the badge text"""
        self.badge_text = text

    def set_tooltip(self, text):
        """Set or update tooltip text"""
        self.tooltip = text
        if self.translation_func and text:
            self.tooltip = self.translation_func(text)

    def set_text(self, text):
        """Update button text"""
        self.original_text = text
        if self.translation_func and text:
            self.text = self.translation_func(text)
        else:
            self.text = text

    def set_hover_text(self, text):
        """Set the text to display when hovering"""
        self.hover_text = text

    def update(self, event=None):
        """Update and draw the button in one call"""
        if event:
            self.handle_event(event)
        self.draw()
        return self.hovered

    @classmethod
    def update_all(cls, event=None):
        """Update all buttons in one call - useful for keyboard navigation"""
        result = False
        for button in cls.all_buttons:
            if event and button.handle_event(event):
                result = True
        return result


class ButtonGroup:
    """Group buttons together for radio-button style behavior"""

    def __init__(self, allow_unselect=False):
        """
        Create a button group for radio-style behavior

        Args:
            allow_unselect: If True, clicking a selected button will deselect it
        """
        self.buttons = []
        self.selected = None
        self.allow_unselect = allow_unselect

    def add(self, button):
        """Add a button to this group"""
        self.buttons.append(button)
        button.group = self
        button.selected = False

        # Set first button as selected by default
        if len(self.buttons) == 1 and not self.selected:
            button.selected = True
            self.selected = button

    def get_selected(self):
        """Get the currently selected button"""
        for button in self.buttons:
            if getattr(button, 'selected', False):
                return button
        return None

    def select(self, button_id):
        """Select a button by its ID"""
        found = False
        for button in self.buttons:
            if button.id == button_id:
                button.selected = True
                self.selected = button
                found = True
            else:
                button.selected = False
        return found

    def clear_selection(self):
        """Clear the current selection if allow_unselect is True"""
        if self.allow_unselect:
            for button in self.buttons:
                button.selected = False
            self.selected = None
            return True
        return False