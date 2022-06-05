import pygame
from tkinter import *
import pygame_widgets as pw
import game_play


def window():
    pygame.quit()
    color_light = (202, 203, 213)
    color_dark = (22, 22, 22)
    pygame.init()
    window = pygame.display.set_mode((900, 600))
    image = pygame.image.load("Main_Enistien.png")
    image = image.convert()
    small_font = pygame.font.Font('Roboto-Bold.ttf', 70)
    text = small_font.render('Choose Difficulty', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (460, 110)
    """def quit():
        window.distroy()"""

    # button
    def text_objects(text, font):
        text_surface = font.render(text, True, "white")
        return text_surface, text_surface.get_rect()

    def button(msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(window, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(window, ic, (x, y, w, h))
        small_text = pygame.font.SysFont("cosmeticians", 30)
        text_surf, text_rect = text_objects(msg, small_text)
        text_rect.center = ((x + (w / 2)), (y + (h / 2)))
        window.blit(text_surf, text_rect)

    running = True
    while running:
        events = pygame.event.get()
        window.blit(pygame.transform.scale(image, (900, 600)), (0, 0))
        window.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        button("Easy", 340, 320, 80, 40, color_dark, color_light, lambda: game_play.TwoPlayers(1))
        button("Medium", 430, 320, 80, 40, color_dark, color_light, lambda: game_play.TwoPlayers(3))
        button("Hard", 520, 320, 80, 40, color_dark, color_light, lambda: game_play.TwoPlayers(5))

        pygame.display.update()
        pygame.display.flip()

    pygame.quit()


window
