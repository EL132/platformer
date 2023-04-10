import pygame, random, sys
from Levels.LevelOne.constants import WINDOW_WIDTH, WINDOW_HEIGHT

#Use 2D vectors
vector = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    # parameters are TBD for grass and water tiles
    def __init__(self, x, y, land_tiles):
        super().__init__()

        self.load_animation_sprites()

        # index of the current sprite 
        self.current_sprite = 0

        self.image = self.run_right_frames[self.current_sprite]
        # create a mask
        self.mask = pygame.mask.from_surface(self.image, 4)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

        # self.rect.bottomleft = (x, y)

        self.land_tiles = land_tiles

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
        self.leg_hitbox_rect = pygame.Rect(self.x, self.y, 34, 15)

        

        self.is_jumping = False
        self.is_attacking = False
        self.is_hurting = False
        self.is_dying = False
        self.is_sprinting = False
        self.started_hurting = False

        self.right = True

        self.attack_number = 1

        self.able_to_move = True

        self.axe_swing = pygame.mixer.Sound("./SFX/axe_swing.mp3")
        self.footstep = pygame.mixer.Sound("./SFX/footstep_two.wav")
        self.footstep.set_volume(0.3)

        self.temp_x = self.x

        self.is_on_grass = True

        self.reverse = False


    def update(self):
        self.move()
        self.check_collisions()
        self.check_animations()
        self.mask_maintenance()


    def check_animations(self):
        if self.is_jumping:
            if self.right:
                self.animate(self.jump_right_frames, 0.1)
            else:
                self.animate(self.jump_left_frames, 0.1)
        elif self.is_hurting:
            if self.right:
                self.animate(self.hurt_right_frames, 0.1)
            else:
                self.animate(self.hurt_left_frames, 0.1)
        elif self.is_attacking: # this is true right now  
            if self.right:
                if self.attack_number == 1:
                    self.animate(self.attack_one_right_frames, 0.1)
                elif self.attack_number == 2:
                    self.animate(self.attack_two_right_frames, 0.1)
            else:
                if self.attack_number == 1:
                    self.animate(self.attack_one_left_frames, 0.1)
                elif self.attack_number == 2:
                    self.animate(self.attack_two_left_frames, 0.1)
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
        # pygame.draw.lines(self.image, (255, 0, 0), True, self.mask_outline)


    def move(self):
        sprint_distance_footstep = 150
        walk_distance_footstep = 100

        if self.able_to_move:

            self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

            keys = pygame.key.get_pressed()

            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and keys[pygame.K_LSHIFT]:
                self.right = False
                self.is_sprinting = True
                if not self.is_jumping:
                    if abs(self.position.x - self.temp_x) > sprint_distance_footstep:
                        self.footstep.play()
                        self.temp_x = self.position.x
                if self.position.x < 0:
                    self.position.x = WINDOW_WIDTH
                self.acceleration.x = -1 * (self.HORIZONTAL_ACCELERATION + 0.2)
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and keys[pygame.K_LSHIFT]:
                self.right = True
                self.is_sprinting = True
                if not self.is_jumping:
                    if abs(self.position.x - self.temp_x) > sprint_distance_footstep:
                        self.footstep.play()
                        self.temp_x = self.position.x
                if self.position.x > WINDOW_WIDTH:
                    self.position.x = 0
                self.acceleration.x = 1 * (self.HORIZONTAL_ACCELERATION + 0.2)
            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]):
                self.right = False
                self.is_sprinting = False
                if not self.is_jumping:
                    if abs(self.position.x - self.temp_x) > walk_distance_footstep:
                        self.footstep.play()
                        self.temp_x = self.position.x
                if self.position.x < 0:
                    self.position.x = WINDOW_WIDTH
                self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                self.right = True
                self.is_sprinting = False
                # i only want to play the sound if the player is in contact with the grass
                if not self.is_jumping:
                # and self.is_on_grass:
                    if abs(self.position.x - self.temp_x) > walk_distance_footstep:
                        self.footstep.play()
                        self.temp_x = self.position.x
                if self.position.x > WINDOW_WIDTH:
                    self.position.x = 0
                self.acceleration.x = self.HORIZONTAL_ACCELERATION
            else:
                if self.velocity.x > 0:
                    self.right = True
                    self.is_sprinting = False
                    self.mask = self.mask.scale((64, 80))
                else:
                    self.right = False
                    self.is_sprinting = False

            # # calc new kinematic values 
            self.acceleration.x -= self.HORIZONTAL_FRICTION * self.velocity.x # this is for friction of the acceleration
            self.velocity += self.acceleration
            self.position += self.velocity + 0.5 * self.acceleration
            
            self.rect.bottomleft = self.position
            if self.right:
                self.leg_hitbox_rect.center = (self.position.x + 26, self.position.y - 6)
            else:
                self.leg_hitbox_rect.center = (self.position.x + 53, self.position.y - 6)

            if self.position.y > WINDOW_HEIGHT:
                self.position.y = self.y

    def check_collisions(self):
        for tile in self.land_tiles:  
            if self.leg_hitbox_rect.colliderect(tile.rect):
                if self.velocity.y > 0:
                    # this is where i changed the jumping back to false to prevent infinite jumping 
                    if self.is_jumping:
                        self.is_jumping = False
                    if self.is_sprinting:
                        self.position.y = tile.rect.top
                    else:
                        self.position.y = tile.rect.top + 1
                    self.velocity.y = 0
            # if self.rect.colliderect(tile.rect):
            #     self.is_on_grass = True
            # else:
            #     self.is_on_grass = False
            
            # print("on grass value: ", self.is_on_grass)


    def jump(self):
        self.is_jumping = True
        for tile in self.land_tiles:
            if self.leg_hitbox_rect.colliderect(tile.rect):
                self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED


    def animate(self, sprite_list, speed):
        if self.is_attacking:
            if self.current_sprite < len(sprite_list) - 1 and not self.reverse:
                self.current_sprite += speed
                if self.current_sprite > len(sprite_list) - 1:
                    self.current_sprite = 4.4
                    self.reverse = True
            else:    
                if self.reverse:
                    self.current_sprite -= (speed) * 2
                    if self.current_sprite < 0:
                        self.current_sprite = 0
                        self.is_attacking = False
                        self.reverse = False
        elif self.is_hurting:
            if self.started_hurting:
                self.current_sprite = 0
                self.started_hurting = False

            if self.current_sprite < len(sprite_list) - 1:
                self.current_sprite += speed
            else:
                self.current_sprite = 0
                self.is_hurting = False
        else:
            if self.current_sprite < len(sprite_list) - 1:
                self.current_sprite += speed
            else:    
                self.current_sprite = 0
                if self.is_hurting:
                    self.is_hurting = False
                if self.is_dying:
                    self.is_dying = False


        # YES, the problem is that the fifth sprite animation happens too quickly, so it looks jerky 
        if self.is_hurting and self.current_sprite > 2:
            self.current_sprite = 2
            self.is_hurting = False
        self.image = sprite_list[int(self.current_sprite)]

    
    def attack(self, number):
        # this if statement is needed so the user can't just spam the attack button to have the sound play 
        if not self.is_attacking:
            pygame.mixer.Sound.play(self.axe_swing)
        self.is_attacking = True
        self.attack_number = number

    
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
        self.hurt_right_frames = []
        self.hurt_left_frames = []

        self.death_right_frames = []
        self.death_left_frames = []

        self.attack_one_right_frames = []
        self.attack_one_left_frames = []

        self.attack_two_right_frames = []
        self.attack_two_left_frames = []


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
        self.hurt_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Hurt/hurt 1.png').convert_alpha(), (80, 80)))
        self.hurt_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Hurt/hurt 2.png').convert_alpha(), (80, 80)))
        self.hurt_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Hurt/hurt 3.png').convert_alpha(), (80, 80)))
        for frame in self.hurt_right_frames:
            self.hurt_left_frames.append(pygame.transform.flip(frame, True, False))

        # death frames
        self.death_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Death/death 1.png').convert_alpha(), (80, 80)))
        self.death_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Death/death 2.png').convert_alpha(), (80, 80)))
        self.death_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Death/death 3.png').convert_alpha(), (80, 80)))
        self.death_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Death/death 4.png').convert_alpha(), (80, 80)))
        self.death_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Death/death 5.png').convert_alpha(), (80, 80)))
        self.death_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Death/death 6.png').convert_alpha(), (80, 80)))
        for frame in self.death_right_frames:
            self.death_left_frames.append(pygame.transform.flip(frame, True, False))

        #attack one frames
        self.attack_one_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack One/attack 1.png').convert_alpha(), (80, 80)))
        self.attack_one_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack One/attack 2.png').convert_alpha(), (80, 80)))
        self.attack_one_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack One/attack 3.png').convert_alpha(), (80, 80)))
        self.attack_one_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack One/attack 4.png').convert_alpha(), (80, 80)))
        self.attack_one_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack One/attack 5.png').convert_alpha(), (80, 80)))
        self.attack_one_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack One/attack 6.png').convert_alpha(), (80, 80)))
        for frame in self.attack_one_right_frames:
            self.attack_one_left_frames.append(pygame.transform.flip(frame, True, False))

        # attack three frames
        self.attack_two_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Two/attack 1.png').convert_alpha(), (80, 80)))
        self.attack_two_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Two/attack 2.png').convert_alpha(), (80, 80)))
        self.attack_two_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Two/attack 3.png').convert_alpha(), (80, 80)))
        self.attack_two_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Two/attack 4.png').convert_alpha(), (80, 80)))
        self.attack_two_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Two/attack 5.png').convert_alpha(), (80, 80)))
        self.attack_two_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Attack Two/attack 6.png').convert_alpha(), (80, 80)))
        for frame in self.attack_two_right_frames:
            self.attack_two_left_frames.append(pygame.transform.flip(frame, True, False))

        # idle frames
        self.idle_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Idle/idle 1.png').convert_alpha(), (80, 80)))
        self.idle_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Idle/idle 2.png').convert_alpha(), (80, 80)))
        self.idle_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Idle/idle 3.png').convert_alpha(), (80, 80)))
        self.idle_right_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/player/Woodcutter/Idle/idle 4.png').convert_alpha(), (80, 80)))
        for frame in self.idle_right_frames:
            self.idle_left_frames.append(pygame.transform.flip(frame, True, False))