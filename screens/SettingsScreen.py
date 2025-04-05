import pygame
from engine.DisplayModeButton import DisplayModeButtonFunctionality
from BackButton import BackButtonFunctionality

def ShowSettingsScreen(screen, font, original_background):
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen_width, screen_height = screen.get_size()
        scaled_background = pygame.transform.scale(original_background, (screen_width, screen_height))
        screen.blit(scaled_background, (0, 0))

        # ✅ Display Mode toggle button
        new_screen = DisplayModeButtonFunctionality(screen, font)
        if new_screen:
            screen = new_screen

        # ✅ Back button to exit settings
        if BackButtonFunctionality(screen, font):
            running = False

        pygame.display.flip()

    return screen
