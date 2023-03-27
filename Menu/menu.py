import pygame, sys
from pygame.locals import *

pygame.init()


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 448
FPS = 60

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 32)
title_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 84)

click = False


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    while True:
        display_surface.fill((0,0,0))

        bg = pygame.image.load('./Menu/test_bg.png')
        display_surface.blit(bg, (0, 0))

        draw_text('Name of Game', title_font, (0, 0, 0), display_surface, WINDOW_WIDTH // 2 - 225, 100)
        draw_text('Start game', font, (0, 0, 0), display_surface, WINDOW_WIDTH // 2 - 75, 200)
        draw_text('Options', font, (0, 0, 0), display_surface, WINDOW_WIDTH // 2 - 50, 250)
        draw_text('Quit', font, (0, 0, 0), display_surface, WINDOW_WIDTH // 2 - 25, 300)

        mx, my = pygame.mouse.get_pos()

        start_game_button = pygame.Rect(WINDOW_WIDTH // 2 - 75, 200, 165, 35)
        options_button = pygame.Rect(WINDOW_WIDTH // 2 - 50, 250, 125, 35)
        quit_button = pygame.Rect(WINDOW_WIDTH // 2 - 25, 300, 100, 35)
        if start_game_button.collidepoint((mx, my)):
            # here i can now just blit a line below the text if it is currently being hovered
            pygame.draw.line(display_surface, (0, 0, 0), (WINDOW_WIDTH // 2 - 75, 235), (WINDOW_WIDTH // 2 + 89, 235), 4)
            if click:
                game()
        if options_button.collidepoint((mx, my)):
            pygame.draw.line(display_surface, (0, 0, 0), (WINDOW_WIDTH // 2 - 50, 285), (WINDOW_WIDTH // 2 + 73, 285), 4)
            if click:
                options()
        if quit_button.collidepoint((mx, my)):
            pygame.draw.line(display_surface, (0, 0, 0), (WINDOW_WIDTH // 2 - 25, 335), (WINDOW_WIDTH // 2 + 40, 335), 4)
            if click:
                pygame.quit()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(FPS)

def game():
    running = True
    while running:
        display_surface.fill((0,0,0))
        
        draw_text('game', font, (255, 255, 255), display_surface, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        pygame.display.update()
        clock.tick(FPS)

def options():
    running = True
    while running:
        display_surface.fill((0,0,0))

        draw_text('options', title_font, (255, 255, 255), display_surface, WINDOW_WIDTH // 2 - 150, 25)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        pygame.display.update()
        clock.tick(FPS)

main_menu()