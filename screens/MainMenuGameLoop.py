import pygame
import os
from buttons.ButtonClass import Button
from buttons.ButtonCreator import create_button

# Colors
BACKGROUND = (40, 44, 52)
TEXT_COLOR = (220, 220, 220)
HOVER_COLOR = (100, 100, 150, 180)
HOVER_TEXT_COLOR = (255, 255, 0)

# Sound files paths
click_sound_path = os.path.join("assets", "audio", "click.wav")
hover_sound_path = os.path.join("assets", "audio", "hover.wav")
focus_sound_path = os.path.join("assets", "audio", "focus.wav")


def RunSettingsMenuLoop():
    # Get the screen that was already created
    screen = pygame.display.get_surface()
    screen_width, screen_height = screen.get_size()
    clock = pygame.time.Clock()
    running = True

    # Load fonts
    button_font = pygame.font.Font(None, 32)
    title_font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 24)

    # Check if sound files exist
    sound_path = click_sound_path if os.path.exists(click_sound_path) else None
    hover_sound = hover_sound_path if os.path.exists(hover_sound_path) else None

    # Initialize button variables
    back_btn = None
    fullscreen_btn = None

    # Store original background image
    original_bg = None
    background_image = None
    bg_pos = (0, 0)

    # Get current fullscreen state
    is_fullscreen = screen.get_flags() & pygame.FULLSCREEN

    # Function to load and scale background image
    def load_background_image():
        nonlocal background_image, bg_pos, original_bg, screen_width, screen_height

        # Update screen dimensions
        screen_width, screen_height = screen.get_size()

        try:
            bg_path = os.path.join("assets", "images", "MainMenuBackground.png")

            # Load original image only once
            if original_bg is None and os.path.exists(bg_path):
                original_bg = pygame.image.load(bg_path)

            if original_bg:
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
        except Exception as e:
            print(f"Error loading background: {e}")
            background_image = None
            bg_pos = (0, 0)

    # Function to recreate and reposition buttons
    def recreate_buttons():
        nonlocal back_btn, fullscreen_btn

        # Back button in top left
        back_btn = create_button(
            screen, button_font, width=120, height=40,
            x_offset=-screen_width//2 + 80, y_offset=-screen_height//2 + 40,
            text="← Back",
            hover_text="← Return",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Return to main menu",
            sound_path=sound_path,
            hover_sound_path=hover_sound,
            visible_background=True
        )

        # Fullscreen toggle button
        fullscreen_text = "Fullscreen: ON" if is_fullscreen else "Fullscreen: OFF"
        fullscreen_btn = create_button(
            screen, button_font, width=250, height=50,
            y_offset=0, text=fullscreen_text,
            hover_text="Toggle Fullscreen Mode",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Switch between windowed and fullscreen modes",
            sound_path=sound_path,
            hover_sound_path=hover_sound,
            toggle_mode=True,
            toggled=is_fullscreen
        )

        # Button handlers
        back_btn.on_click = handle_back
        fullscreen_btn.on_click = handle_fullscreen_toggle

        # Set focus on back button initially
        back_btn.set_focus(True)

    # Button handlers
    def handle_back():
        nonlocal running
        running = False
        return True

    def handle_fullscreen_toggle():
        nonlocal is_fullscreen, fullscreen_btn
        is_fullscreen = not is_fullscreen

        # Update button text
        fullscreen_text = "Fullscreen: ON" if is_fullscreen else "Fullscreen: OFF"
        fullscreen_btn.set_text(fullscreen_text)

        # Toggle fullscreen mode
        if is_fullscreen:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

        # Reload background and recreate buttons to match new screen size
        Button.all_buttons.clear()
        load_background_image()
        recreate_buttons()

        return True

    # Initial setup
    load_background_image()
    recreate_buttons()

    # Main settings loop
    while running:
        # Draw background
        if background_image:
            screen.fill(BACKGROUND)
            screen.blit(background_image, bg_pos)
        else:
            screen.fill(BACKGROUND)

        # Draw title
        title_text = title_font.render("Settings", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(screen_width//2, 80))
        screen.blit(title_text, title_rect)

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle window resize
            elif event.type == pygame.VIDEORESIZE:
                Button.all_buttons.clear()
                load_background_image()
                recreate_buttons()

            # Handle button events
            Button.update_all(event)

            # Keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # Draw all buttons
        back_btn.draw()
        fullscreen_btn.draw()

        # Draw instructions
        instructions = small_font.render("Press TAB to navigate, ENTER to select, ESC to go back", True, TEXT_COLOR)
        screen.blit(instructions, (screen_width // 2 - instructions.get_width() // 2, screen_height - 40))

        pygame.display.flip()
        clock.tick(60)

    # Clear buttons before returning
    Button.all_buttons.clear()
    return True


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

    # Button dimensions
    button_width = 250
    button_height = 50
    button_spacing = 20

    # Initialize button variables before using them in nonlocal
    start_game_btn = None
    load_game_btn = None
    settings_btn = None
    quit_btn = None

    # Store original background image
    original_bg = None
    background_image = None
    bg_pos = (0, 0)

    # Function to load and scale background image
    def load_background_image():
        nonlocal background_image, bg_pos, original_bg, screen_width, screen_height

        # Update screen dimensions
        screen_width, screen_height = screen.get_size()

        try:
            bg_path = os.path.join("assets", "images", "MainMenuBackground.png")

            # Load original image only once
            if original_bg is None and os.path.exists(bg_path):
                original_bg = pygame.image.load(bg_path)

            if original_bg:
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
        except Exception as e:
            print(f"Error loading background: {e}")
            background_image = None
            bg_pos = (0, 0)

    # Function to recreate and reposition buttons
    def recreate_buttons():
        nonlocal start_game_btn, load_game_btn, settings_btn, quit_btn

        # Start Game button
        start_game_btn = create_button(
            screen, button_font, width=button_width, height=button_height,
            y_offset=-100, text="Start Game",
            hover_text="▶ Start Game ▶",
            hover_text_color=HOVER_TEXT_COLOR,
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
            hover_text="Load Game (Unavailable)",
            hover_text_color=HOVER_TEXT_COLOR,
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
            hover_text="⚙ Settings ⚙",
            hover_text_color=HOVER_TEXT_COLOR,
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
            hover_text="✖ Exit Game ✖",
            hover_text_color=(255, 100, 100),
            tooltip="Exit the game",
            sound_path=sound_path,
            hover_sound_path=hover_sound,
            visible_background=False,
            debug_hitbox=True
        )

        # Button handlers
        start_game_btn.on_click = handle_start_game
        settings_btn.on_click = handle_settings
        quit_btn.on_click = handle_quit

        # Ensure the first button has focus initially for keyboard navigation
        start_game_btn.set_focus(True)

    # Button handlers
    def handle_start_game():
        # Start new game logic would go here
        return True

    def handle_settings():
        # Clear current buttons
        Button.all_buttons.clear()

        # Run settings menu
        RunSettingsMenuLoop()

        # Recreate main menu buttons when returning
        load_background_image()
        recreate_buttons()
        return True

    def handle_quit():
        nonlocal running
        running = False
        return True

    # Initial setup
    load_background_image()
    recreate_buttons()

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

            # Handle window resize
            elif event.type == pygame.VIDEORESIZE:
                # Clear the button list to avoid duplicates
                Button.all_buttons.clear()
                # Load background with new dimensions
                load_background_image()
                # Recreate buttons with proper positioning
                recreate_buttons()

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