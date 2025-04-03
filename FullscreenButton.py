import pygame

fullscreen_button_rect = pygame.Rect(0, 0, 200, 80)  # Will be repositioned each frame
was_clicked = False
click_ready = False

def FullscreenButtonFunctionality(screen, font):
    global was_clicked, click_ready

    width, height = screen.get_size()
    fullscreen_button_rect.center = (width // 2, height // 2)

    mouse = pygame.mouse
    hovered = fullscreen_button_rect.collidepoint(mouse.get_pos())
    color = (255, 50, 50) if hovered else (255, 255, 255)

    text_surface = font.render("Toggle Fullscreen", True, color)
    text_rect = text_surface.get_rect(center=fullscreen_button_rect.center)
    screen.blit(text_surface, text_rect)

    if not mouse.get_pressed()[0]:
        click_ready = True

    if hovered and mouse.get_pressed()[0]:
        if not was_clicked and click_ready:
            was_clicked = True
            return toggle_fullscreen(screen)
    elif not mouse.get_pressed()[0]:
        was_clicked = False

    return None

def toggle_fullscreen(screen):
    if screen.get_flags() & pygame.FULLSCREEN:
        return pygame.display.set_mode((1280, 720))
    else:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

def ResetFullscreenClickState():
    global click_ready
    click_ready = False
