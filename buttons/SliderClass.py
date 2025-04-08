import pygame
from buttons.ButtonClass import Button


class SliderButton(Button):
    def __init__(self, screen, font, x=0, y=0, width=200, height=30,
                 min_value=0, max_value=100, current_value=50,
                 step=1, label=None, **kwargs):
        super().__init__(screen, font, pygame.Rect(x, y, width, height),
                         "", f"slider_{width}_{height}", **kwargs)

        self.min_value = min_value
        self.max_value = max_value
        self.current_value = current_value
        self.step = step
        self.dragging = False
        self.on_value_change = None  # Callback when value changes
        self.label = label

    def handle_event(self, event):
        if self.disabled:
            return False

        result = super().handle_event(event)

        # Handle dragging behavior
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_value_from_mouse(event.pos[0])
                return True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value_from_mouse(event.pos[0])
            return True

        return result

    def update_value_from_mouse(self, x_pos):
        # Calculate relative position (0.0 to 1.0)
        rel_x = max(0, min(1, (x_pos - self.rect.left) / self.rect.width))
        # Convert to actual value
        new_value = self.min_value + rel_x * (self.max_value - self.min_value)
        # Apply step if needed
        if self.step > 0:
            new_value = round(new_value / self.step) * self.step

        if new_value != self.current_value:
            self.current_value = new_value
            if self.on_value_change:
                self.on_value_change(self.current_value)

    def draw(self):
        # Draw slider track
        pygame.draw.rect(self.screen, (80, 80, 80), self.rect, border_radius=self.rect.height // 2)

        # Draw filled portion
        progress = (self.current_value - self.min_value) / (self.max_value - self.min_value)
        filled_width = int(self.rect.width * progress)
        filled_rect = pygame.Rect(self.rect.left, self.rect.top, filled_width, self.rect.height)

        # Determine color based on state
        if self.disabled:
            fill_color = (100, 100, 100)
        elif self.focused:
            fill_color = self.focus_color
        elif self.hovered or self.dragging:
            fill_color = self.hover_color
        else:
            fill_color = self.bg_color

        pygame.draw.rect(self.screen, fill_color, filled_rect, border_radius=self.rect.height // 2)

        # Draw slider position indicator (thumb)
        thumb_x = self.rect.left + filled_width
        thumb_radius = self.rect.height // 2 + 2
        pygame.draw.circle(self.screen, (220, 220, 220), (thumb_x, self.rect.centery), thumb_radius)

        # Draw value text to the right
        value_text = self.font.render(f"{int(self.current_value)}", True, self.text_color)
        self.screen.blit(value_text, (self.rect.right + 10, self.rect.centery - value_text.get_height() // 2))

        # Draw label text if provided
        if self.label:
            label_text = self.font.render(self.label, True, self.text_color)
            self.screen.blit(label_text, (self.rect.left, self.rect.top - label_text.get_height() - 5))

    def get_value(self):
        return self.current_value

    def set_value(self, value):
        self.current_value = max(self.min_value, min(self.max_value, value))
        if self.on_value_change:
            self.on_value_change(self.current_value)