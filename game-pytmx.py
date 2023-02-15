import pygame, time
from pytmx.util_pygame import load_pygame


#Use 2D vectors
vector = pygame.math.Vector2

#Initiailize pygame
pygame.init()

#Set display surface (tile size is 32x32 ; 25 tiles wide, 14 tiles high)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 448
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
sprite_group = pygame.sprite.Group()


#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()



# classes
class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,surf,groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)


class Player(pygame.sprite.Sprite):
    # parameters are TBD for grass and water tiles
    def __init__(self, x, y, contact_tiles):
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

        self.contact_tiles = contact_tiles

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
        dirt_collided_platforms = pygame.sprite.spritecollide(self, self.contact_tiles, False, pygame.sprite.collide_mask) # this makes a list of all in contact tiles
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






class BossOne(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y



# video tmx code
tmx_data = load_pygame('./maps/levelOne.tmx')

# sprite group for collision detection
contact_sprite_group = pygame.sprite.Group()


# cycle through all layers
for layer in tmx_data.visible_layers:
	# if layer.name in ('Floor', 'Plants and rocks', 'Pipes')

    print(layer.name)
    if hasattr(layer,'data'):
        for x, y, surf in layer.tiles():
            pos = (x * 32, y * 32)
            temp = Tile(pos = pos, surf = surf, groups = sprite_group)
            if layer.name in ('Yellow Dirt'):
                contact_sprite_group.add(temp)






my_player_group = pygame.sprite.Group()

my_player = Player(164, 164, contact_sprite_group)
my_player_group.add(my_player)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         my_player.jump()

    display_surface.fill('black')
    sprite_group.draw(display_surface)

    # my_player_group.update()
    # my_player_group.draw(display_surface)
    

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()