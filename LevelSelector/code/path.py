import pygame 
from pytmx.util_pygame import load_pygame

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 448
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

tmx_data = load_pygame('./maps/levelOne.tmx')

# for layer in tmx_data.visible_layers:
#     print(layer.name)

class PathBorder(): 
    pass
