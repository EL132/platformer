import pygame
from pytmx.util_pygame import load_pygame

pygame.init()

print('***************')

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 448
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
sprite_group = pygame.sprite.Group()

#tmx_data = load_pygame('./maps/levelOne.tmx')
tmx_data = load_pygame('./levelSelector/Custom/Ninja Tilemaps/noTerrains.tmx')
print(dir(tmx_data))

while True: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit()
    
    display_surface.fill('black')
    pygame.display.update()