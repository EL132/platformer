import pygame

class Vulture(pygame.sprite.Sprite):
    def __init__(self, x, y, attack_timing, player, area):
        super().__init__()
        self.load_animation_sprites()
        
        self.current_sprite = 0
        self.enemy_id = 1 

        self.right = True
        self.image = self.idle_right_sprites[0]

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

        self.player = player
        self.area = area

        self.idle = False

    
    def update(self):
        self.move(self.player)
        self.check_animations()
        

    def move(self, player):
        if self.area == 'right':
            if self.rect.x < 526:
                self.idle = True
            else:
                self.idle = False
                if self.rect.x > player.rect.x:
                    self.rect.x -= 1
                    self.right = False

            if self.rect.x < player.rect.x and self.rect.x + 1 < 768:
                self.rect.x += 1
                self.right = True
        elif self.area == 'left':
            if self.rect.x > 220:
                self.idle = True
            else:
                self.idle = False
                if self.rect.x < player.rect.x:
                    self.rect.x += 1
                    self.right = True
            if self.rect.x > player.rect.x and self.rect.x - 1 > 32:
                    self.rect.x -= 1
                    self.right = False


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
        elif self.idle:
            if self.right:
                self.animate(self.idle_right_sprites, 0.07)
            else:
                self.animate(self.idle_left_sprites, 0.07)
        else:
            if self.right:
                self.animate(self.walk_right_sprites, 0.1)
            else:
                self.animate(self.walk_left_sprites, 0.1)
    

    def load_animation_sprites(self):
        self.attack_left_sprites = []
        self.attack_right_sprites = []

        self.walk_left_sprites = []
        self.walk_right_sprites = []

        for i in range(1, 5):
            self.death_left_sprites.append(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Death/row-1-column-{i}.png"))
            self.death_right_sprites.append(pygame.transform.flip(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Death/row-1-column-{i}.png"), True, False))

            self.idle_left_sprites.append(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Idle/row-1-column-{i}.png"))
            self.idle_right_sprites.append(pygame.transform.flip(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Idle/row-1-column-{i}.png"), True, False))

            self.walk_left_sprites.append(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Walk/row-1-column-{i}.png"))
            self.walk_right_sprites.append(pygame.transform.flip(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Walk/row-1-column-{i}.png"), True, False))

        for i in range(1, 7):
            self.attack_left_sprites.append(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Attack/row-1-column-{i}.png"))
            self.attack_right_sprites.append(pygame.transform.flip(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Attack/row-1-column-{i}.png"), True, False))
