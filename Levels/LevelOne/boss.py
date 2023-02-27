import pygame, random
from constants import WINDOW_HEIGHT, WINDOW_WIDTH

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()       

        self.load_animation_sprites()

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

        self.set = 0

        self.mask = pygame.mask.from_surface(self.image, 4)

    
    def update(self):
        self.move()
        self.check_animations()
        self.mask_maintenance()

    
    def mask_maintenance(self):
        self.mask = pygame.mask.from_surface(self.image, 4)
        self.mask_outline = self.mask.outline() # this gives a list of points that are on the mask 
        # self.mask = self.mask.scale((64, 80))
        pygame.draw.lines(self.image, (255, 0, 0), True, self.mask_outline)


    def move(self):
        if not self.attacking and self.set is not 1 or self.set is not 2:

            timePassed = pygame.time.get_ticks() - self.starting_time

            # note: end conditions of rect.x prevents boss from attacking on side of the screen
            if timePassed % 3000 > 0 and timePassed % 3000 < 100 and not self.attacking and self.rect.x > 50 and self.rect.x < WINDOW_WIDTH - 50:
                self.attacking = True   
                self.set = random.randint(1, 3)

            if self.right:
                self.rect.centerx += self.move_speed
                if self.rect.x > 600:
                    self.right = False
            else:
                self.rect.x -= self.move_speed
                if self.rect.x < 0:
                    self.right = True


    def check_animations(self):
        if self.attacking:
            if self.right:
                self.attack(self.set, 'right', 0.1)  
            else:    
                self.attack(self.set, 'left', 0.1)
        else:
            if self.right: 
                self.animate(self.walk_right_frames, 0.1)
            else: 
                self.animate(self.walk_left_frames, 0.1)


    # right now, the attack animation is not functional as the animations 
    # move too fast, but there is a place to start working on it if you go 
    # to chatGPT and take a look at the stuff it said 
    def attack(self, number, orientation, speed):
        # print("inside attacking number",  number)
        if number == 1 and orientation == 'left':
            # print("inside one left")
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
            if self.attacking: 
                self.attacking = False

        self.image = sprite_list[int(self.current_sprite)]
    
    def load_animation_sprites(self):
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
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Walk/walk 1.png').convert_alpha(), (200, 200)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Walk/walk 2.png').convert_alpha(), (200, 200)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Walk/walk 3.png').convert_alpha(), (200, 200)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Walk/walk 4.png').convert_alpha(), (200, 200)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Walk/walk 5.png').convert_alpha(), (200, 200)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Walk/walk 6.png').convert_alpha(), (200, 200)))
        for frame in self.walk_left_frames:
            self.walk_right_frames.append(pygame.transform.flip(frame, True, False))

        # attack one frames
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack One/attack 1.png').convert_alpha(), (200, 200)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack One/attack 2.png').convert_alpha(), (200, 200)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack One/attack 3.png').convert_alpha(), (200, 200)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack One/attack 4.png').convert_alpha(), (200, 200)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack One/attack 5.png').convert_alpha(), (200, 200)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack One/attack 6.png').convert_alpha(), (200, 200)))
        for frame in self.attack_one_left_frames:
            self.attack_one_right_frames.append(pygame.transform.flip(frame, True, False))

        # attack two frames
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack Two/attack 1.png').convert_alpha(), (200, 200)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack Two/attack 2.png').convert_alpha(), (200, 200)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack Two/attack 3.png').convert_alpha(), (200, 200)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack Two/attack 4.png').convert_alpha(), (200, 200)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack Two/attack 5.png').convert_alpha(), (200, 200)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack Two/attack 6.png').convert_alpha(), (200, 200)))
        for frame in self.attack_two_left_frames:
            self.attack_two_right_frames.append(pygame.transform.flip(frame, True, False))

        # attack three frames
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack Three/attack 1.png').convert_alpha(), (200, 200)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack Three/attack 2.png').convert_alpha(), (200, 200)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack Three/attack 3.png').convert_alpha(), (200, 200)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack Three/attack 4.png').convert_alpha(), (200, 200)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack Three/attack 5.png').convert_alpha(), (200, 200)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Attack Three/attack 6.png').convert_alpha(), (200, 200)))
        for frame in self.attack_three_left_frames:
            self.attack_three_right_frames.append(pygame.transform.flip(frame, True, False)) 