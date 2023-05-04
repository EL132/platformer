import pygame, random



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

        self.attacking = False

        # self.is_hurting = False
        self.is_dying = False
        self.able_to_move = True

        self.head_rect = pygame.Rect(self.rect.x, self.rect.y, 64, 60)
        self.head_rect.width = 32
        self.head_rect.height = 32


    def update(self):
        self.move(self.move_speed)
        self.check_animations()
        self.collision_maintenance()
    

    def collision_maintenance(self):
        self.mask = pygame.mask.from_surface(self.image, 4)
        self.mask_outline = self.mask.outline() # this gives a list of points that are on the mask 
        

        if self.right:
            self.head_rect.x = self.rect.x + 25
        else:
            self.head_rect.x = self.rect.x + 92
        self.head_rect.y = self.rect.y + 45


    def move(self, speed):
        if self.able_to_move:
            if not self.attacking:
                if not self.right:
                    self.rect.x -= speed
                    if self.rect.x < 10:
                        self.right = True
                else:
                    self.rect.x += speed
                    if self.rect.x > 600:
                        self.right = False



    def check_animations(self):

        timePassed = pygame.time.get_ticks() - self.starting_time
        if self.attacking:
            print(self.current_sprite)

        # note: end conditions of rect.x prevents boss from attacking on side of the screen

        if timePassed % 3000 > 0 and timePassed % 3000 < 100 and timePassed > 1000:
            self.attacking = True
            self.current_sprite = 0

            # self.attack_number = random.randint(1, 2)
            self.attack_number = 1
            self.able_to_move = False


        if self.attacking:
            if self.attack_number == 1:
                if self.right:
                    self.animate(self.attack_one_right_frames, 0.1)
                else:
                    self.animate(self.attack_one_left_frames, 0.1)

        elif self.is_dying:
            if self.right:
                self.animate(self.death_right_frames, 0.1)
            else:
                self.animate(self.death_left_frames, 0.1)

        else:
            if self.right:
                self.animate(self.walk_right_frames, 0.05)
            else:
                self.animate(self.walk_left_frames, 0.05)            


    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

            if self.attacking:
                self.attacking = False
                self.able_to_move = True

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

        self.idle_left_frames = []
        self.idle_right_frames = []

        self.sneer_left_frames = []
        self.sneer_right_frames = []

        self.ball = pygame.image.load('./Levels/LevelTwo/images/boss/Ball.png').convert_alpha()


        # attack one frames
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 1/row-1-column-1.png').convert_alpha(), (120, 120)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 1/row-1-column-2.png').convert_alpha(), (120, 120)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 1/row-1-column-3.png').convert_alpha(), (120, 120)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 1/row-1-column-4.png').convert_alpha(), (120, 120)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 1/row-1-column-5.png').convert_alpha(), (120, 120)))
        self.attack_one_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 1/row-1-column-6.png').convert_alpha(), (120, 120)))
        for frame in self.attack_one_left_frames:
            self.attack_one_right_frames.append(pygame.transform.flip(frame, True, False))

        # attack two frames
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 2/row-1-column-1.png').convert_alpha(), (120, 120)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 2/row-1-column-2.png').convert_alpha(), (120, 120)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 2/row-1-column-3.png').convert_alpha(), (120, 120)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 2/row-1-column-4.png').convert_alpha(), (120, 120)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 2/row-1-column-5.png').convert_alpha(), (120, 120)))
        self.attack_two_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 2/row-1-column-6.png').convert_alpha(), (120, 120)))
        for frame in self.attack_two_left_frames:
            self.attack_two_right_frames.append(pygame.transform.flip(frame, True, False))

        # attack three frames
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 3/row-1-column-1.png').convert_alpha(), (120, 120)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 3/row-1-column-2.png').convert_alpha(), (120, 120)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 3/row-1-column-3.png').convert_alpha(), (120, 120)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 3/row-1-column-4.png').convert_alpha(), (120, 120)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 3/row-1-column-5.png').convert_alpha(), (120, 120)))
        self.attack_three_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 3/row-1-column-6.png').convert_alpha(), (120, 120)))
        for frame in self.attack_three_left_frames:
            self.attack_three_right_frames.append(pygame.transform.flip(frame, True, False)) 
        
        # attack four frames
        self.attack_four_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 4/row-1-column-1.png').convert_alpha(), (120, 120)))
        self.attack_four_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 4/row-1-column-2.png').convert_alpha(), (120, 120)))
        self.attack_four_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 4/row-1-column-3.png').convert_alpha(), (120, 120)))
        self.attack_four_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Attack 4/row-1-column-4.png').convert_alpha(), (120, 120)))
        for frame in self.attack_four_left_frames:
            self.attack_four_right_frames.append(pygame.transform.flip(frame, True, False))
        
        # death frames
        self.death_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Death/row-1-column-1.png').convert_alpha(), (120, 120)))
        self.death_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Death/row-1-column-2.png').convert_alpha(), (120, 120)))
        self.death_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Death/row-1-column-3.png').convert_alpha(), (120, 120)))
        self.death_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Death/row-1-column-4.png').convert_alpha(), (120, 120)))
        self.death_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Death/row-1-column-5.png').convert_alpha(), (120, 120)))
        self.death_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Death/row-1-column-6.png').convert_alpha(), (120, 120)))
        for frame in self.death_left_frames:
            self.death_right_frames.append(pygame.transform.flip(frame, True, False))
        

        # idle frames
        self.idle_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Idle/row-1-column-1.png').convert_alpha(), (120, 120)))
        self.idle_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Idle/row-1-column-2.png').convert_alpha(), (120, 120)))
        self.idle_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Idle/row-1-column-3.png').convert_alpha(), (120, 120)))
        self.idle_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Idle/row-1-column-4.png').convert_alpha(), (120, 120)))
        for frame in self.idle_left_frames:
            self.idle_right_frames.append(pygame.transform.flip(frame, True, False))

        
        # sneer frames
        self.sneer_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Sneer/row-1-column-1.png').convert_alpha(), (120, 120)))
        self.sneer_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Sneer/row-1-column-2.png').convert_alpha(), (120, 120)))
        self.sneer_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Sneer/row-1-column-3.png').convert_alpha(), (120, 120)))
        self.sneer_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Sneer/row-1-column-4.png').convert_alpha(), (120, 120)))
        self.sneer_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Sneer/row-1-column-5.png').convert_alpha(), (120, 120)))
        self.sneer_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Sneer/row-1-column-6.png').convert_alpha(), (120, 120)))
        for frame in self.sneer_left_frames:
            self.sneer_right_frames.append(pygame.transform.flip(frame, True, False))


        # walk frames
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Walk/row-1-column-1.png').convert_alpha(), (120, 120)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Walk/row-1-column-2.png').convert_alpha(), (120, 120)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Walk/row-1-column-3.png').convert_alpha(), (120, 120)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Walk/row-1-column-4.png').convert_alpha(), (120, 120)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Walk/row-1-column-5.png').convert_alpha(), (120, 120)))
        self.walk_left_frames.append(pygame.transform.scale(pygame.image.load('./Levels/LevelTwo/images/boss/Walk/row-1-column-6.png').convert_alpha(), (120, 120)))
        for frame in self.walk_left_frames:
            self.walk_right_frames.append(pygame.transform.flip(frame, True, False))