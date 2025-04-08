import pygame
import os
from buttons.ButtonClass import Button
from buttons.ButtonCreator import create_button, create_slider
from utility.MusicManager import MusicManager

# Colors
BACKGROUND = (40, 44, 52)
TEXT_COLOR = (220, 220, 220)
HOVER_COLOR = (100, 100, 150, 180)
HOVER_TEXT_COLOR = (255, 255, 0)

# Sound files paths
click_sound_path = os.path.join("assets", "audio", "click.wav")
hover_sound_path = os.path.join("assets", "audio", "hover.wav")
focus_sound_path = os.path.join("assets", "audio", "focus.wav")

# Music file path
background_music_path = os.path.join("assets", "audio", "background_music.mp3")

# Initialize music manager
music_manager = MusicManager()

# Global settings - now loaded from settings manager
fps_display_enabled = music_manager.settings_manager.get_setting("fps_display", False)
music_enabled = music_manager.settings_manager.get_setting("music_enabled", True)


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
    fps_btn = None
    music_toggle_btn = None
    volume_slider = None
    master_volume_slider = None  # New slider for master volume

    # Store original background image
    original_bg = None
    background_image = None
    bg_pos = (0, 0)

    # Access global settings
    global fps_display_enabled, music_enabled

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
        nonlocal back_btn, fullscreen_btn, fps_btn, music_toggle_btn, volume_slider, master_volume_slider

        # Back button in top left
        back_btn = create_button(
            screen, button_font, "← Back",
            width=120, height=40,
            x_offset=-screen_width // 2 + 80, y_offset=-screen_height // 2 + 40,
            hover_text="← Return",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Return to main menu",
            sound_path=sound_path,
            hover_sound_path=hover_sound,
            visible_background=True,
            music_manager=music_manager
        )

        # Fullscreen toggle button
        fullscreen_text = "Fullscreen: ON" if is_fullscreen else "Fullscreen: OFF"
        fullscreen_btn = create_button(
            screen, button_font, fullscreen_text,
            width=250, height=50,
            y_offset=-20,
            hover_text="Toggle Fullscreen Mode",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Switch between windowed and fullscreen modes",
            sound_path=sound_path,
            hover_sound_path=hover_sound,
            toggle_mode=True,
            toggled=is_fullscreen,
            music_manager=music_manager
        )

        # FPS counter toggle button
        fps_text = "FPS Counter: ON" if fps_display_enabled else "FPS Counter: OFF"
        fps_btn = create_button(
            screen, button_font, fps_text,
            width=250, height=50,
            y_offset=50,
            hover_text="Toggle FPS Display",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Show or hide frames per second counter",
            sound_path=sound_path,
            hover_sound_path=hover_sound,
            toggle_mode=True,
            toggled=fps_display_enabled,
            music_manager=music_manager
        )

        # Music toggle button
        music_text = "Music: ON" if music_enabled else "Music: OFF"
        music_toggle_btn = create_button(
            screen, button_font, music_text,
            width=250, height=50,
            y_offset=120,
            hover_text="Toggle Background Music",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Turn background music on or off",
            sound_path=sound_path,
            hover_sound_path=hover_sound,
            toggle_mode=True,
            toggled=music_enabled,
            music_manager=music_manager
        )

        # Master volume slider - add before music volume
        master_volume_slider = create_slider(
            screen, button_font,
            width=250, height=30,
            y_offset=200,  # Increased from 180 to 200
            min_value=0, max_value=100,
            current_value=int(music_manager.get_master_volume() * 100),
            label="Master Volume",
            sound_path=sound_path,
            hover_sound_path=hover_sound,
            music_manager=music_manager
        )

        # Music volume slider - move down
        volume_slider = create_slider(
            screen, button_font,
            width=250, height=30,
            y_offset=280,  # Increased from 240 to 280 for more spacing
            min_value=0, max_value=100,
            current_value=int(music_manager.get_volume() * 100),
            label="Music Volume",
            sound_path=sound_path,
            hover_sound_path=hover_sound,
            music_manager=music_manager
        )

        # Button handlers
        back_btn.on_click = handle_back
        fullscreen_btn.on_click = handle_fullscreen_toggle
        fps_btn.on_click = handle_fps_toggle
        music_toggle_btn.on_click = handle_music_toggle
        volume_slider.on_value_change = handle_volume_change
        master_volume_slider.on_value_change = handle_master_volume_change  # Add handler for master volume

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
        
        # Save fullscreen setting
        music_manager.settings_manager.set_setting("fullscreen", is_fullscreen)

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

    def handle_fps_toggle():
        global fps_display_enabled
        fps_display_enabled = not fps_display_enabled
        
        # Save fps display setting
        music_manager.settings_manager.set_setting("fps_display", fps_display_enabled)

        # Update button text
        fps_text = "FPS Counter: ON" if fps_display_enabled else "FPS Counter: OFF"
        fps_btn.set_text(fps_text)
        return True

    def handle_music_toggle():
        global music_enabled
        music_enabled = not music_enabled
        
        # Update music_enabled in music manager
        music_manager.set_music_enabled(music_enabled)

        # Update button text
        music_text = "Music: ON" if music_enabled else "Music: OFF"
        music_toggle_btn.set_text(music_text)

        # Start or stop music
        if music_enabled:
            if not music_manager.is_playing():
                music_manager.play_music(background_music_path)
        else:
            music_manager.stop_music()

        return True

    def handle_volume_change(value):
        volume = value / 100.0  # Convert to 0.0-1.0 range
        music_manager.set_volume(volume)
        return True

    def handle_master_volume_change(value):
        volume = value / 100.0  # Convert to 0.0-1.0 range
        music_manager.set_master_volume(volume)
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
        title_rect = title_text.get_rect(center=(screen_width // 2, 80))
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
            
            # Handle slider events directly
            if volume_slider:
                volume_slider.handle_event(event)
            if master_volume_slider:
                master_volume_slider.handle_event(event)

            # Keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F11:
                    # F11 to toggle fullscreen
                    handle_fullscreen_toggle()

        # Draw all buttons
        back_btn.draw()
        fullscreen_btn.draw()
        fps_btn.draw()
        music_toggle_btn.draw()
        master_volume_slider.draw()  # Draw master volume slider
        volume_slider.draw()

        # Draw instructions
        instructions = small_font.render("Press TAB to navigate, ENTER to select, ESC to go back, F11 for fullscreen",
                                         True, TEXT_COLOR)
        screen.blit(instructions, (screen_width // 2 - instructions.get_width() // 2, screen_height - 40))

        # Draw FPS counter if enabled
        if fps_display_enabled:
            fps = int(clock.get_fps())
            fps_text = small_font.render(f"FPS: {fps}", True, (255, 255, 0))
            screen.blit(fps_text, (10, 10))

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

    # Apply fullscreen setting from saved settings
    is_fullscreen = music_manager.settings_manager.get_setting("fullscreen", False)
    if is_fullscreen and not (screen.get_flags() & pygame.FULLSCREEN):
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    elif not is_fullscreen and (screen.get_flags() & pygame.FULLSCREEN):
        pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

    # Start background music if enabled
    if music_enabled and os.path.exists(background_music_path):
        music_manager.play_music(background_music_path)

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

    # Track fullscreen state
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

    # Function to toggle fullscreen mode
    def toggle_fullscreen():
        nonlocal is_fullscreen
        is_fullscreen = not is_fullscreen

        # Save fullscreen setting
        music_manager.settings_manager.set_setting("fullscreen", is_fullscreen)

        # Toggle fullscreen mode
        if is_fullscreen:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

        # Reload background and recreate buttons to match new screen size
        Button.all_buttons.clear()
        load_background_image()
        recreate_buttons()

    # Function to recreate and reposition buttons
    def recreate_buttons():
        nonlocal start_game_btn, load_game_btn, settings_btn, quit_btn

        # Start Game button
        start_game_btn = create_button(
            screen, button_font, "Start Game",
            width=button_width, height=button_height,
            y_offset=-100,
            hover_text="▶ Start Game ▶",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Start a new game",
            sound_path=sound_path,
            hover_sound_path=hover_sound,
            visible_background=False,
            debug_hitbox=True,
            music_manager=music_manager
        )

        # Load Game button (greyed out)
        load_game_btn = create_button(
            screen, button_font, "Load Game",
            width=button_width, height=button_height,
            y_offset=-100 + button_height + button_spacing,
            hover_text="Load Game (Unavailable)",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Load a saved game",
            visible_background=False,
            debug_hitbox=True,
            disabled=True,
            music_manager=music_manager
        )

        # Settings button
        settings_btn = create_button(
            screen, button_font, "Settings",
            width=button_width, height=button_height,
            y_offset=-100 + (button_height + button_spacing) * 2,
            hover_text="⚙ Settings ⚙",
            hover_text_color=HOVER_TEXT_COLOR,
            tooltip="Game settings",
            sound_path=sound_path,
            hover_sound_path=hover_sound,
            visible_background=False,
            debug_hitbox=True,
            music_manager=music_manager
        )

        # Quit button
        quit_btn = create_button(
            screen, button_font, "Quit",
            width=button_width, height=button_height,
            y_offset=-100 + (button_height + button_spacing) * 3,
            hover_text="✖ Exit Game ✖",
            hover_text_color=(255, 100, 100),
            tooltip="Exit the game",
            sound_path=sound_path,
            hover_sound_path=hover_sound,
            visible_background=False,
            debug_hitbox=True,
            music_manager=music_manager
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

            # Global keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_F11:
                    # F11 to toggle fullscreen
                    toggle_fullscreen()

        # Draw all buttons
        start_game_btn.draw()
        load_game_btn.draw()
        settings_btn.draw()
        quit_btn.draw()

        # Draw instructions
        instructions = small_font.render("Press TAB to navigate, ENTER to select, Q to quit, F11 for fullscreen", True,
                                         TEXT_COLOR)
        screen.blit(instructions, (screen_width // 2 - instructions.get_width() // 2, screen_height - 40))

        # Draw FPS counter if enabled
        if fps_display_enabled:
            fps = int(clock.get_fps())
            fps_text = small_font.render(f"FPS: {fps}", True, (255, 255, 0))
            screen.blit(fps_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

