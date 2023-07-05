import pygame

vector = pygame.math.Vector2

# game setup
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 448

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

        self.colliding_with_ground = False
    
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

            # if self.position.y > DISPLAY_HEIGHT:
            #     self.position.y = self.y
            
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



    def animate(self, sprite_list, speed):
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

        
    def load_animation_sprites(self):
        self.attack_right_sprites = []
        self.attack_left_sprites = []

        self.walk_left_sprites = []
        self.walk_right_sprites = []

        self.idle_left_sprites = []
        self.idle_right_sprites = []

        self.death_left_sprites = []
        self.death_right_sprites = []

        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Attack/row-1-column-1.png').convert_alpha(),(65, 65)))
        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Attack/row-1-column-2.png').convert_alpha(),(65, 65)))
        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Attack/row-1-column-3.png').convert_alpha(),(65, 65)))
        self.attack_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Attack/row-1-column-4.png').convert_alpha(),(65, 65)))
        for sprite in self.attack_left_sprites:
            self.attack_right_sprites.append(pygame.transform.flip(sprite, True, False))
        
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Walk/row-1-column-1.png').convert_alpha(),(65, 65)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Walk/row-1-column-2.png').convert_alpha(),(65, 65)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Walk/row-1-column-3.png').convert_alpha(),(65, 65)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Walk/row-1-column-4.png').convert_alpha(),(65, 65)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Walk/row-1-column-5.png').convert_alpha(),(65, 65)))
        self.walk_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Walk/row-1-column-6.png').convert_alpha(),(65, 65)))
        for sprite in self.walk_left_sprites:
            self.walk_right_sprites.append(pygame.transform.flip(sprite, True, False))

        self.idle_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Idle/row-1-column-1.png').convert_alpha(),(65, 65)))
        self.idle_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Idle/row-1-column-2.png').convert_alpha(),(65, 65)))
        self.idle_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Idle/row-1-column-3.png').convert_alpha(),(65, 65)))
        self.idle_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Idle/row-1-column-4.png').convert_alpha(),(65, 65)))
        for sprite in self.idle_left_sprites:
            self.idle_right_sprites.append(pygame.transform.flip(sprite, True, False))

        self.death_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Death/row-1-column-1.png').convert_alpha(),(65, 65)))
        self.death_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Death/row-1-column-2.png').convert_alpha(),(65, 65)))
        self.death_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Death/row-1-column-3.png').convert_alpha(),(65, 65)))
        self.death_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Death/row-1-column-4.png').convert_alpha(),(65, 65)))
        self.death_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Death/row-1-column-5.png').convert_alpha(),(65, 65)))
        self.death_left_sprites.append(pygame.transform.scale(pygame.image.load('./Levels/LevelThree/creeps/Snowy/Death/row-1-column-6.png').convert_alpha(),(65, 65)))
        for sprite in self.death_left_sprites:
            self.death_right_sprites.append(pygame.transform.flip(sprite, True, False))