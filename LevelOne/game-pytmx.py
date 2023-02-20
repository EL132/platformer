from colorsys import rgb_to_hls
import pygame, time, random
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


# test
# classes
class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,surf,groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)


class Player(pygame.sprite.Sprite):
    # parameters are TBD for grass and water tiles
    def __init__(self, x, y, land_tiles, water_tiles):
        super().__init__()

        # animation frames :: default orientation is right 
        self.walk_right_frames = []
        self.walk_left_frames = []

        self.run_right_frames = []
        self.run_left_frames = []

        self.jump_right_frames = []
        self.jump_left_frames = []

        self.idle_right_frames = []
        self.idle_left_frames = []


        # establish left and right precedent for these frames at a later point 
        self.hurt_frames = []
        self.death_frames = []
        self.attack_one_frames = []
        self.attack_two_frames = []
        self.attack_three_frames = []


        # walk frames 
        self.walk_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Walk/walk 1.png').convert_alpha(), (80, 80)))
        self.walk_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Walk/walk 2.png').convert_alpha(), (80, 80)))
        self.walk_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Walk/walk 3.png').convert_alpha(), (80, 80)))
        self.walk_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Walk/walk 4.png').convert_alpha(), (80, 80)))
        self.walk_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Walk/walk 5.png').convert_alpha(), (80, 80)))
        self.walk_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Walk/walk 6.png').convert_alpha(), (80, 80)))
        for frame in self.walk_right_frames:
            self.walk_left_frames.append(pygame.transform.flip(frame, True, False))

        # run frames 
        self.run_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Run/run 1.png').convert_alpha(), (80, 80)))
        self.run_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Run/run 2.png').convert_alpha(), (80, 80)))
        self.run_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Run/run 3.png').convert_alpha(), (80, 80)))
        self.run_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Run/run 4.png').convert_alpha(), (80, 80)))
        self.run_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Run/run 5.png').convert_alpha(), (80, 80)))
        self.run_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Run/run 6.png').convert_alpha(), (80, 80)))
        for frame in self.run_right_frames:
            self.run_left_frames.append(pygame.transform.flip(frame, True, False))

        # jump frames 
        self.jump_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Jump/jump 1.png').convert_alpha(), (80, 80)))
        self.jump_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Jump/jump 2.png').convert_alpha(), (80, 80)))
        self.jump_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Jump/jump 3.png').convert_alpha(), (80, 80)))
        self.jump_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Jump/jump 4.png').convert_alpha(), (80, 80)))
        self.jump_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Jump/jump 5.png').convert_alpha(), (80, 80)))
        self.jump_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Jump/jump 6.png').convert_alpha(), (80, 80)))
        for frame in self.jump_right_frames:
            self.jump_left_frames.append(pygame.transform.flip(frame, True, False))

        # hurt frames
        self.hurt_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Hurt/hurt 1.png').convert_alpha(), (80, 80)))
        self.hurt_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Hurt/hurt 2.png').convert_alpha(), (80, 80)))
        self.hurt_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Hurt/hurt 3.png').convert_alpha(), (80, 80)))

        # death frames
        self.death_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Death/death 1.png').convert_alpha(), (80, 80)))
        self.death_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Death/death 2.png').convert_alpha(), (80, 80)))
        self.death_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Death/death 3.png').convert_alpha(), (80, 80)))
        self.death_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Death/death 4.png').convert_alpha(), (80, 80)))
        self.death_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Death/death 5.png').convert_alpha(), (80, 80)))
        self.death_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Death/death 6.png').convert_alpha(), (80, 80)))

        #attack one frames
        self.attack_one_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack One/attack 1.png').convert_alpha(), (80, 80)))
        self.attack_one_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack One/attack 2.png').convert_alpha(), (80, 80)))
        self.attack_one_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack One/attack 3.png').convert_alpha(), (80, 80)))
        self.attack_one_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack One/attack 4.png').convert_alpha(), (80, 80)))
        self.attack_one_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack One/attack 5.png').convert_alpha(), (80, 80)))
        self.attack_one_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack One/attack 6.png').convert_alpha(), (80, 80)))

        # attack two frames
        self.attack_two_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack Two/attack 1.png').convert_alpha(), (80, 80)))
        self.attack_two_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack Two/attack 2.png').convert_alpha(), (80, 80)))
        self.attack_two_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack Two/attack 3.png').convert_alpha(), (80, 80)))
        self.attack_two_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack Two/attack 4.png').convert_alpha(), (80, 80)))
        self.attack_two_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack Two/attack 5.png').convert_alpha(), (80, 80)))
        self.attack_two_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack Two/attack 6.png').convert_alpha(), (80, 80)))

        # attack three frames
        self.attack_three_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack Three/attack 1.png').convert_alpha(), (80, 80)))
        self.attack_three_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack Three/attack 2.png').convert_alpha(), (80, 80)))
        self.attack_three_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack Three/attack 3.png').convert_alpha(), (80, 80)))
        self.attack_three_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack Three/attack 4.png').convert_alpha(), (80, 80)))
        self.attack_three_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack Three/attack 5.png').convert_alpha(), (80, 80)))
        self.attack_three_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Attack Three/attack 6.png').convert_alpha(), (80, 80)))

        # idle frames
        self.idle_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Idle/idle 1.png').convert_alpha(), (80, 80)))
        self.idle_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Idle/idle 2.png').convert_alpha(), (80, 80)))
        self.idle_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Idle/idle 3.png').convert_alpha(), (80, 80)))
        self.idle_right_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/player/Woodcutter/Idle/idle 4.png').convert_alpha(), (80, 80)))
        for frame in self.idle_right_frames:
            self.idle_left_frames.append(pygame.transform.flip(frame, True, False))




        # index of the current sprite 
        self.current_sprite = 0

        self.image = self.run_right_frames[self.current_sprite]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.bottomleft = (x, y)

        self.land_tiles = land_tiles
        self.water_tiles = water_tiles

        # vector stuff with position, velocity, and accel
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        # kinematic constants
        # this acceleration is used for walking and running will just add to this value 
        self.HORIZONTAL_ACCELERATION = 0.35
        self.HORIZONTAL_FRICTION = 0.10
        self.VERTICAL_ACCELERATION = 0.25 # gravity 
        self.VERTICAL_JUMP_SPEED = 10


        # NEW CODE FOR IMPROVED COLLISION HERE:
        self.leg_hitbox_rect = pygame.Rect(self.x, self.y, 10, 15)
        print(self.leg_hitbox_rect)

        # create a mask
        self.mask = pygame.mask.from_surface(self.image, 4)


    def update(self):
        self.move()
        self.check_collisions()
        mask_outline = self.mask.outline() # this gives a list of points that are on the mask 
        # pygame.draw.lines(self.image, (255, 0, 0), True, mask_outline)


    def move(self):
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        # for collision improvements
        self.leg_hitbox_rect.centery = self.position.y - 16
        # pygame.draw.rect(display_surface, (255, 0, 0), self.leg_hitbox_rect, 1)
        left = False
        if left:
            self.leg_hitbox_rect.centerx = self.position.x + 6
        else:
            self.leg_hitbox_rect.centerx = self.position.x + 36


        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and keys[pygame.K_LSHIFT]:
            left = True
            if self.position.x < 0:
                self.position.x = WINDOW_WIDTH
            self.acceleration.x = -1 * (self.HORIZONTAL_ACCELERATION + 0.2)
            self.animate(self.run_left_frames, 0.1)
        elif keys[pygame.K_RIGHT] and keys[pygame.K_LSHIFT]:
            left = False
            if self.position.x < 0:
                self.position.x = WINDOW_WIDTH
            self.acceleration.x = 1 * (self.HORIZONTAL_ACCELERATION + 0.2)
            self.animate(self.run_right_frames, 0.1)
        elif keys[pygame.K_LEFT]:
            left = True
            if self.position.x < 0:
                self.position.x = WINDOW_WIDTH
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
            self.animate(self.walk_left_frames, 0.1)
        elif keys[pygame.K_RIGHT]:
            left = False
            if self.position.x > WINDOW_WIDTH:
                self.position.x = 0
            self.acceleration.x = self.HORIZONTAL_ACCELERATION    
            self.animate(self.walk_right_frames, 0.1)    
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_frames, 0.05)
            else:
                self.animate(self.idle_left_frames, 0.05)

        # # calc new kinematic values 
        self.acceleration.x -= self.HORIZONTAL_FRICTION * self.velocity.x # this is for friction of the acceleration
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration
        
        self.rect.bottomleft = self.position

        if self.position.y > WINDOW_HEIGHT:
            self.position.y = self.y

    def check_collisions(self):

        for tile in self.land_tiles:  
            # if pygame.sprite.collide_mask(self.mask.scale((15, 15)), tile):
            if pygame.sprite.collide_mask(self, tile):
                tile.mask = pygame.mask.from_surface(tile.image)
                tile_mask_outline = tile.mask.outline() # this gives a list of points that are on
                # pygame.draw.lines(self.image, (255, 0, 0), True, tile_mask_outline)
                if self.velocity.y > 0:
                    self.position.y = tile.rect.top + 2
                    self.velocity.y = 0
        for tile in self.water_tiles:  
            if pygame.sprite.collide_mask(self, tile):
                self.position.x = self.x
                self.position.y = self.y
    
    def jump(self):
        if pygame.sprite.spritecollide(self, self.land_tiles, False):
            self.animate(self.jump_right_frames, 0.1)
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED

    def animate(self, sprite_list, speed):
        # speed parameter used to limit how fast the animation goes 

        # loop through sprite list and change current sprite 
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
        
        self.image = sprite_list[int(self.current_sprite)]





