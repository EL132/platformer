import pygame, csv

#Use 2D vectors
vector = pygame.math.Vector2

#Initiailize pygame
pygame.init()

#Set display surface (tile size is 32x32 ; 25 tiles wide, 14 tiles high)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("TBD")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Define classes
class Tile(pygame.sprite.Sprite):
    """class to read and create individual tiles and place in display"""
    def __init__(self, x, y, image_number, main_group, sub_group=""):
        super().__init__()
        if image_number == 1:
            pass
        main_group.add(self)

        # rect and positioning
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# create sprite groups
main_tile_group = pygame.sprite.Group()


# for i in range(len(tile_map)):
#     for j in range(len(tile_map[i])): # don't need to store in a variable bc the init function of the class puts it into a group 
#         if tile_map[i][j] == 1:
#             Tile(j * 32, i * 32, 1, main_tile_group)
#         elif tile_map[i][j] == 2:
#             Tile(j * 32, i * 32, 2, main_tile_group, grass_tile_group)
#         elif tile_map[i][j] == 3:
#             Tile(j * 32, i * 32, 3, main_tile_group, water_tile_group)

background_tiles = []
brown_dirt_tiles = []
accessories_tiles = []
water_tiles = []
yellow_dirt_tiles = []


with open("./csv/Level One/Background.csv") as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        background_tiles.append(row)
with open("./csv/Level One/Accessories.csv") as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        accessories_tiles.append(row)
with open("./csv/Level One/Brown Dirt.csv") as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        brown_dirt_tiles.append(row)
with open("./csv/Level One/Water.csv") as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        water_tiles.append(row)
with open("./csv/Level One/Yellow Dirt.csv") as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        yellow_dirt_tiles.append(row)



# to parse tile image to smaller tile images:

def import_cut_graphics(image_path):
    surface = pygame.image.load(image_path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / 32)
    tile_num_y = int(surface.get_size()[1] / 32)

    cut_tiles = []

    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * 32
            y = row * 32
            new_surface = pygame.Surface((32, 32))
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, 32, 32))

            cut_tiles.append(new_surface)
            
    return cut_tiles

tile_list = import_cut_graphics('./images/tiles/tiles-original.png')

# i have all the csv files in arrays and the tile_list, now I need to match them 


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()

    # main_tile_group.draw(display_surface) --> use when main tile group has been drawn


pygame.quit()