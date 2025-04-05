import pygame

screen = None
font = None
background = None

def InitializeWindowCreation():
    global screen, font, background

    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Fantasy Falls")
    font = pygame.font.SysFont(None, 60)

    background = pygame.image.load("images\\MainMenuBackground.png").convert()

def DrawBackground():
    global screen, background

    screen_width, screen_height = screen.get_size()
    scaled_background = pygame.transform.scale(background, (screen_width, screen_height))
    screen.blit(scaled_background, (0, 0))