class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # animation frames ::
        self.walk_right_frames = []
        self.walk_left_frames = []

        self.attack_one_left_frames = []
        self.attack_one_right_frames = []

        self.attack_two_left_frames = []
        self.attack_two_right_frames = []

        self.attack_three_left_frames = []
        self.attack_three_right_frames = []

        self.attack_four_left_frames = []
        self.attack_four_right_frames = []


        # walk frames
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Walk/walk 1.png').convert_alpha(), (200, 200)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Walk/walk 2.png').convert_alpha(), (200, 200)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Walk/walk 3.png').convert_alpha(), (200, 200)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Walk/walk 4.png').convert_alpha(), (200, 200)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Walk/walk 5.png').convert_alpha(), (200, 200)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Walk/walk 6.png').convert_alpha(), (200, 200)))
        for frame in self.walk_left_frames:
            self.walk_right_frames.append(pygame.transform.flip(frame, True, False))

        # attack one frames
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack One/attack 1.png').convert_alpha(), (200, 200)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack One/attack 2.png').convert_alpha(), (200, 200)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack One/attack 3.png').convert_alpha(), (200, 200)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack One/attack 4.png').convert_alpha(), (200, 200)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack One/attack 5.png').convert_alpha(), (200, 200)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack One/attack 6.png').convert_alpha(), (200, 200)))
        for frame in self.attack_one_left_frames:
            self.attack_one_right_frames.append(pygame.transform.flip(frame, True, False))

        # attack two frames
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Two/attack 1.png').convert_alpha(), (200, 200)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Two/attack 2.png').convert_alpha(), (200, 200)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Two/attack 3.png').convert_alpha(), (200, 200)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Two/attack 4.png').convert_alpha(), (200, 200)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Two/attack 5.png').convert_alpha(), (200, 200)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Two/attack 6.png').convert_alpha(), (200, 200)))
        for frame in self.attack_two_left_frames:
            self.attack_two_right_frames.append(pygame.transform.flip(frame, True, False))

        # attack three frames
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Three/attack 1.png').convert_alpha(), (200, 200)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Three/attack 2.png').convert_alpha(), (200, 200)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Three/attack 3.png').convert_alpha(), (200, 200)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Three/attack 4.png').convert_alpha(), (200, 200)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Three/attack 5.png').convert_alpha(), (200, 200)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Three/attack 6.png').convert_alpha(), (200, 200)))
        for frame in self.attack_three_left_frames:
            self.attack_three_right_frames.append(pygame.transform.flip(frame, True, False))

        # attack four frames
        self.attack_four_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Four/attack 1.png').convert_alpha(), (200, 200)))
        self.attack_four_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Four/attack 2.png').convert_alpha(), (200, 200)))
        self.attack_four_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Four/attack 3.png').convert_alpha(), (200, 200)))
        self.attack_four_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Four/attack 4.png').convert_alpha(), (200, 200)))
        self.attack_four_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Four/attack 5.png').convert_alpha(), (200, 200)))
        self.attack_four_left_frames.append(pygame.transform.scale(pygame.image.load('./LevelOne/images/boss/Attack Four/attack 6.png').convert_alpha(), (200, 200)))
        for frame in self.attack_four_left_frames:
            self.attack_four_right_frames.append(pygame.transform.flip(frame, True, False))

        


        self.current_sprite = 0

        self.image = self.walk_right_frames[self.current_sprite]
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.rect.bottomleft = (x, y)

        self.move_speed = 1
        self.right = False
        self.starting_time= pygame.time.get_ticks()
        self.attacking = False

    
    def update(self):
        self.move()


    def move(self):
        attackNumber = random.randint(1, 3)
        timePassed = pygame.time.get_ticks() - self.starting_time
        # what should the system be for deciding when to attack ?
        # print(timePassed)


        if self.right:
            self.rect.centerx += self.move_speed
            if timePassed % 3000 > 0 and timePassed % 3000 < 100:
                self.attacking = True
                self.attack(attackNumber, 'right', 0.1)
            else:
                self.animate(self.walk_right_frames, 0.1)
            if self.rect.x > 600:
                self.right = False
        else:
            self.rect.x -= self.move_speed
            if timePassed % 3000 > 0 and timePassed % 3000 < 100 and timePassed > 200:
                self.attacking = True
                self.attack(attackNumber, 'left', 0.1)
            else:
                self.animate(self.walk_left_frames, 0.1)
            if self.rect.x < 0:
                self.right = True


    # right now, the attack animation is not functional as the animations 
    # move too fast, but there is a place to start working on it if you go 
    # to chatGPT and take a look at the stuff it said 
    def attack(self, number, orientation, speed):
        if number == 1 and orientation == 'left':
            self.animate(self.attack_one_left_frames, speed)
        elif number == 1 and orientation == 'right':
            self.animate(self.attack_one_right_frames, speed)
        elif number == 2 and orientation == 'left':
            self.animate(self.attack_two_left_frames, speed)
        elif number == 2 and orientation == 'right':
            self.animate(self.attack_two_right_frames, speed)
        elif number == 3 and orientation == 'left':
            self.animate(self.attack_three_left_frames, speed)
        elif number == 3 and orientation == 'right':
            self.animate(self.attack_three_right_frames, speed)


    def animate(self, sprite_list, speed):
        # loop through sprite list and change current sprite 
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
        
        self.image = sprite_list[int(self.current_sprite)]



# video tmx code
tmx_data = load_pygame('./levelOne/maps/levelOne.tmx')

# sprite group for collision detection
land_sprite_group = pygame.sprite.Group()
water_sprite_group = pygame.sprite.Group()



# cycle through all layers
for layer in tmx_data.visible_layers:
	# if layer.name in ('Floor', 'Plants and rocks', 'Pipes')

    print(layer.name)
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