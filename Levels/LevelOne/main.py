from colorsys import rgb_to_hls
import pygame, time, random
from pytmx.util_pygame import load_pygame

from tile import Tile
from player import Player
from boss import Boss
from constants import *


display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

sprite_group = pygame.sprite.Group()

clock = pygame.time.Clock()

#Initiailize pygame
pygame.init()

# video tmx code
tmx_data = load_pygame('./Levels/levelOne/maps/levelOne.tmx')


land_sprite_group = pygame.sprite.Group()
water_sprite_group = pygame.sprite.Group()

# cycle through all layers
for layer in tmx_data.visible_layers:
    if hasattr(layer,'data'):
        for x, y, surf in layer.tiles():
            # for tile in layer.tiles():
                # NOTE: here i need to check if the tile is an edge tile , use the ID of the edge tile to check this, just am not sure 
                # how to do that because the documentation is so shit and basic 
            pos = (x * 32, y * 32)
            temp = Tile(pos = pos, surf = surf, groups = sprite_group)
            if layer.name in ('Yellow Dirt', 'Brown Dirt'):
                land_sprite_group.add(temp)
            elif layer.name in ('Water'):
                water_sprite_group.add(temp)





my_player_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

my_player = Player(164, 164, land_sprite_group, water_sprite_group)
my_player_group.add(my_player)

boss_chomper = Boss(600, 385)
boss_group.add(boss_chomper)





class Game():
    def __init__(self):


        self.lives = 5
        self.score = 0

        self.custom_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 32)
        self.title_text = self.custom_font.render("Level One", True, BEIGE)
        self.title_text_rect = self.title_text.get_rect()
        self.title_text_rect.center = (WINDOW_WIDTH // 2, 25)

        self.score_text = self.custom_font.render("Score " + str(self.score), True, BEIGE)
        self.score_text_rect = self.score_text.get_rect()
        self.score_text_rect.center = (75, 25)

        self.lives_text = self.custom_font.render("Lives " + str(self.lives), True, BEIGE)
        self.lives_text_rect = self.lives_text.get_rect()
        self.lives_text_rect.center = (WINDOW_WIDTH - 65, 25)

    def update(self):
        self.score_text = self.custom_font.render("Score " + str(self.score), True, BEIGE)        
        display_surface.blit(self.score_text, self.score_text_rect)

        self.lives_text = self.custom_font.render("Lives " + str(self.lives), True, BEIGE)
        display_surface.blit(self.lives_text, self.lives_text_rect)
        self.check_collisions(my_player, boss_chomper)

    def check_collisions(self, player, boss):
        if pygame.sprite.groupcollide(my_player_group, boss_group, False, False):
            self.score_update(15)
            self.lives_update(1)
        # not sure why this doesn't work
        # if pygame.sprite.collide_mask(player.mask, boss.mask):
        #     self.score_update(15)
        #     self.lives_update(1)

    def score_update(self, score):
        self.score += score
    
    def lives_update(self, lives):
        self.lives -= lives


my_game = Game()





running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                my_player.jump()

    display_surface.fill('black')
    sprite_group.draw(display_surface)

    my_player_group.update()
    my_player_group.draw(display_surface)
    # pygame.draw.rect(display_surface, (255, 255, 255), my_player.rect)

    boss_group.update()
    boss_group.draw(display_surface)
    # pygame.draw.rect(display_surface, (255, 255, 255), boss_chomper.rect)

    my_game.update()
    

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()