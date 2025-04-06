import pygame
import os
from buttons.ButtonClass import Button
from buttons.ButtonCreator import create_button

# Colors
BACKGROUND = (40, 44, 52)
TEXT_COLOR = (220, 220, 220)
HOVER_COLOR = (100, 100, 150, 180)  # Semi-transparent hover color

# Sound files paths
click_sound_path = os.path.join("assets", "audio", "click.wav")
hover_sound_path = os.path.join("assets", "audio", "hover.wav")
focus_sound_path = os.path.join("assets", "audio", "focus.wav")


def RunMainMenuLoop():
    # Get the screen that was already created
    screen = pygame.display.get_surface()
    screen_width, screen_height = screen.get_size()
    clock = pygame.time.Clock()
    running = True

    # Load fonts
    button_font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 24)

    # Check if sound files exist
    sound_path = click_sound_path if os.path.exists(click_sound_path) else None
    hover_sound = hover_sound_path if os.path.exists(hover_sound_path) else None

    # Create main menu buttons (vertically aligned)
    button_width = 250
    button_height = 50
    button_spacing = 20

    # Start Game button
    start_game_btn = create_button(
        screen, button_font, width=button_width, height=button_height,
        y_offset=-100, text="Start Game",
        hover_text="▶ Start Game ▶",  # Text when hovering
        tooltip="Start a new game", sound_path=sound_path,
        hover_sound_path=hover_sound,
        visible_background=False,
        debug_hitbox=True
    )

    # Load Game button (greyed out)
    load_game_btn = create_button(
        screen, button_font, width=button_width, height=button_height,
        y_offset=-100 + button_height + button_spacing,
        text="Load Game",
        hover_text="Load Game (Unavailable)",  # Text when hovering
        tooltip="Load a saved game",
        visible_background=False,
        debug_hitbox=True,
        disabled=True
    )

    # Settings button
    settings_btn = create_button(
        screen, button_font, width=button_width, height=button_height,
        y_offset=-100 + (button_height + button_spacing) * 2,
        text="Settings",
        hover_text="⚙ Settings ⚙",  # Text when hovering
        tooltip="Game settings",
        sound_path=sound_path,
        hover_sound_path=hover_sound,
        visible_background=False,
        debug_hitbox=True
    )

    # Quit button
    quit_btn = create_button(
        screen, button_font, width=button_width, height=button_height,
        y_offset=-100 + (button_height + button_spacing) * 3,
        text="Quit",
        hover_text="✖ Exit Game ✖",  # Text when hovering
        tooltip="Exit the game",
        sound_path=sound_path,
        hover_sound_path=hover_sound,
        visible_background=False,
        debug_hitbox=True
    )

    # Button handlers
    def handle_start_game():
        # Start new game logic would go here
        return True

    def handle_settings():
        # Open settings menu logic would go here
        return True

    def handle_quit():
        nonlocal running
        running = False
        return True

    start_game_btn.on_click = handle_start_game
    settings_btn.on_click = handle_settings
    quit_btn.on_click = handle_quit

    # Ensure the first button has focus initially for keyboard navigation
    start_game_btn.set_focus(True)

    # Load background image
    try:
        bg_path = os.path.join("assets", "images", "MainMenuBackground.png")
        if os.path.exists(bg_path):
            original_bg = pygame.image.load(bg_path)
            # Get original image dimensions
            bg_width, bg_height = original_bg.get_size()

            # Calculate scaling factor to fill the screen
            width_ratio = screen_width / bg_width
            height_ratio = screen_height / bg_height
            scale_factor = max(width_ratio, height_ratio)

            # Calculate new dimensions
            new_width = int(bg_width * scale_factor)
            new_height = int(bg_height * scale_factor)

            # Scale the image with the calculated dimensions
            background_image = pygame.transform.scale(original_bg, (new_width, new_height))

            # Calculate position to center the image
            bg_x = (screen_width - new_width) // 2
            bg_y = (screen_height - new_height) // 2

            # Store position with the image
            bg_pos = (bg_x, bg_y)
        else:
            background_image = None
            bg_pos = (0, 0)
    except:
        background_image = None
        bg_pos = (0, 0)

    # Main game loop
    while running:
        # Draw background
        if background_image:
            screen.fill(BACKGROUND)  # Fill with background color first
            screen.blit(background_image, bg_pos)  # Draw the centered image
        else:
            screen.fill(BACKGROUND)

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle button events
            Button.update_all(event)

            # Global keyboard shortcut
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

        # Draw all buttons
        start_game_btn.draw()
        load_game_btn.draw()
        settings_btn.draw()
        quit_btn.draw()

        # Draw instructions
        instructions = small_font.render("Press TAB to navigate, ENTER to select, Q to quit", True, TEXT_COLOR)
        screen.blit(instructions, (screen_width // 2 - instructions.get_width() // 2, screen_height - 40))

        pygame.display.flip()
        clock.tick(60)