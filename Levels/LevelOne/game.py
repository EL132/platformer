from variables import *
import pygame


class Game():
    def __init__(self):

        GREEN = (0, 255, 0)
        DARK_GREEN = (10, 50, 10)
        BLACK = (0, 0, 0)
        self.lives = 0
        self.score = 0

        # custom_font = pygame.font.Font('arial', 32)
        # self.title_text = custom_font.render("Feed the Dragon", True, GREEN, DARK_GREEN)
        # self.title_text_rect = self.title_text.get_rect()
        # self.title_text_rect.center = (WINDOW_WIDTH // 2, 25)

        # self.score_text = custom_font.render("Score: " + str(self.score), True, GREEN, DARK_GREEN)
        # self.score_text_rect = self.score_text.get_rect()
        # self.score_text_rect.center = (75, 25)

        # self.lives_text = custom_font.render("Lives: " + str(self.lives), True, GREEN, DARK_GREEN)
        # self.lives_text_rect = self.lives_text.get_rect()
        # self.lives_text_rect.center = (WINDOW_WIDTH - 65, 25)

    def update(self):
        # display_surface.blit(self.title_text, self.title_text_rect)
        # display_surface.blit(self.score_text, self.score_text_rect)
        # display_surface.blit(self.lives_text, self.lives_text_rect)
        self.check_collisions(my_player_group, boss_group)
    
    def check_collisions(self, player, boss):
        if pygame.sprite.groupcollide(player, boss, False, True):
            self.score_update(15)
            self.lives_update(1)

        

    def score_update(self, score):
        self.score += score
    
    def lives_update(self, lives):
        self.lives -= lives