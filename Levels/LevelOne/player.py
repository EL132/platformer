import pygame, random, sys
from constants import WINDOW_WIDTH, WINDOW_HEIGHT

#Use 2D vectors
vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    # parameters are TBD for grass and water tiles
    def __init__(self, x, y, land_tiles, water_tiles):
        super().__init__()

        self.load_animation_sprites()

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

        # create a mask
        self.mask = pygame.mask.from_surface(self.image, 4)

        self.is_jumping = False

        self.right = True


    def update(self):
        self.move()
        self.check_collisions()
        self.check_animations()
        self.mask_maintenance()


    def check_animations(self):
        if self.is_jumping:
            self.jump()
        else:
            keys = pygame.key.get_pressed()
            
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and keys[pygame.K_LSHIFT]:
                self.animate(self.run_left_frames, 0.1)
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and keys[pygame.K_LSHIFT]:
                self.animate(self.run_right_frames, 0.1)
            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]):
                self.animate(self.walk_left_frames, 0.1)
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                self.animate(self.walk_right_frames, 0.1)    
            else:
                if self.velocity.x > 0:
                    self.animate(self.idle_right_frames, 0.05)
                else:
                    self.animate(self.idle_left_frames, 0.05)


    def mask_maintenance(self):
        self.mask = pygame.mask.from_surface(self.image, 4)
        self.mask_outline = self.mask.outline() # this gives a list of points that are on the mask 
        self.mask = self.mask.scale((64, 80))
        pygame.draw.lines(self.image, (255, 0, 0), True, self.mask_outline)


    def move(self):
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        # for collision improvements
        self.leg_hitbox_rect.centery = self.position.y - 16
        left = False
        if left:
            self.leg_hitbox_rect.centerx = self.position.x + 6
        else:
            self.leg_hitbox_rect.centerx = self.position.x + 36


        keys = pygame.key.get_pressed()

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and keys[pygame.K_LSHIFT]:
            self.right = False
            if self.position.x < 0:
                self.position.x = WINDOW_WIDTH
            self.acceleration.x = -1 * (self.HORIZONTAL_ACCELERATION + 0.2)
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and keys[pygame.K_LSHIFT]:
            self.right = True
            if self.position.x < 0:
                self.position.x = WINDOW_WIDTH
            self.acceleration.x = 1 * (self.HORIZONTAL_ACCELERATION + 0.2)
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.right = False
            if self.position.x < 0:
                self.position.x = WINDOW_WIDTH
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.right = True
            if self.position.x > WINDOW_WIDTH:
                self.position.x = 0
            self.acceleration.x = self.HORIZONTAL_ACCELERATION    
        else:
            if self.velocity.x > 0:
                self.right = True
                self.mask = self.mask.scale((64, 80))
                pygame.draw.lines(self.image, (255, 0, 0), True, self.mask_outline)  
            else:
                self.right = False

        # # calc new kinematic values 
        self.acceleration.x -= self.HORIZONTAL_FRICTION * self.velocity.x # this is for friction of the acceleration
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration
        
        self.rect.bottomleft = self.position

        if self.position.y > WINDOW_HEIGHT:
            self.position.y = self.y

    def check_collisions(self):
        for tile in self.land_tiles:  
            if pygame.sprite.collide_mask(self, tile):
                tile.mask = pygame.mask.from_surface(tile.image)
                tile_mask_outline = tile.mask.outline() # this gives a list of points that are on
                if self.velocity.y > 0:
                    # this is where i changed the jumping back to false to prevent infinite jumping 
                    if self.is_jumping:
                        self.is_jumping = False     
                    self.position.y = tile.rect.top + 1
                    self.velocity.y = 0
        for tile in self.water_tiles:  
            if pygame.sprite.collide_mask(self, tile):
                self.position.x = self.x
                self.position.y = self.y
    
    def jump(self):
        if pygame.sprite.spritecollide(self, self.land_tiles, False):
            if self.right:
                self.animate(self.jump_right_frames, 0.1)
            else:
                self.animate(self.jump_left_frames, 0.1)
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED

    def animate(self, sprite_list, speed):
        # speed parameter used to limit how fast the animation goes 

        # loop through sprite list and change current sprite 
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
        
        self.image = sprite_list[int(self.current_sprite)]

    
    def load_animation_sprites(self):
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
        self.walk_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Walk/walk 1.png').convert_alpha(), (80, 80)))
        self.walk_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Walk/walk 2.png').convert_alpha(), (80, 80)))
        self.walk_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Walk/walk 3.png').convert_alpha(), (80, 80)))
        self.walk_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Walk/walk 4.png').convert_alpha(), (80, 80)))
        self.walk_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Walk/walk 5.png').convert_alpha(), (80, 80)))
        self.walk_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Walk/walk 6.png').convert_alpha(), (80, 80)))
        for frame in self.walk_right_frames:
            self.walk_left_frames.append(pygame.transform.flip(frame, True, False))

        # run frames 
        self.run_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Run/run 1.png').convert_alpha(), (80, 80)))
        self.run_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Run/run 2.png').convert_alpha(), (80, 80)))
        self.run_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Run/run 3.png').convert_alpha(), (80, 80)))
        self.run_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Run/run 4.png').convert_alpha(), (80, 80)))
        self.run_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Run/run 5.png').convert_alpha(), (80, 80)))
        self.run_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Run/run 6.png').convert_alpha(), (80, 80)))
        for frame in self.run_right_frames:
            self.run_left_frames.append(pygame.transform.flip(frame, True, False))

        # jump frames 
        self.jump_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Jump/jump 1.png').convert_alpha(), (80, 80)))
        self.jump_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Jump/jump 2.png').convert_alpha(), (80, 80)))
        self.jump_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Jump/jump 3.png').convert_alpha(), (80, 80)))
        self.jump_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Jump/jump 4.png').convert_alpha(), (80, 80)))
        self.jump_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Jump/jump 5.png').convert_alpha(), (80, 80)))
        self.jump_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Jump/jump 6.png').convert_alpha(), (80, 80)))
        for frame in self.jump_right_frames:
            self.jump_left_frames.append(pygame.transform.flip(frame, True, False))

        # hurt frames
        self.hurt_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Hurt/hurt 1.png').convert_alpha(), (80, 80)))
        self.hurt_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Hurt/hurt 2.png').convert_alpha(), (80, 80)))
        self.hurt_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Hurt/hurt 3.png').convert_alpha(), (80, 80)))

        # death frames
        self.death_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Death/death 1.png').convert_alpha(), (80, 80)))
        self.death_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Death/death 2.png').convert_alpha(), (80, 80)))
        self.death_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Death/death 3.png').convert_alpha(), (80, 80)))
        self.death_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Death/death 4.png').convert_alpha(), (80, 80)))
        self.death_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Death/death 5.png').convert_alpha(), (80, 80)))
        self.death_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Death/death 6.png').convert_alpha(), (80, 80)))

        #attack one frames
        self.attack_one_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack One/attack 1.png').convert_alpha(), (80, 80)))
        self.attack_one_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack One/attack 2.png').convert_alpha(), (80, 80)))
        self.attack_one_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack One/attack 3.png').convert_alpha(), (80, 80)))
        self.attack_one_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack One/attack 4.png').convert_alpha(), (80, 80)))
        self.attack_one_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack One/attack 5.png').convert_alpha(), (80, 80)))
        self.attack_one_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack One/attack 6.png').convert_alpha(), (80, 80)))

        # attack two frames
        self.attack_two_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Two/attack 1.png').convert_alpha(), (80, 80)))
        self.attack_two_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Two/attack 2.png').convert_alpha(), (80, 80)))
        self.attack_two_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Two/attack 3.png').convert_alpha(), (80, 80)))
        self.attack_two_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Two/attack 4.png').convert_alpha(), (80, 80)))
        self.attack_two_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Two/attack 5.png').convert_alpha(), (80, 80)))
        self.attack_two_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Two/attack 6.png').convert_alpha(), (80, 80)))

        # attack three frames
        self.attack_three_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Three/attack 1.png').convert_alpha(), (80, 80)))
        self.attack_three_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Three/attack 2.png').convert_alpha(), (80, 80)))
        self.attack_three_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Three/attack 3.png').convert_alpha(), (80, 80)))
        self.attack_three_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Three/attack 4.png').convert_alpha(), (80, 80)))
        self.attack_three_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Three/attack 5.png').convert_alpha(), (80, 80)))
        self.attack_three_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Three/attack 6.png').convert_alpha(), (80, 80)))

        # idle frames
        self.idle_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Idle/idle 1.png').convert_alpha(), (80, 80)))
        self.idle_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Idle/idle 2.png').convert_alpha(), (80, 80)))
        self.idle_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Idle/idle 3.png').convert_alpha(), (80, 80)))
        self.idle_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Idle/idle 4.png').convert_alpha(), (80, 80)))
        for frame in self.idle_right_frames:
            self.idle_left_frames.append(pygame.transform.flip(frame, True, False))