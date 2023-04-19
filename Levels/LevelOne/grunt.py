import pygame, settings

vector = pygame.math.Vector2

class Grunt(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, attack_timing, tiles):
        super().__init__()
        self.load_animation_sprites()
        self.land_tiles = tiles
        self.current_sprite = 0
        self.x = x
        self.y = y

        self.direction = direction

        if self.direction == "right":
            self.image = self.walk_right_sprites[self.current_sprite]
            self.right = True
        else:
            self.image = self.walk_left_sprites[self.current_sprite]
            self.right = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image, 4)
        self.attack_timing = attack_timing
        self.VERTICAL_ACCELERATION = 0.25 # gravity 
        self.HORIZONTAL_FRICTION = 0.10 # friction
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        self.attacking = False

        self.starting_time = pygame.time.get_ticks()

        self.collision_occurred = False
    
    def update(self):
        self.check_animations()
        self.check_collisions()
        self.move()

    
    def move(self):
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)


        if self.position.y > settings.DISPLAY_HEIGHT - 100 and not self.attacking:
            # only if the grunt is on the ground should it be moving
            if self.direction == 'left':
                self.velocity.x = -1
            else:
                self.velocity.x = 1
        
        self.acceleration.x -= self.HORIZONTAL_FRICTION * self.velocity.x # this is for friction of the acceleration
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        if self.position.y > settings.DISPLAY_HEIGHT:
            self.position.y = self.y
        
        self.rect.bottomleft = self.position

    def check_collisions(self):
        for tile in self.land_tiles:  
            if self.rect.colliderect(tile.rect):
                if self.velocity.y > 0:
                    self.position.y = tile.rect.top + 1
                    self.velocity.y = 0


    def load_animation_sprites(self):
        self.attack_right_sprites = []
        self.attack_left_sprites = []

        self.walk_left_sprites = []
        self.walk_right_sprites = []

        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/attack/attack1.png').convert_alpha(),(60, 60)))
        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/attack/attack2.png').convert_alpha(),(60, 60)))
        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/attack/attack3.png').convert_alpha(),(60, 60)))
        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/attack/attack4.png').convert_alpha(),(60, 60)))
        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/attack/attack5.png').convert_alpha(),(60, 60)))
        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/attack/attack6.png').convert_alpha(),(60, 60)))
        for sprite in self.attack_left_sprites:
            self.attack_right_sprites.append(pygame.transform.flip(sprite, True, False))
        
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/walk/walk1.png').convert_alpha(),(60, 60)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/walk/walk2.png').convert_alpha(),(60, 60)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/walk/walk3.png').convert_alpha(),(60, 60)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/walk/walk4.png').convert_alpha(),(60, 60)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/walk/walk5.png').convert_alpha(),(60, 60)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/walk/walk6.png').convert_alpha(),(60, 60)))
        for sprite in self.walk_left_sprites:
            self.walk_right_sprites.append(pygame.transform.flip(sprite, True, False))
        

    def animate(self, sprite_list, speed):
        if self.position.y > settings.DISPLAY_HEIGHT - 100:
            if self.current_sprite < len(sprite_list) - 1:
                self.current_sprite += speed
            else:    
                self.current_sprite = 0
                if self.attacking:
                    self.attacking = False

            self.image = sprite_list[int(self.current_sprite)]


    
    def check_animations(self):
        timePassed = pygame.time.get_ticks() - self.starting_time

        if timePassed > self.attack_timing:
            self.attacking = True
            self.starting_time = pygame.time.get_ticks()

        if self.attacking:
            if self.right:
                self.animate(self.attack_right_sprites, 0.1)
            else:
                self.animate(self.attack_left_sprites, 0.1)
        else:
            if self.right:
                self.animate(self.walk_right_sprites, 0.07)
            else:
                self.animate(self.walk_left_sprites, 0.07)