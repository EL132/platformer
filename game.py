import pygame, csv, time

#Use 2D vectors
vector = pygame.math.Vector2

#Initiailize pygame
pygame.init()

#Set display surface (tile size is 32x32 ; 25 tiles wide, 14 tiles high)
WINDOW_WIDTH = 775
WINDOW_HEIGHT = 434
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

        if image_number == -1:
            pass
        else:
            self.image = tile_list[image_number]

            main_group.add(self)

            # rect and positioning
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)    
            if sub_group == water_tile_group or sub_group == dirt_tile_group:
                sub_group.add(self)

        

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        
    def custom_draw(self):
        for sprite in self.sprites():
            display_surface.blit(sprite.image, sprite.rect)


class Player(pygame.sprite.Sprite):
    # parameters are TBD for grass and water tiles
    def __init__(self, x, y, dirt_tiles, water_tiles):
        super().__init__()

        # animation frames ::
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []

        # adding the moving right frames
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (1).png'), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (2).png'), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (3).png'), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (4).png'), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (5).png'), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (6).png'), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (7).png'), (64, 64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (8).png'), (64, 64)))

        # adding the moving left frames
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (1).png'), (64, 64)), True, False))
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (2).png'), (64, 64)), True, False))
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (3).png'), (64, 64)), True, False))
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (4).png'), (64, 64)), True, False))
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (5).png'), (64, 64)), True, False))
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (6).png'), (64, 64)), True, False))
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (7).png'), (64, 64)), True, False))
        self.move_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Run (8).png'), (64, 64)), True, False))

        # idle left frames 
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (1).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (2).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (3).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (4).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (5).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (6).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (7).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (8).png'), (64, 64)), True, False))
        self.idle_left_sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (9).png'), (64, 64)), True, False))

        # idle right frames 
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (1).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (2).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (3).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (4).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (5).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (6).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (7).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (8).png'), (64, 64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load('./images/player/boy/Idle (9).png'), (64, 64)))

        # index of the current sprite 
        self.current_sprite = 0

        self.image = self.move_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.bottomleft = (x, y)

        self.dirt_tiles = dirt_tiles
        self.water_tiles = water_tiles

        # vector stuff with position, velocity, and accel
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        # kinematic constants
        self.HORIZONTAL_ACCELERATION = 0.7
        self.HORIZONTAL_FRICTION = 0.10
        self.VERTICAL_ACCELERATION = 0.25 # gravity 
        self.VERTICAL_JUMP_SPEED = 10


    def update(self):
        self.move()
        self.check_collisions()
        # create a mask
        self.mask = pygame.mask.from_surface(self.image, 4)
        mask_outline = self.mask.outline() # this gives a list of points that are on the mask 
        pygame.draw.lines(self.image, (255, 0, 0), True, mask_outline)


    def move(self):
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.position.x < 0:
                self.position.x = WINDOW_WIDTH
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, 0.1)
        elif keys[pygame.K_RIGHT]:
            if self.position.x > WINDOW_WIDTH:
                self.position.x = 0
            self.acceleration.x = self.HORIZONTAL_ACCELERATION    
            self.animate(self.move_right_sprites, 0.1)    
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, 0.1)
            else:
                self.animate(self.idle_left_sprites, 0.1)

        # # calc new kinematic values 
        self.acceleration.x -= self.HORIZONTAL_FRICTION * self.velocity.x # this is for friction of the acceleration
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration
        
        self.rect.bottomleft = self.position

        if self.position.y > WINDOW_HEIGHT:
            self.position.y = self.y

    def check_collisions(self):
        # this function needs to really be rewritten, we need to make sure the contact is natural
        dirt_collided_platforms = pygame.sprite.spritecollide(self, self.dirt_tiles, False, pygame.sprite.collide_mask) # this makes a list of all in contact tiles
        if dirt_collided_platforms:
            if self.velocity.y > 0:
                self.position.y = dirt_collided_platforms[0].rect.top + 8
                self.velocity.y = 0        
        water_collided_platforms = pygame.sprite.spritecollide(self, self.water_tiles, False)
        if water_collided_platforms:
            self.position = (self.x, self.y)
    
    def jump(self):
        if pygame.sprite.spritecollide(self, self.dirt_tiles, False):
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED

    def animate(self, sprite_list, speed):
        # speed parameter used to limit how fast the animation goes 

        # loop through sprite list and change current sprite 
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
        
        self.image = sprite_list[int(self.current_sprite)]


# create sprite groups
visible_sprites = YSortCameraGroup()
my_player_group = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group() 
dirt_tile_group = pygame.sprite.Group()


tic = time.perf_counter()

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
            new_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, 32, 32))

            cut_tiles.append(new_surface)
            
    return cut_tiles

tile_list = import_cut_graphics('./images/tiles/tiles-original.png')

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



# i have all the csv files in arrays and the tile_list, now I need to match them 

for i in range(len(background_tiles)):
    for j in range(len(background_tiles[i])): 
        # background tiles is a sequence of ID's
        Tile(j * 31, i * 31, int(background_tiles[i][j]), visible_sprites)

for i in range(len(brown_dirt_tiles)):
    for j in range(len(brown_dirt_tiles[i])): 
        # background tiles is a sequence of ID's
        Tile(j * 31, i * 31, int(brown_dirt_tiles[i][j]), visible_sprites, dirt_tile_group)

for i in range(len(accessories_tiles)):
    for j in range(len(accessories_tiles[i])): 
        # background tiles is a sequence of ID's
        Tile(j * 31, i * 31, int(accessories_tiles[i][j]), visible_sprites)

for i in range(len(water_tiles)):
    for j in range(len(water_tiles[i])): 
        # background tiles is a sequence of ID's
        Tile(j * 31, i * 31, int(water_tiles[i][j]), visible_sprites, water_tile_group)

for i in range(len(yellow_dirt_tiles)):
    for j in range(len(yellow_dirt_tiles[i])): 
        # background tiles is a sequence of ID's
        Tile(j * 31, i * 31, int(yellow_dirt_tiles[i][j]), visible_sprites, dirt_tile_group)



my_player = Player(164, 164, dirt_tile_group, water_tile_group)
my_player_group.add(my_player)

print(dirt_tile_group)

toc = time.perf_counter()
print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.jump()
    
    visible_sprites.custom_draw()

    my_player_group.update()
    my_player_group.draw(display_surface)
    

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()