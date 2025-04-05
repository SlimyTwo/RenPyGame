import pygame

back_button_rect = pygame.Rect(20, 20, 120, 50)
was_clicked = False

def BackButtonFunctionality(screen, font):
    global was_clicked

    hovered = back_button_rect.collidepoint(pygame.mouse.get_pos())
    color = (255, 50, 50) if hovered else (255, 255, 255)

    text_surface = font.render("← Back", True, color)
    text_rect = text_surface.get_rect(center=back_button_rect.center)
    screen.blit(text_surface, text_rect)

    if hovered and pygame.mouse.get_pressed()[0]:
        if not was_clicked:
            was_clicked = True
            return True
    elif not pygame.mouse.get_pressed()[0]:
        was_clicked = False

    return False
