import pygame
from player import Player
from boss import Boss
from game import Game


#Set display surface (tile size is 32x32 ; 25 tiles wide, 14 tiles high)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 448
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

sprite_group = pygame.sprite.Group()


#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()


# global variables


# sprite group for collision detection
land_sprite_group = pygame.sprite.Group()
water_sprite_group = pygame.sprite.Group()

my_player_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()


my_player = Player(164, 164, land_sprite_group, water_sprite_group)
my_player_group.add(my_player)

boss_chomper = Boss(600, 373)
boss_group.add(boss_chomper)

my_game = Game()