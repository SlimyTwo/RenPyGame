import pygame
import utility.GlobalVariables as gv

from utility.DrawMainMenuBackground import DrawMainMenuBackground
from buttons.StartButton import StartButtonDrawingAndHandling
from buttons.LoadGameButton import LoadGameButtonDrawingAndHandling
from buttons.SettingsButton import SettingsButtonDrawingAndHandling, GetUpdatedScreen
from buttons.QuitButton import QuitButtonDrawingAndHandling
from buttons.TestButton import create_test_button
from buttons.ButtonClass import ButtonGroup
from utility.CompleteProgramTermination import ProgramTerminator


def RunMainMenuLoop():
    running = True

    # Load an icon for demo purposes
    try:
        icon = pygame.image.load("assets/images/settings_icon.png")
        icon = pygame.transform.scale(icon, (24, 24))
    except:
        # Fallback if image can't be loaded
        icon = None

    # Create a button group for radio-button style behavior
    radio_group = ButtonGroup()

    # Create buttons with different features to showcase capabilities
    test_button = create_test_button(
        gv.screen, gv.font,
        width=500, height=80,
        y_offset=-150,
        text="Invisible with Debug",
        visible_background=False,
        debug_hitbox=True,
        debug_color=(255, 0, 0),
        tooltip="This button has an invisible background with hitbox outline"
    )

    icon_button = create_test_button(
        gv.screen, gv.font,
        width=500, height=80,
        y_offset=-50,
        text="Button with Icon",
        visible_background=True,
        debug_hitbox=False,
        icon=icon,
        tooltip="This button has an icon and tooltip"
    )

    disabled_button = create_test_button(
        gv.screen, gv.font,
        width=500, height=80,
        y_offset=50,
        text="Disabled Button",
        visible_background=True,
        disabled=True,
        tooltip="This button is disabled and can't be clicked"
    )

    # Radio button group - only one can be selected at a time
    radio_button1 = create_test_button(
        gv.screen, gv.font,
        width=500, height=60,
        y_offset=150,
        text="Radio Option 1",
        button_group=radio_group,
        tooltip="Part of radio group"
    )

    radio_button2 = create_test_button(
        gv.screen, gv.font,
        width=500, height=60,
        y_offset=220,
        text="Radio Option 2",
        button_group=radio_group,
        tooltip="Part of radio group"
    )

    radio_button3 = create_test_button(
        gv.screen, gv.font,
        width=500, height=60,
        y_offset=290,
        text="Radio Option 3",
        button_group=radio_group,
        tooltip="Part of radio group"
    )

    animation_button = create_test_button(
        gv.screen, gv.font,
        width=500, height=80,
        y_offset=370,
        text="Animation Button",
        tooltip="This button has smooth color transitions"
    )

    while running:
        # Process all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Toggle disabled state with keyboard for demo
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    disabled_button.set_disabled(not disabled_button.disabled)

            # Handle events for all buttons
            test_button.handle_event(event)
            icon_button.handle_event(event)
            disabled_button.handle_event(event)
            radio_button1.handle_event(event)
            radio_button2.handle_event(event)
            radio_button3.handle_event(event)
            animation_button.handle_event(event)

        DrawMainMenuBackground()

        # StartButtonDrawingAndHandling(gv.screen, gv.font)

        # Display some info text
        info_font = pygame.font.Font(None, 24)
        info_text = info_font.render("Press 'D' to toggle disabled state", True, (255, 255, 255))
        gv.screen.blit(info_text, (20, 20))

        selected = radio_group.get_selected()
        if selected:
            selection_text = info_font.render(f"Selected: {selected.text}", True, (255, 255, 255))
            gv.screen.blit(selection_text, (20, 50))

        # Draw all the test buttons
        test_button.draw()
        icon_button.draw()
        disabled_button.draw()
        radio_button1.draw()
        radio_button2.draw()
        radio_button3.draw()
        animation_button.draw()

        updated_screen = GetUpdatedScreen()
        if updated_screen:
            gv.screen = updated_screen

        pygame.display.flip()

    ProgramTerminator.terminate()