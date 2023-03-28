import pygame, sys
from pygame.locals import *
import settings

pygame.init()


display_surface = pygame.display.set_mode((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 32)
medium_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 64)
title_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 84)




def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


class Menu():
    def main_menu(self):
        self.started_game = False
        self.fade_counter = 0
        self.click = False
        self.transitioned = False

        self.running = True

        while self.running:
            
            display_surface.fill((0,0,0))

            bg = pygame.image.load('./Menu/test_bg.png')
            display_surface.blit(bg, (0, 0))

            draw_text('Name of Game', title_font, (0, 0, 0), display_surface, settings.DISPLAY_WIDTH // 2 - 225, 100)
            draw_text('Start game', font, (0, 0, 0), display_surface, settings.DISPLAY_WIDTH // 2 - 75, 200)
            draw_text('Options', font, (0, 0, 0), display_surface, settings.DISPLAY_WIDTH // 2 - 50, 250)
            draw_text('Quit', font, (0, 0, 0), display_surface, settings.DISPLAY_WIDTH // 2 - 25, 300)

            mx, my = pygame.mouse.get_pos()

            start_game_button = pygame.Rect(settings.DISPLAY_WIDTH // 2 - 75, 200, 165, 35)
            options_button = pygame.Rect(settings.DISPLAY_WIDTH // 2 - 50, 250, 125, 35)
            quit_button = pygame.Rect(settings.DISPLAY_WIDTH // 2 - 25, 300, 100, 35)
            if start_game_button.collidepoint((mx, my)):
                # here i can now just blit a line below the text if it is currently being hovered
                pygame.draw.line(display_surface, (0, 0, 0), (settings.DISPLAY_WIDTH // 2 - 75, 235), (settings.DISPLAY_WIDTH // 2 + 89, 235), 4)
                if self.click:
                    self.game()
            if options_button.collidepoint((mx, my)):
                pygame.draw.line(display_surface, (0, 0, 0), (settings.DISPLAY_WIDTH // 2 - 50, 285), (settings.DISPLAY_WIDTH // 2 + 73, 285), 4)
                if self.click:
                    self.options()
            if quit_button.collidepoint((mx, my)):
                pygame.draw.line(display_surface, (0, 0, 0), (settings.DISPLAY_WIDTH // 2 - 25, 335), (settings.DISPLAY_WIDTH // 2 + 40, 335), 4)
                if self.click:
                    pygame.quit()

            self.click = False
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

            pygame.display.update()
            clock.tick(settings.FPS)

    def game(self):
        if self.fade_counter < 200:
            pygame.draw.rect(display_surface, (0, 0, 0), (0, 0, self.fade_counter, settings.DISPLAY_HEIGHT))
            self.fade_counter += 5

        # this transition is never getting shown because the loop stops when the self.running goes to false and when
        # the game state goes to 0, so we need to transition in the main.py once game has been started

        self.running = False
        self.started_game = True
        settings.game_state = 0
        # self.started_game = True


    def options(self):
        # only want to deal with options that we can change in our settings basically
        # likely will only be able to change FPS value and difficulty value 

        running = True
        while running:
            # will need to do the mx, my stuff that i did for the original screen, but for now this is fine
            
            display_surface.fill((0,0,0))

            pygame.draw.line(display_surface, (255, 255, 255), (0, 98), (settings.DISPLAY_WIDTH, 98), 8)

            draw_text('options', title_font, (255, 255, 255), display_surface, settings.DISPLAY_WIDTH // 2 - 150, 25)

            draw_text('Difficulty', medium_font, (255, 255, 255), display_surface, 25, 125)
            pygame.draw.line(display_surface, (255, 255, 255), (0, 195), (400, 195), 2)
            draw_text('Easy', font, (255, 255, 255), display_surface, 45, 215)
            draw_text('Medium', font, (255, 255, 255), display_surface, 205, 215)
            draw_text('Hard', font, (255, 255, 255), display_surface, 405, 215)

            draw_text('FPS', medium_font, (255, 255, 255), display_surface, 25, 275)
            pygame.draw.line(display_surface, (255, 255, 255), (0, 345), (400, 345), 2)
            draw_text('40', font, (255, 255, 255), display_surface, 45, 375)
            draw_text('60', font, (255, 255, 255), display_surface, 205, 375)
            draw_text('80', font, (255, 255, 255), display_surface, 405, 375)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
            
            pygame.display.update()
            clock.tick(settings.FPS)
    
    def run(self):
        self.main_menu()