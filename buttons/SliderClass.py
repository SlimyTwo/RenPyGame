import pygame


class SliderButton:
    def __init__(self, screen, font, x, y, width, height, min_value=0, max_value=100,
                 current_value=50, step=1, label=None, bg_color=(80, 80, 80),
                 hover_color=(100, 100, 150), text_color=(220, 220, 220),
                 focus_color=(120, 120, 200), disabled=False, tooltip=None,
                 sound_path=None, hover_sound_path=None, focus_sound_path=None):
        self.screen = screen
        self.font = font
        self.rect = pygame.Rect(x, y, width, height)  # Use a proper Rect object
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = max(min_value, min(max_value, current_value))  # Clamp value
        self.step = step
        self.label = label
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.focus_color = focus_color
        self.disabled = disabled
        self.tooltip = tooltip
        self.sound_path = sound_path
        self.hover_sound_path = hover_sound_path
        self.focus_sound_path = focus_sound_path

        # State tracking
        self.is_hovered = False
        self.is_dragging = False
        self.has_focus = False

        # For handling callbacks
        self.on_value_change = None

        # Initialize sounds
        self.click_sound = None
        self.hover_sound = None
        self.focus_sound = None

        if sound_path:
            try:
                self.click_sound = pygame.mixer.Sound(sound_path)
            except:
                print(f"Could not load sound: {sound_path}")

        if hover_sound_path:
            try:
                self.hover_sound = pygame.mixer.Sound(hover_sound_path)
            except:
                print(f"Could not load sound: {hover_sound_path}")

        if focus_sound_path:
            try:
                self.focus_sound = pygame.mixer.Sound(focus_sound_path)
            except:
                print(f"Could not load sound: {focus_sound_path}")

    def draw(self):
        # Draw the slider track with rounded corners
        track_color = self.focus_color if self.has_focus else self.bg_color
        if self.is_hovered and not self.disabled:
            track_color = self.hover_color

        # Draw track background
        border_radius = self.rect.height // 2
        pygame.draw.rect(self.screen, track_color, self.rect, border_radius=border_radius)

        # Calculate handle position based on current value
        value_range = self.max_value - self.min_value
        value_percent = (self.current_value - self.min_value) / value_range if value_range > 0 else 0
        handle_x = self.rect.x + int(value_percent * self.rect.width)

        # Draw handle
        handle_radius = self.rect.height - 4
        handle_color = (200, 200, 200) if not self.disabled else (150, 150, 150)
        pygame.draw.circle(self.screen, handle_color, (handle_x, self.rect.y + self.rect.height // 2),
                           handle_radius // 2)

        # Draw label if provided
        if self.label:
            label_text = self.font.render(self.label, True, self.text_color)
            label_rect = label_text.get_rect(bottomleft=(self.rect.x, self.rect.y - 5))
            self.screen.blit(label_text, label_rect)

        # Draw current value
        value_text = self.font.render(str(self.current_value), True, self.text_color)
        value_rect = value_text.get_rect(topleft=(self.rect.x, self.rect.y + self.rect.height + 5))
        self.screen.blit(value_text, value_rect)

        # Draw tooltip if hovered and tooltip exists
        if self.is_hovered and self.tooltip and not self.disabled:
            tooltip_font = pygame.font.Font(None, 24)
            tooltip_text = tooltip_font.render(self.tooltip, True, (255, 255, 255))
            tooltip_rect = tooltip_text.get_rect(midbottom=(self.rect.centerx, self.rect.top - 10))

            # Draw tooltip background
            padding = 5
            bg_rect = tooltip_rect.inflate(padding * 2, padding * 2)
            pygame.draw.rect(self.screen, (50, 50, 50), bg_rect, border_radius=5)
            self.screen.blit(tooltip_text, tooltip_rect)

    def handle_event(self, event):
        if self.disabled:
            return False

        handled = False
        mouse_pos = pygame.mouse.get_pos()

        # Check for hover state
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Play hover sound when first hovering
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

        # Handle keyboard focus for accessibility
        elif event.type == pygame.KEYDOWN and self.has_focus:
            if event.key == pygame.K_LEFT:
                self.adjust_value(-self.step if self.step else -1)
                handled = True
            elif event.key == pygame.K_RIGHT:
                self.adjust_value(self.step if self.step else 1)
                handled = True

        return handled

    def update_value(self, x_pos):
        # Calculate the new value based on mouse x position
        value_range = self.max_value - self.min_value
        slider_width = self.rect.width
        relative_x = max(0, min(slider_width, x_pos - self.rect.x))
        new_value = self.min_value + (relative_x / slider_width) * value_range

        # Apply step if specified
        if self.step:
            new_value = round(new_value / self.step) * self.step

        # Update value if changed
        if new_value != self.current_value:
            self.current_value = round(max(self.min_value, min(self.max_value, new_value)))
            if self.on_value_change:
                self.on_value_change(self.current_value)

    def adjust_value(self, amount):
        # Adjust value by amount, respecting min/max bounds
        new_value = max(self.min_value, min(self.max_value, self.current_value + amount))
        if new_value != self.current_value:
            self.current_value = new_value
            if self.on_value_change:
                self.on_value_change(self.current_value)

    def set_focus(self, focus):
        # Update focus state and play sound if gaining focus
        if focus and not self.has_focus and self.focus_sound:
            self.focus_sound.play()
        self.has_focus = focus