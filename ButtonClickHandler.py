import pygame

click_sound = None
click_states = {}

def handle_button_click(rect, on_click, id="default", sound_path="assets/audio/click.wav"):
    global click_sound

    if click_sound is None:
        pygame.mixer.init()
        click_sound = pygame.mixer.Sound(sound_path)

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    hovered = rect.collidepoint(mouse_pos)
    was_clicked = click_states.get(id, False)

    if hovered and mouse_click[0]:
        if not was_clicked:
            click_sound.play()
            on_click()
            click_states[id] = True
    elif not mouse_click[0]:
        click_states[id] = False

    return hovered
