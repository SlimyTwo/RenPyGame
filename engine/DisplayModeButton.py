import pygame

display_modes = ["Windowed", "Fullscreen"]
current_mode_index = 0
was_clicked = False
click_ready = False

def DisplayModeButtonFunctionality(screen, font):
    global current_mode_index, was_clicked, click_ready

    width, height = screen.get_size()
    button_rect = pygame.Rect(width // 2 - 250, height // 2 + 50, 500, 80)

    hovered = button_rect.collidepoint(pygame.mouse.get_pos())
    color = (255, 50, 50) if hovered else (255, 255, 255)

    text = f"Current Mode: {display_modes[current_mode_index]}"
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    if not pygame.mouse.get_pressed()[0]:
        click_ready = True

    if hovered and pygame.mouse.get_pressed()[0]:
        if not was_clicked and click_ready:
            was_clicked = True
            current_mode_index = (current_mode_index + 1) % len(display_modes)
            return apply_display_mode(display_modes[current_mode_index])
    elif not pygame.mouse.get_pressed()[0]:
        was_clicked = False

    return None

def apply_display_mode(mode):
    if mode == "Windowed":
        screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        pygame.display.set_caption("Fantasy Falls")
        return screen

    elif mode == "Fullscreen":
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
