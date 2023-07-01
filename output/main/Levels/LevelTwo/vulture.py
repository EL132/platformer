import pygame

class Vulture(pygame.sprite.Sprite):
    def __init__(self, x, y, attack_timing, tiles):
        super().__init__()
        self.load_animation_sprites()
        
        self.current_sprite = 0
        self.enemy_id = 1 

        self.right = True
        self.image = self.walk_right_sprites[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.height = self.rect.height * 1.1
        self.mask = pygame.mask.from_surface(self.image, 4)

        self.collision_rect = self.rect.copy()
        self.collision_rect.width = self.rect.width * 1.15
        self.collision_rect.height = self.rect.height * 1.15
        self.collision_rect.x = self.rect.x - 10

        self.attack_timing = attack_timing

        self.attacking = False

        self.starting_time = pygame.time.get_ticks()
        # starting time used for posted up time
        self.postedUpStarting = pygame.time.get_ticks()
        self.timePassed = 0
        # variable to keep track of time passed for posted up variable
        self.postedUpTime = 0

        self.moving_down = True

        self.posted_up = False

        self.idle = False

        self.tiles = tiles

        # time spent posted up
        self.posted_up_time = 0

    
    def update(self):
        self.move()
        self.check_animations()
        self.check_posted_up()

    
    def check_posted_up(self):
        self.postedUpTime = pygame.time.get_ticks() - self.postedUpStarting

        if self.posted_up:
            self.posted_up_time = pygame.time.get_ticks() - self.postedUpStarting
            if self.posted_up_time > 5000:
                self.posted_up = False
                self.posted_up_time = 0

        for tile in self.tiles:  
            if self.rect.colliderect(tile.rect):
                if 0 < self.postedUpTime % 30000 and self.postedUpTime % 30000 < 5000 and self.postedUpTime > 1000 and self.rect.y < (tile.rect.y - 10) and ((340 < self.rect.x and self.rect.x < 512) or (640 < self.rect.x and self.rect.x < 812) or (0 < self.rect.x and self.rect.x < 172)):
                    self.posted_up = True     
                    self.rect.y = tile.rect.y - 43  

    def move(self):
        if not self.posted_up:
            # i just want the vulture to fly back and forth across the screen, left to right
            if self.rect.x + 1 > 760:
                self.right = False
            elif self.rect.x - 1 < 40:
                self.right = True
            
            if self.right:
                self.rect.x += 1
            else:
                self.rect.x -= 1

            if self.rect.y > 300:
                self.moving_down = False
            else:
                self.moving_down = True

            if self.moving_down:
                if 0 < self.timePassed % self.attack_timing and self.timePassed % self.attack_timing < 100:
                    self.rect.y += 1
            else:
                if 0 < self.timePassed % self.attack_timing and self.timePassed % self.attack_timing < 100:
                    self.rect.y -= 1


    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:    
            self.current_sprite = 0
            if self.attacking:
                self.attacking = False

        self.image = sprite_list[int(self.current_sprite)]

    
    def check_animations(self):
        self.timePassed = pygame.time.get_ticks() - self.starting_time

        if self.timePassed > self.attack_timing:
            self.attacking = True
            self.starting_time = pygame.time.get_ticks()

        if self.posted_up:
            if self.right:
                self.animate(self.idle_right_sprites, 0.07)
            else:
                self.animate(self.idle_left_sprites, 0.07)
        elif self.attacking:
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

        self.idle_left_sprites = []
        self.idle_right_sprites = []

        for i in range(1, 5):
            self.walk_left_sprites.append(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Walk/row-1-column-{i}.png"))
            self.walk_right_sprites.append(pygame.transform.flip(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Walk/row-1-column-{i}.png"), True, False))

            self.attack_left_sprites.append(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Attack/row-1-column-{i}.png"))
            self.attack_right_sprites.append(pygame.transform.flip(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Attack/row-1-column-{i}.png"), True, False))

            self.idle_left_sprites.append(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Idle/row-1-column-{i}.png"))
            self.idle_right_sprites.append(pygame.transform.flip(pygame.image.load(f"./Levels/LevelTwo/images/creeps/Vulture/Idle/row-1-column-{i}.png"), True, False))
