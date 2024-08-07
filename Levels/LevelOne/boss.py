import pygame, random
from GameSave.SaveLoadManager import SaveLoadSystem

save_load_manager = SaveLoadSystem(".save", "save_data")
difficulty = save_load_manager.load_game_data(["difficulty"], [2])

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()       

        self.load_animation_sprites()

        self.current_sprite = 0
        self.attack_number = 0
        self.enemy_id = 0

        self.image = self.walk_left_frames[self.current_sprite]
        self.mask = pygame.mask.from_surface(self.image, 4)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.rect.bottomleft = (x, y)

        self.move_speed = 1
        self.right = False
        self.starting_time = pygame.time.get_ticks()

        self.attacking_basic = False
        self.attacking_special = False

        # self.is_hurting = False
        self.is_dying = False
        self.able_to_move = True

        self.head_rect = pygame.Rect(self.rect.x, self.rect.y, 64, 60)
        self.butt_rect = pygame.Rect(self.rect.x, self.rect.y, 64, 60)


    def update(self):
        self.move(True, self.move_speed)
        self.check_animations()
        self.collision_maintenance()
        

    

    def collision_maintenance(self):
        self.mask = pygame.mask.from_surface(self.image, 4)
        self.mask_outline = self.mask.outline() # this gives a list of points that are on the mask 
        

        if self.right:
            self.head_rect.x = self.rect.x + 75
            self.butt_rect.x = self.rect.x + 5
        else:
            self.head_rect.x = self.rect.x + 60
            self.butt_rect.x = self.rect.x + 130
        self.head_rect.y = self.rect.y + 105
        self.butt_rect.y = self.rect.y + 125


    def move(self, animate, speed):
        if self.able_to_move:
            if not self.attacking_basic: 
                if self.right:
                    self.rect.centerx += speed
                    if animate:
                        self.animate(self.walk_right_frames, 0.125)

                    if self.rect.x > 600:
                        self.right = False
                else:
                    self.rect.x -= speed
                    if animate:
                        self.animate(self.walk_left_frames, 0.125)

                    if self.rect.x < 0:
                        self.right = True


    def check_animations(self):

        timePassed = pygame.time.get_ticks() - self.starting_time


        # note: end conditions of rect.x prevents boss from attacking on side of the screen
        if difficulty == 1:
            if timePassed % 12000 > 0 and timePassed % 12000 < 100 and timePassed > 1000 and not self.attacking_special:
                self.attacking_special = True
                self.current_sprite = 0
            elif timePassed % 6000 > 0 and timePassed % 6000 < 100 and timePassed > 1000 and not self.attacking_basic and not self.attacking_special:
                self.attacking_basic = True   
                self.current_sprite = 0

                self.attack_number = random.randint(1, 2)
        elif difficulty == 2:
            if timePassed % 9000 > 0 and timePassed % 9000 < 100 and timePassed > 1000 and not self.attacking_special:
                self.attacking_special = True
                self.current_sprite = 0
            elif timePassed % 4500 > 0 and timePassed % 4500 < 100 and timePassed > 1000 and not self.attacking_basic and not self.attacking_special:
                self.attacking_basic = True   
                self.current_sprite = 0

                self.attack_number = random.randint(1, 2)
        else:
            if timePassed % 6000 > 0 and timePassed % 6000 < 100 and timePassed > 1000 and not self.attacking_special:
                self.attacking_special = True
                self.current_sprite = 0
            elif timePassed % 3000 > 0 and timePassed % 3000 < 100 and timePassed > 1000 and not self.attacking_basic and not self.attacking_special:
                self.attacking_basic = True   
                self.current_sprite = 0

                self.attack_number = random.randint(1, 2)



        if self.attacking_special: 
            if self.right:
                self.attack_special('right', 0.01)
            else: 
                self.attack_special('left', 0.01)

        elif self.attacking_basic:
            if self.right:
                self.attack_basic(self.attack_number, 'right', 0.1)  
            else:    
                self.attack_basic(self.attack_number, 'left', 0.1)

        elif self.is_dying:
            if self.right:
                self.animate(self.death_right_frames, 0.1)
            else:
                self.animate(self.death_left_frames, 0.1)


    def attack_basic(self, attack_number, orientation, speed):
        if attack_number == 1:
            if orientation == 'left':
                self.animate(self.attack_one_left_frames, speed)
            elif orientation == 'right':
                self.animate(self.attack_one_right_frames, speed)
        elif attack_number == 2: 
            if orientation == 'left':
                self.animate(self.attack_two_left_frames, speed)
            elif orientation == 'right':
                self.animate(self.attack_two_right_frames, speed)


    def attack_special(self, orientation, speed): 
        if orientation == 'left':
            self.animate(self.attack_three_left_frames, speed)
            if self.current_sprite > 0 and self.current_sprite < 1:
                self.move(False, self.move_speed * 1.1)
            elif self.current_sprite > 1 and self.current_sprite < 2:
                self.move(False, self.move_speed * 1.3)
            elif self.current_sprite > 2 and self.current_sprite < 3:
                self.move(False, self.move_speed * 1.5)
            elif self.current_sprite > 3 and self.current_sprite < 4:
                self.move(False, self.move_speed * 1.7)
            elif self.current_sprite > 4 and self.current_sprite < 5:
                self.move(False, self.move_speed * 1.9)
            elif self.current_sprite > 5 and self.current_sprite < 6:
                self.move(False, self.move_speed * 2)  
        else:
            self.animate(self.attack_three_right_frames, speed)      
            if self.current_sprite > 0 and self.current_sprite < 1:
                self.move(False, self.move_speed * 1.1)
            elif self.current_sprite > 1 and self.current_sprite < 2:
                self.move(False, self.move_speed * 1.3)
            elif self.current_sprite > 2 and self.current_sprite < 3:
                self.move(False, self.move_speed * 1.5)
            elif self.current_sprite > 3 and self.current_sprite < 4:
                self.move(False, self.move_speed * 1.7)
            elif self.current_sprite > 4 and self.current_sprite < 5:
                self.move(False, self.move_speed * 1.9)
            elif self.current_sprite > 5 and self.current_sprite < 6:
                self.move(False, self.move_speed * 2)
            


    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

            if self.attacking_basic: 
                self.attacking_basic = False
            if self.attacking_special: 
                self.attacking_special = False

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

        self.death_left_frames = []
        self.death_right_frames = []


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

        # hurt frames
        # self.hurt_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Hurt/hurt 1.png').convert_alpha(), (200, 200)))
        # self.hurt_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Hurt/hurt 2.png').convert_alpha(), (200, 200)))
        # self.hurt_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Hurt/hurt 3.png').convert_alpha(), (200, 200)))
        # self.hurt_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Hurt/hurt 4.png').convert_alpha(), (200, 200)))
        # for frame in self.hurt_left_frames:
        #     self.hurt_right_frames.append(pygame.transform.flip(frame, True, False))
        
        # death frames
        self.death_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Death/death 1.png').convert_alpha(), (200, 200)))
        self.death_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Death/death 2.png').convert_alpha(), (200, 200)))
        self.death_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Death/death 3.png').convert_alpha(), (200, 200)))
        self.death_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Death/death 4.png').convert_alpha(), (200, 200)))
        self.death_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Death/death 5.png').convert_alpha(), (200, 200)))
        self.death_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelOne/images/boss/Death/death 6.png').convert_alpha(), (200, 200)))
        for frame in self.death_left_frames:
            self.death_right_frames.append(pygame.transform.flip(frame, True, False))