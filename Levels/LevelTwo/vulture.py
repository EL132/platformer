import pygame

class Vulture(pygame.sprite.Sprite):
    def __init__(self, x, y, attack_timing):
        super().__init__()
        self.load_animation_sprites()
        
        self.current_sprite = 0
        self.enemy_id = 1 

        self.right = True
        self.image = self.walk_right_sprites[0]

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


        self.idle = False

    
    def update(self):
        self.move()
        self.check_animations()
        

    def move(self):
        # i just want the vulture to fly back and forth across the screen, left to right
        if self.rect.x + 1 > 760:
            self.right = False
        elif self.rect.x - 1 < 40:
            self.right = True
        
        if self.right:
            self.rect.x += 1
        else:
            self.rect.x -= 1


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
                self.animate(self.walk_right_sprites, 0.1)
            else:
                self.animate(self.walk_left_sprites, 0.1)
    

    def load_animation_sprites(self):
        self.attack_left_sprites = []
        self.attack_right_sprites = []

        self.walk_left_sprites = []
        self.walk_right_sprites = []

        for i in range(1, 5):
            self.walk_left_sprites.append(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Walk/row-1-column-{i}.png"))
            self.walk_right_sprites.append(pygame.transform.flip(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Walk/row-1-column-{i}.png"), True, False))

            self.attack_left_sprites.append(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Attack/row-1-column-{i}.png"))
            self.attack_right_sprites.append(pygame.transform.flip(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Attack/row-1-column-{i}.png"), True, False))