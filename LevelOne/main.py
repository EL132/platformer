from colorsys import rgb_to_hls
import pygame, time, random
from pytmx.util_pygame import load_pygame
from boss import *
from player import *
from constants import *
from tile import *

#Initiailize pygame
pygame.init()

# video tmx code
tmx_data = load_pygame('./levelOne/maps/levelOne.tmx')

# sprite group for collision detection
land_sprite_group = pygame.sprite.Group()
water_sprite_group = pygame.sprite.Group()

# cycle through all layers
for layer in tmx_data.visible_layers:
    if hasattr(layer,'data'):
        for x, y, surf in layer.tiles():
            # for tile in layer.tiles():
            #     print(tile.data)
                # NOTE: here i need to check if the tile is an edge tile , use the ID of the edge tile to check this, just am not sure 
                # how to do that because the documentation is so shit and basic 
            pos = (x * 31, y * 31)
            temp = Tile(pos = pos, surf = surf, groups = sprite_group)
            if layer.name in ('Yellow Dirt', 'Brown Dirt'):
                land_sprite_group.add(temp)
            elif layer.name in ('Water'):
                water_sprite_group.add(temp)



my_player_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()


my_player = Player(164, 164, land_sprite_group, water_sprite_group)
my_player_group.add(my_player)

boss_chomper = Boss(600, 373)
boss_group.add(boss_chomper)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.jump()

    display_surface.fill('black')
    sprite_group.draw(display_surface)

    my_player_group.update()
    my_player_group.draw(display_surface)

    boss_group.update()
    boss_group.draw(display_surface)
    

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()