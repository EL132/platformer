from colorsys import rgb_to_hls
import pygame, time, random
from pytmx.util_pygame import load_pygame

from variables import *
from player import Player
from boss import Boss
from game import Game
from tile import *




my_player = Player(164, 164, land_sprite_group, water_sprite_group)
my_player_group.add(my_player)

boss_chomper = Boss(600, 373)
boss_group.add(boss_chomper)

my_game = Game()


#Initiailize pygame
pygame.init()

# video tmx code
tmx_data = load_pygame('./Levels/levelOne/maps/levelOne.tmx')


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

    boss_group.update()
    boss_group.draw(display_surface)

    my_game.update()
    

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()