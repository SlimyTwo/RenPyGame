import pygame

def draw_button_text(screen, font, text, center_pos, hovered, base_color=(255, 255, 255), hover_color=(255, 50, 50)):
    color = hover_color if hovered else base_color
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center_pos)
    screen.blit(text_surface, text_rect)
