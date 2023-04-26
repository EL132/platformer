import pygame

class MiniChomper(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, attack_timing):
        super().__init__()
        self.load_animation_sprites()
        
        self.current_sprite = 0
        self.enemy_id = 1 

        if direction == 'right':
            self.right = True
            self.image = self.idle_right_sprites[0]
        else:
            self.right = False
            self.image = self.idle_left_sprites[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image, 4)

        self.collision_rect = self.rect.copy()
        self.collision_rect.width = self.rect.width * 1.15
        self.collision_rect.height = self.rect.height * 1.15
        self.collision_rect.x = self.rect.x - 10

        self.attack_timing = attack_timing

        self.attacking = False

        self.starting_time = pygame.time.get_ticks()

    
    def update(self):
        self.check_animations()


    def load_animation_sprites(self):
        self.attack_right_sprites = []
        self.attack_left_sprites = []

        self.idle_left_sprites = []
        self.idle_right_sprites = []

        self.attack_left_sprites.append(pygame.image.load('Levels/LevelOne/images/creeps/mini_chomper/attack/attack1.png'))
        self.attack_left_sprites.append(pygame.image.load('Levels/LevelOne/images/creeps/mini_chomper/attack/attack2.png'))
        self.attack_left_sprites.append(pygame.image.load('Levels/LevelOne/images/creeps/mini_chomper/attack/attack3.png'))
        self.attack_left_sprites.append(pygame.image.load('Levels/LevelOne/images/creeps/mini_chomper/attack/attack4.png'))
        self.attack_left_sprites.append(pygame.image.load('Levels/LevelOne/images/creeps/mini_chomper/attack/attack5.png'))
        self.attack_left_sprites.append(pygame.image.load('Levels/LevelOne/images/creeps/mini_chomper/attack/attack6.png'))
        for sprite in self.attack_left_sprites:
            self.attack_right_sprites.append(pygame.transform.flip(sprite, True, False))
        
        self.idle_left_sprites.append(pygame.image.load('Levels/LevelOne/images/creeps/mini_chomper/idle/idle1.png'))
        self.idle_left_sprites.append(pygame.image.load('Levels/LevelOne/images/creeps/mini_chomper/idle/idle2.png'))
        self.idle_left_sprites.append(pygame.image.load('Levels/LevelOne/images/creeps/mini_chomper/idle/idle3.png'))
        self.idle_left_sprites.append(pygame.image.load('Levels/LevelOne/images/creeps/mini_chomper/idle/idle4.png'))
        for sprite in self.idle_left_sprites:
            self.idle_right_sprites.append(pygame.transform.flip(sprite, True, False))
        

    def animate(self, sprite_list, speed):
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
                self.animate(self.idle_right_sprites, 0.07)
            else:
                self.animate(self.idle_left_sprites, 0.07)