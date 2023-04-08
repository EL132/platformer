import pygame, sys
from pygame.locals import *
import settings
from GameSave.SaveLoadManager import SaveLoadSystem

pygame.init()


display_surface = pygame.display.set_mode((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 32)
medium_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 64)
title_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 84)

save_load_manager = SaveLoadSystem(".save", "save_data")
settings.FPS = save_load_manager.load_game_data(["FPS"], [60])
settings.difficulty = save_load_manager.load_game_data(["difficulty"], [2])


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

        self.select = pygame.mixer.Sound('./SFX/menu-select.mp3')
        self.select.set_volume(0.3)
        self.hover = pygame.mixer.Sound('./SFX/menu-hover.wav')
        self.transition = pygame.mixer.Sound('./SFX/transition_sound.wav')

        pygame.mixer.music.load('./SFX/menu_music.mp3')
        pygame.mixer.music.play()

        button_list = [False, False, False]

        while self.running:
            
            # print("fps: ", settings.FPS)
            # print("difficulty: ", settings.difficulty)
            
            display_surface.fill((0,0,0))

            bg = pygame.image.load('./Menu/test_bg.png')
            display_surface.blit(bg, (0, 0))

            draw_text('Platformer', title_font, (0, 0, 0), display_surface, settings.DISPLAY_WIDTH // 2 - 225, 100)
            draw_text('Start game', font, (0, 0, 0), display_surface, settings.DISPLAY_WIDTH // 2 - 75, 200)
            draw_text('Options', font, (0, 0, 0), display_surface, settings.DISPLAY_WIDTH // 2 - 50, 250)
            draw_text('Quit', font, (0, 0, 0), display_surface, settings.DISPLAY_WIDTH // 2 - 25, 300)

            mx, my = pygame.mouse.get_pos()

            start_game_button = pygame.Rect(settings.DISPLAY_WIDTH // 2 - 75, 200, 165, 35)
            options_button = pygame.Rect(settings.DISPLAY_WIDTH // 2 - 50, 250, 125, 35)
            quit_button = pygame.Rect(settings.DISPLAY_WIDTH // 2 - 25, 300, 100, 35)

            if start_game_button.collidepoint((mx, my)):
                if not button_list[0]:
                    pygame.mixer.Sound.play(self.hover)
                    button_list[0] = True
                pygame.draw.line(display_surface, (0, 0, 0), (settings.DISPLAY_WIDTH // 2 - 75, 235), (settings.DISPLAY_WIDTH // 2 + 89, 235), 4)
                if self.click:
                    pygame.mixer.Sound.play(self.select)
                    pygame.mixer.music.stop()
                    pygame.time.delay(150)
                    pygame.mixer.Sound.play(self.transition)
                    self.game()
            else:
                button_list[0] = False

            if options_button.collidepoint((mx, my)):
                if not button_list[1]:
                    pygame.mixer.Sound.play(self.hover)
                    button_list[1] = True
                pygame.draw.line(display_surface, (0, 0, 0), (settings.DISPLAY_WIDTH // 2 - 50, 285), (settings.DISPLAY_WIDTH // 2 + 73, 285), 4)
                if self.click:
                    pygame.mixer.Sound.play(self.select)
                    self.options()
            else:
                button_list[1] = False

            if quit_button.collidepoint((mx, my)):
                if not button_list[2]:
                    pygame.mixer.Sound.play(self.hover)
                    button_list[2] = True
                pygame.draw.line(display_surface, (0, 0, 0), (settings.DISPLAY_WIDTH // 2 - 25, 335), (settings.DISPLAY_WIDTH // 2 + 40, 335), 4)
                if self.click:
                    save_load_manager.save_game_data([settings.FPS], ["FPS"])
                    save_load_manager.save_game_data([settings.difficulty], ["difficulty"])
                    pygame.quit()
            else:
                button_list[2] = False
            
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

        button_list = [False, False, False, False, False, False]

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

            mx, my = pygame.mouse.get_pos()

            # (left, top, width, height)
            easy_button = pygame.Rect(45, 215, 69, 35)
            medium_button = pygame.Rect(205, 215, 108, 35)
            hard_button = pygame.Rect(405, 215, 70, 35)

            button_40 = pygame.Rect(45, 375, 50, 35)
            button_60 = pygame.Rect(205, 375, 50, 35)
            button_80 = pygame.Rect(405, 375, 50, 35)

            if easy_button.collidepoint((mx, my)):
                if not button_list[0]:
                    pygame.mixer.Sound.play(self.hover)
                    button_list[0] = True
                pygame.draw.line(display_surface, (255, 255, 255), (45, 250), (115, 250), 4)
                if self.click:
                    settings.difficulty = 1
                    pygame.mixer.Sound.play(self.select)
            else:
                button_list[0] = False

            if medium_button.collidepoint((mx, my)):
                if not button_list[1]:
                    pygame.mixer.Sound.play(self.hover)
                    button_list[1] = True
                pygame.draw.line(display_surface, (255, 255, 255), (205, 250), (313, 250), 4)
                if self.click:
                    settings.difficulty = 2
                    pygame.mixer.Sound.play(self.select)
            else:
                button_list[1] = False

            if hard_button.collidepoint((mx, my)):
                if not button_list[2]:
                    pygame.mixer.Sound.play(self.hover)
                    button_list[2] = True
                pygame.draw.line(display_surface, (255, 255, 255), (405, 250), (475, 250), 4)
                if self.click:
                    settings.difficulty = 3
                    pygame.mixer.Sound.play(self.select)
            else:
                button_list[2] = False

            if button_40.collidepoint((mx, my)):
                if not button_list[3]:
                    pygame.mixer.Sound.play(self.hover)
                    button_list[3] = True
                pygame.draw.line(display_surface, (255, 255, 255), (45, 410), (82, 410), 4)
                if self.click:
                    settings.FPS = 40
                    pygame.mixer.Sound.play(self.select)
            else:
                button_list[3] = False
            
            if button_60.collidepoint((mx, my)):
                if not button_list[4]:
                    pygame.mixer.Sound.play(self.hover)
                    button_list[4] = True
                pygame.draw.line(display_surface, (255, 255, 255), (205, 410), (242, 410), 4)
                if self.click:
                    settings.FPS = 60
                    pygame.mixer.Sound.play(self.select)
            else:
                button_list[4] = False

            if button_80.collidepoint((mx, my)):
                if not button_list[5]:
                    pygame.mixer.Sound.play(self.hover)
                    button_list[5] = True
                pygame.draw.line(display_surface, (255, 255, 255), (405, 410), (442, 410), 4)
                if self.click:
                    settings.FPS = 80
                    pygame.mixer.Sound.play(self.select)
            else:
                button_list[5] = False


            self.click = False
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True   
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.update()
            clock.tick(settings.FPS)
    
    def run(self):
        self.main_menu()