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
        self.health = 1

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

        self.collision_rect = self.rect.copy()
        self.collision_rect.width = self.rect.width * 1.15
        self.collision_rect.height = self.rect.height * 1.15
        self.collision_rect.x = self.rect.x - 10

        self.attacking = False

        self.starting_time = pygame.time.get_ticks()

        self.idle = False
        self.death_started = False

        self.enemy_id = 5
    
    def update(self, player):
        self.check_animations()
        self.check_collisions()
        self.move(player)
        if self.health == 0:
            self.die()

    def die(self):
        if not self.death_started:
            self.current_sprite = 0
            self.death_started = True
    
    def move(self, player):
        if self.health > 0:
            # want the grunt to move towards the player, but if the grunt is right next to the player, it should stop moving
            if self.position.x < player.position.x + 40 and self.position.x > player.position.x - 40:
                self.idle = True
                
                self.acceleration = vector(0, self.VERTICAL_ACCELERATION)
                self.velocity.y += self.acceleration.y
                self.position.y += self.velocity.y + 0.5 * self.acceleration.y
            else:
                self.idle = False
                if self.position.x < player.position.x:
                    self.direction = 'right'
                    self.right = True
                else:
                    self.direction = 'left'
                    self.right = False

                self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

                for tile in self.land_tiles:  
                    if self.rect.colliderect(tile.rect) and not self.attacking:
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
            self.collision_rect.bottomleft = self.position
        # else if the grunt is dying
        else:
            self.acceleration = vector(0, self.VERTICAL_ACCELERATION)
            self.velocity.y += self.acceleration.y
            self.position.y += self.velocity.y + 0.5 * self.acceleration.y
            
            self.rect.bottomleft = self.position
            self.collision_rect.bottomleft = self.position

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

        self.idle_left_sprites = []
        self.idle_right_sprites = []

        self.death_left_sprites = []
        self.death_right_sprites = []

        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/attack/attack1.png').convert_alpha(),(55, 55)))
        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/attack/attack2.png').convert_alpha(),(55, 55)))
        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/attack/attack3.png').convert_alpha(),(55, 55)))
        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/attack/attack4.png').convert_alpha(),(55, 55)))
        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/attack/attack5.png').convert_alpha(),(55, 55)))
        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/attack/attack6.png').convert_alpha(),(55, 55)))
        for sprite in self.attack_left_sprites:
            self.attack_right_sprites.append(pygame.transform.flip(sprite, True, False))
        
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/walk/walk1.png').convert_alpha(),(55, 55)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/walk/walk2.png').convert_alpha(),(55, 55)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/walk/walk3.png').convert_alpha(),(55, 55)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/walk/walk4.png').convert_alpha(),(55, 55)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/walk/walk5.png').convert_alpha(),(55, 55)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/walk/walk6.png').convert_alpha(),(55, 55)))
        for sprite in self.walk_left_sprites:
            self.walk_right_sprites.append(pygame.transform.flip(sprite, True, False))

        self.idle_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/Idle/idle1.png').convert_alpha(),(55, 55)))
        self.idle_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/Idle/idle2.png').convert_alpha(),(55, 55)))
        self.idle_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/Idle/idle3.png').convert_alpha(),(55, 55)))
        self.idle_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/Idle/idle4.png').convert_alpha(),(55, 55)))
        for sprite in self.idle_left_sprites:
            self.idle_right_sprites.append(pygame.transform.flip(sprite, True, False))

        self.death_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/death/death1.png').convert_alpha(),(55, 55)))
        self.death_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/death/death2.png').convert_alpha(),(55, 55)))
        self.death_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/death/death3.png').convert_alpha(),(55, 55)))
        self.death_left_sprites.append(pygame.transform.scale(pygame.image.load('Levels/LevelOne/images/creeps/person_melee/death/death4.png').convert_alpha(),(55, 55)))
        for sprite in self.death_left_sprites:
            self.death_right_sprites.append(pygame.transform.flip(sprite, True, False))


    def animate(self, sprite_list, speed):
        if self.position.y > settings.DISPLAY_HEIGHT - 100:
            if self.current_sprite < len(sprite_list) - 1:
                self.current_sprite += speed
            else:    
                self.current_sprite = 0
                if self.attacking:
                    self.attacking = False
                if self.death_started:
                    self.kill()

            self.image = sprite_list[int(self.current_sprite)]


    
    def check_animations(self):
        timePassed = pygame.time.get_ticks() - self.starting_time
        
        if timePassed > self.attack_timing:
            self.attacking = True
            self.starting_time = pygame.time.get_ticks()

        if self.death_started:
            if self.right:
                self.animate(self.death_right_sprites, 0.05)
            else:
                self.animate(self.death_left_sprites, 0.05)
        elif self.attacking:
            if self.right:
                self.animate(self.attack_right_sprites, 0.1)
            else:
                self.animate(self.attack_left_sprites, 0.1)
        else:
            if self.right:
                if self.idle:
                    self.animate(self.idle_right_sprites, 0.07)
                else:
                    self.animate(self.walk_right_sprites, 0.07)
            else:
                if self.idle:
                    self.animate(self.idle_left_sprites, 0.07)
                else:
                    self.animate(self.walk_left_sprites, 0.07)