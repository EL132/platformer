import pygame, time, random, math
from pytmx.util_pygame import load_pygame


from tile import Tile

from player import Player
from boss import Boss
from grunt import Grunt
from snake import Snake
from vulture import Vulture

pygame.init()

# game setup
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 448

global transition
transition = False

FPS      = 60
TILESIZE = 32

global game_state
game_state = -1

global next_game_state
next_game_state = -1

global difficulty
difficulty = 2

global save_level
save_level = 0

global level_one_score
level_one_score = 0

global level_two_score
level_two_score = 0

global leaving_level
leaving_level = False

#colors 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

sprite_group = pygame.sprite.Group()

# video tmx code
tmx_data = load_pygame('./Levels/levelTwo/maps/LevelTwo.tmx')

# save_load_manager = SaveLoadSystem(".save", "save_data")

# level_two_score = save_load_manager.load_game_data(["level_two_score"], [0])

land_sprite_group = pygame.sprite.Group()

sprite_group = pygame.sprite.Group()

display_surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("tile map!")

# cycle through all layers
for layer in tmx_data.visible_layers:
    if hasattr(layer,'data'):
        for x, y, surf in layer.tiles():
            pos = (x * 32, y * 32)
            temp = Tile(pos = pos, surf = surf, groups = sprite_group)
            if layer.name in ('Main'):
                land_sprite_group.add(temp)

class LevelTwo():
    def __init__(self):
        self.player = Player(164, 290, land_sprite_group)
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.player_lives = 3

        self.custom_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 32)
        self.medium_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 40)
        self.title_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 64)

        self.boss = Boss(650, 385)
        self.boss_group = pygame.sprite.Group()
        self.boss_group.add(self.boss)

        self.creeper_group = pygame.sprite.Group()
        self.vulture_group = pygame.sprite.Group()
        self.creeper_one = Snake(100, 145, 3500, self.player, 'left')
        self.creeper_two = Snake(670, 145, 2500, self.player, 'right')
        self.vulture = Vulture(20, 6, 3500, land_sprite_group)
        self.creeper_group.add(self.creeper_one)
        self.creeper_group.add(self.creeper_two)
        self.vulture_group.add(self.vulture)

        self.grunt_group = pygame.sprite.Group()
        self.grunt_one = Grunt(DISPLAY_WIDTH, 0, 'right', 3500, land_sprite_group)

        self.heart = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/heart.png").convert_alpha(), (48, 48))
        self.boss_health = 1

        self.oof = pygame.mixer.Sound("./SFX/oof.wav")

        self.loaded_up = False
        self.starting_time = time.time()

        self.display_time = 0

        self.score = 0

        self.flashing_red = False
        self.word_present = False
        self.displaying_word = False

        self.word_draw_start_time = 0

        self.spawned = False

    def update(self):
        if self.loaded_up:
            self.starting_time = time.time()
            self.loaded_up = False
        self.check_game_over()
        self.draw_hearts()
        self.draw_health_bar()
        self.draw_time()
        self.draw_portrait()
        self.check_collisions(self.player, self.boss, self.creeper_one, self.creeper_two)
        self.check_grunt_spawn()
        self.boss_spawn_grunt()
        if self.displaying_word:
            self.draw_word()
        if len(self.boss.ball_group) > 0:
            for ball in self.boss.ball_group:
                self.check_ball_collisions(ball)

    def check_ball_collisions(self, ball):
        if self.player.is_rolling:
            if ball.rect.colliderect(self.player.leg_hitbox_rect):
                self.player_lives -= 1
                self.oof.play()
                ball.kill()
        else:
            if pygame.sprite.collide_rect(ball, self.player):
                self.player_lives -= 1
                self.oof.play()
                ball.kill()

    def boss_spawn_grunt(self):
        if self.boss.attack_number == 1 and self.boss.current_sprite > 5 and self.boss.attacking:
            if self.boss.right:
                self.spawn_grunt(self.boss.rect.x + 65, 350, random.choice(['left', 'right']), random.randint(2000, 5000))
            else:
                self.spawn_grunt(self.boss.rect.x, 350, random.choice(['left', 'right']), random.randint(2000, 5000))

    def check_grunt_spawn(self):
        if int(self.display_time) % 7 == 0 and self.spawned == False and len(self.grunt_group) < 2:
            self.spawn_grunt(random.randint(DISPLAY_WIDTH // 2 - 20, DISPLAY_WIDTH // 2 + 80), 0, random.choice(['left', 'right']), random.randint(2000, 5000))
            self.spawned = True
        if int(self.display_time) % 7 != 0:
            self.spawned = False

    def spawn_grunt(self, x, y, direction, attack_timing):
        grunt = Grunt(x, y, direction, attack_timing, land_sprite_group)
        self.grunt_group.add(grunt)

    def draw_portrait(self):
        portrait = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/player/Woodcutter/portrait.png").convert_alpha(), (48, 48))
        portrait_rect = portrait.get_rect()
        portrait_rect.topleft = (0, 0)
        screen.blit(portrait, portrait_rect)


    def draw_time(self):
        self.display_time = time.time() - self.starting_time
        self.display_time = round(self.display_time)
        

        if self.display_time == 0:
            self.display_time = "0000"
        elif self.display_time < 10:
            self.display_time = "000" + str(self.display_time)
        elif self.display_time < 100:
            self.display_time = "00" + str(self.display_time)
        elif self.display_time < 1000:
            self.display_time = "0" + str(self.display_time)
        

        time_text = self.medium_font.render("TIME  " + str(self.display_time), True, (255, 255, 255))
        time_rect = time_text.get_rect()
        time_rect.center = (DISPLAY_WIDTH - 95, 20)
        
        screen.blit(time_text, time_rect)


    def draw_health_bar(self):
        left_shift = 30
        right_shift = 35

        if self.boss.right:
            pygame.draw.line(screen, (0, 0, 0), (self.boss.rect.x - right_shift, self.boss.rect.y + 10), (self.boss.rect.x + 145, self.boss.rect.y + 10), 2)
            pygame.draw.line(screen, (0, 0, 0), (self.boss.rect.x - right_shift, self.boss.rect.y + 30), (self.boss.rect.x + 145, self.boss.rect.y + 30), 2)
            pygame.draw.line(screen, (0, 0, 0), (self.boss.rect.x - right_shift, self.boss.rect.y + 10), (self.boss.rect.x - right_shift, self.boss.rect.y + 30), 2)
            pygame.draw.line(screen, (0, 0, 0), (self.boss.rect.x + 145, self.boss.rect.y + 10), (self.boss.rect.x + 145, self.boss.rect.y + 30), 2)
        
            # fill for the health bar: 
            if time.time() - self.word_draw_start_time < 0.35:
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.boss.rect.x - (32), self.boss.rect.y + 13, 176 * self.boss_health, 16.5))
                self.flashing_red = False
            else:
                pygame.draw.rect(screen, (100, 255, 0), pygame.Rect(self.boss.rect.x - (right_shift - 3), self.boss.rect.y + 13, 176 * self.boss_health, 16.5))
        else:
            pygame.draw.line(screen, (0, 0, 0), (self.boss.rect.x + left_shift, self.boss.rect.y + 10), (self.boss.rect.x + 210, self.boss.rect.y + 10), 2)
            pygame.draw.line(screen, (0, 0, 0), (self.boss.rect.x + left_shift, self.boss.rect.y + 30), (self.boss.rect.x + 210, self.boss.rect.y + 30), 2)
            pygame.draw.line(screen, (0, 0, 0), (self.boss.rect.x + left_shift, self.boss.rect.y + 10), (self.boss.rect.x + left_shift, self.boss.rect.y + 30), 2)
            pygame.draw.line(screen, (0, 0, 0), (self.boss.rect.x + 210, self.boss.rect.y + 10), (self.boss.rect.x + 210, self.boss.rect.y + 30), 2)
        
            # outline for the health bar: 
            if time.time() - self.word_draw_start_time < 0.35:
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.boss.rect.x + (33), self.boss.rect.y + 13, 176 * self.boss_health, 16.5))
                self.flashing_red = False
            else:
                pygame.draw.rect(screen, (100, 255, 0), pygame.Rect(self.boss.rect.x + (left_shift + 3), self.boss.rect.y + 13, 176 * self.boss_health, 16.5))

    def boss_hurt(self, damage):
        self.boss_health -= damage
        self.flashing_red = True
        self.displaying_word = True
        self.word_draw_start_time = time.time()
        
        # Define the message to display
        if damage == 0.1:
            self.message = 'Critical Hit!'
        else:
            self.message = 'Hit big ole boss somewhere else'

    def draw_word(self):
        if time.time() - self.word_draw_start_time < 1:
            text = self.custom_font.render(self.message, True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (self.boss.rect.x + 120, self.boss.rect.y - 25)
            screen.blit(text, text_rect)
        else:
            self.displaying_word = False


    def draw_hearts(self):
        for i in range(1, 4):
            if math.ceil(self.player_lives) < i:
                self.heart = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/empty-heart.png").convert_alpha(), (48, 48))            
            elif self.player_lives % 1 != 0 and i == math.ceil(self.player_lives):
                self.heart = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/half-heart.png").convert_alpha(), (48, 48))
            else:
                self.heart = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/heart.png").convert_alpha(), (48, 48))

            self.heart_rect = self.heart.get_rect() # sets a rectangle that surrounds the surface, use this to position
            self.heart_rect.topleft = (10 + (i * 52), 0)
            screen.blit(self.heart, self.heart_rect)
    
        

    def check_collisions(self, player, boss, creeper_one, creeper_two):
        boss_list = pygame.sprite.groupcollide(self.boss_group, self.player_group, False, False, pygame.sprite.collide_mask)
        creeper_list = []
        for creeper in self.creeper_group:
            if pygame.Rect.colliderect(creeper.collision_rect, player.rect):
                creeper_list.append(creeper)
        grunt_list = []
        for grunt in self.grunt_group:
            if pygame.Rect.colliderect(grunt.collision_rect, player.rect):
                grunt_list.append(grunt)
        collision_list = []
        collision_list.extend(boss_list)
        collision_list.extend(creeper_list)
        collision_list.extend(grunt_list)

        for collided in collision_list:
            # print(collided.enemy_id)
            if player.is_attacking and not player.reverse:
                if (player.attack_number == 1 and player.current_sprite > 3.2 and player.current_sprite < 3.35) or (player.attack_number == 2 and player.current_sprite > 4.2 and player.current_sprite < 4.35):
                    # if self.collide_mask_rect(player.mask, boss.head_rect):
                    if player.collision_rect.colliderect(boss.head_rect):
                        self.boss_hurt(0.1)
                        boss.is_hurting = True
                    elif player.rect.colliderect(boss.rect):
                        self.boss_hurt(0.04)
                        boss.is_hurting = True

            
            for grunt in self.grunt_group:
                if player.is_attacking and grunt.collision_rect.colliderect(player.rect) and ((player.attack_number == 1 and player.current_sprite > 3.0 and player.current_sprite < 3.5) or (player.attack_number == 2 and player.current_sprite > 4.2 and player.current_sprite < 4.35)):
                    # had collidemask here before, but this colliderect is better for making it easier for the player to hit the grunt
                    grunt.health = 0
                elif pygame.sprite.collide_mask(player, grunt) and grunt.attacking and grunt.current_sprite > 3 and grunt.current_sprite < 3.1:
                    self.player_lives_update(0.5)
                    pass


            if boss.attacking and collided.enemy_id == 0:
                if boss.attacking and boss.current_sprite > 3.2 and boss.current_sprite < 3.3 and boss.attack_number != 1 and boss.attack_number != 4:
                    # print("special attack")
                    self.player_lives_update(1)
                

            elif (creeper_one.attacking or creeper_two.attacking) and collided.enemy_id == 1:
                if collided.current_sprite > 4 and collided.current_sprite < 4.1:
                    # way to verify that the chomper is facing the player 
                    if (collided.right and player.rect.x > collided.rect.x) or (not collided.right and player.rect.x < collided.rect.x):
                        self.player_lives_update(0.5)

    def check_game_over(self):
        if self.player_lives <= 0:
            self.player.is_dying = True
            self.player.able_to_move = False
            self.player_death_animation()
            self.show_player_loss_screen()
        elif self.boss_health <= 0.09:
            self.boss.is_dying = True
            self.boss.able_to_move = False
            self.boss_death_animation()
            save_level = 2
            self.show_player_win_screen()


    def player_death_animation(self):
        if self.player.right:
            death_frames = self.player.death_right_frames # a list of death frames
        else:
            death_frames = self.player.death_left_frames # a list of death frames
        delay = 200 # the delay between each frame in milliseconds

        for frame in death_frames:
            # currently have it so that everything goes away except the player 
            self.player.image = frame
            # redraw the screen
            self.player_group.draw(screen)
            pygame.display.flip()
            pygame.time.delay(delay)
            screen.fill('black')
            sprite_group.draw(screen)

    
    def boss_death_animation(self):
        # here i just want the player to go through a whole cycle of animations, and 
        # then i want the game to show the death screen 
        if self.boss.right:
            death_frames = self.boss.death_right_frames # a list of death frames
        else:
            death_frames = self.boss.death_left_frames # a list of death frames

        delay = 400 # the delay between each frame in milliseconds

        for frame in death_frames:
            # currently have it so that everything goes away except the player 
            self.boss.image = frame
            # redraw the screen
            self.boss_group.draw(screen)
            self.player_group.draw(screen)

            pygame.display.flip()
            pygame.time.delay(delay)
            screen.fill('black')
            sprite_group.draw(screen)

        # pause the animation for a few seconds
        pygame.time.wait(2000)


    def show_player_loss_screen(self):
        game_over = True

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        main_text = self.custom_font.render("GAME OVER", True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (DISPLAY_WIDTH//2, DISPLAY_HEIGHT//2)

        retry_text = self.custom_font.render("Press Y to retry", True, WHITE)
        exit_text = self.custom_font.render("Press N to exit", True, WHITE)

        retry_rect = retry_text.get_rect()
        retry_rect.center = (DISPLAY_WIDTH//2, DISPLAY_HEIGHT//2 + 50)

        exit_rect = exit_text.get_rect()
        exit_rect.center = (DISPLAY_WIDTH//2, DISPLAY_HEIGHT//2 + 100)

        #Display the pause text
        screen.fill(BLACK)
        screen.blit(main_text, main_rect)
        screen.blit(retry_text, retry_rect)
        screen.blit(exit_text, exit_rect)

        pygame.display.update()
        while game_over:
            pygame.mixer.music.stop()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        self.reset()
                        game_over = False
                    if event.key == pygame.K_n:
                        self.reset()
                        game_state = 0
                        transition = not transition
                        game_over = False
                if event.type == pygame.QUIT: 
                    pygame.quit()

    def show_player_win_screen(self):
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        game_over = True

        #Create main pause text
        main_text = self.title_font.render("YOU WON", True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (DISPLAY_WIDTH//2 + 15, DISPLAY_HEIGHT//2 - 150)

        new_high_score = False
        display_time = time.time() - self.starting_time
        # previous :
        if ((self.player_lives * 1000 - int(display_time) * 10) < 0):
            score = 0
        elif (self.player_lives * 1000 - int(display_time) * 10) > level_two_score:
            print("new high score!!!")
            new_high_score = True
            # score is their score during this round 
            score = self.player_lives * 1000 - (display_time) * 10
        else:
            score = self.player_lives * 1000 - (display_time) * 10
        
        screen.fill(BLACK)

        if new_high_score and level_two_score != 0:

            old_high_score_text = self.custom_font.render("OLD HIGH SCORE " + str(int(level_two_score)), True, WHITE)
            old_high_score_text_rect = old_high_score_text.get_rect()
            old_high_score_text_rect.center = (DISPLAY_WIDTH//2 + 20, DISPLAY_HEIGHT//2 - 75)

            new_high_score = self.custom_font.render("NEW HIGH SCORE " + str(int(score)), True, WHITE)
            new_high_score_rect = new_high_score.get_rect()
            new_high_score_rect.center = (DISPLAY_WIDTH//2 + 20, DISPLAY_HEIGHT//2 - 25)

            # save the new high score with the "score" variable
            level_two_score = score

            screen.blit(old_high_score_text, old_high_score_text_rect)
            screen.blit(new_high_score, new_high_score_rect)
        elif new_high_score and level_two_score == 0:
            print("inside second if")
            # if there is no old high score, i want it to say "your score: score"
            # and then underneath it, it will say "high score: score"
            player_score_text = self.custom_font.render("YOUR SCORE " + str(int(score)), True, WHITE)
            player_score_text_rect = player_score_text.get_rect()
            player_score_text_rect.center = (DISPLAY_WIDTH//2 + 20, DISPLAY_HEIGHT//2 - 75)

            high_score_text = self.custom_font.render("HIGH SCORE " + str(int(score)), True, WHITE)
            high_score_text_rect = high_score_text.get_rect()
            high_score_text_rect.center = (DISPLAY_WIDTH//2 + 20, DISPLAY_HEIGHT//2 - 25)

            level_two_score = score

            screen.blit(player_score_text, player_score_text_rect)
            screen.blit(high_score_text, high_score_text_rect)
        else:
            print("inside else")
            # if there is no new high score, i want it to say "your score: score"
            # and then underneath it, it will say "high score: score"
            player_score_text = self.custom_font.render("YOUR SCORE " + str(int(score)), True, WHITE)
            player_score_text_rect = player_score_text.get_rect()
            player_score_text_rect.center = (DISPLAY_WIDTH//2 + 20, DISPLAY_HEIGHT//2 - 75)

            high_score_text = self.custom_font.render("HIGH SCORE " + str(int(level_two_score)), True, WHITE)
            high_score_text_rect = high_score_text.get_rect()
            high_score_text_rect.center = (DISPLAY_WIDTH//2 + 20, DISPLAY_HEIGHT//2 - 25)

            screen.blit(player_score_text, player_score_text_rect)
            screen.blit(high_score_text, high_score_text_rect)
        

        # save_load_manager.save_game_data([level_two_score], ["level_two_score"])

        continue_text = self.custom_font.render("PRESS ENTER TO CONTINUE", True, WHITE)
        continue_rect = main_text.get_rect()
        continue_rect.center = (DISPLAY_WIDTH//2 - 55, DISPLAY_HEIGHT//2 + 100)
        
        #Display the pause text
        screen.blit(main_text, main_rect)
        screen.blit(continue_text, continue_rect)
        

        pygame.display.update()
        while game_over:
            for event in pygame.event.get():    
                #User wants to quit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # THIS SHOULD GO TO THE LEVEL SELECTOR
                        # save_load_manager.save_game_data([level_two_score], ["level_two_score"])
                        
                        pygame.mixer.music.stop()

                        next_game_state = 0
                        transition = True
                        pygame.image.save(screen,"screenshot.jpg")
                        game_over = False

    def reset(self):
        self.player_lives = 3
        self.boss_health = 1
        self.boss.rect.bottomleft = (600, 385)
        self.player.position = (164, 164)
        self.player.able_to_move = True
        self.player.is_hurting = False
        self.player.is_attacking = False
        self.boss.is_dying = False
        self.boss.able_to_move = True
        self.boss.is_hurting = False
        self.boss.attacking = False
        self.starting_time = time.time()
        self.grunt_group = pygame.sprite.Group()

    
    def player_lives_update(self, lives):
        pygame.mixer.Sound.play(self.oof)
        self.player_lives -= lives
        self.update_needed = True

    def blurSurf(self, surface, amt):
        if amt < 1.0:
            raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
        scale = 1.0/float(amt)
        surf_size = surface.get_size()
        scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
        surf = pygame.transform.smoothscale(surface, scale_size)
        surf = pygame.transform.smoothscale(surf, surf_size)
        return surf

    def pause_game(self, main_text, sub_text1, sub_text2):
        time_initial = time.time()

        # pygame.mixer.music.pause()

        #Set colors
        BLACK = (0, 0, 0, 0)
        GREEN = (25, 200, 25)
        WHITE = (255, 255, 255)

        #Create main pause text
        main_text = self.custom_font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (DISPLAY_WIDTH//2, DISPLAY_HEIGHT//2 - 100)

        #Create sub pause text
        sub_text1 = self.custom_font.render(sub_text1, True, WHITE)
        sub_rect1 = sub_text1.get_rect()
        sub_rect1.center = (DISPLAY_WIDTH//2, DISPLAY_HEIGHT//2 - 50)
        
        #Create sub pause text
        sub_text2 = self.custom_font.render(sub_text2, True, WHITE)
        sub_rect2 = sub_text2.get_rect()
        sub_rect2.center = (DISPLAY_WIDTH//2, DISPLAY_HEIGHT//2)

        # blurred_background = pygame.transform.box_blur(screen, 5)
        blurred_background = self.blurSurf(screen, 5)
        pygame.image.save(blurred_background, "./Levels/LevelOne/blurred.jpg")
        blurred_rect = blurred_background.get_rect(topleft = (0, 0))
        screen.blit(blurred_background, blurred_rect)

        #Display the pause text
        # screen.fill(BLACK)
        pygame.draw.rect(screen, BLACK, pygame.Rect(150, 80, 475, 180), 3)
        pygame.draw.line(screen, WHITE, (153, 150), (621, 150), 3)
        screen.blit(main_text, main_rect)
        screen.blit(sub_text1, sub_rect1)
        screen.blit(sub_text2, sub_rect2)
        pygame.display.update()

        # pygame.image.save(self.screen,"screenshot.jpg")

        #Pause the game until user hits enter or quits
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #User wants to continue
                    if event.key == pygame.K_RETURN:
                        time_passed = time.time() - time_initial
                        self.display_time = int(self.display_time)
                        self.display_time -= time_passed
                        is_paused = False
                        self.starting_time = time.time()
                        # pygame.mixer.music.unpause()
                #User wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    pygame.quit()

    def run(self): 
        sprite_group.draw(screen)

        self.player_group.update()
        self.player_group.draw(screen)

        self.boss_group.update()
        self.boss_group.draw(screen)

        self.creeper_group.update()
        self.creeper_group.draw(screen)

        self.grunt_group.update(self.player)
        self.grunt_group.draw(screen)

        self.vulture_group.update()
        self.vulture_group.draw(screen)

        self.update()

levelTwo = LevelTwo()

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and levelTwo.player.is_attacking == False:
                levelTwo.player.jump()
            if event.key == pygame.K_ESCAPE:
                levelTwo.pause_game("Paused", "Press     escape     to     quit", "Press    enter     to     continue")
            if event.key == pygame.K_q:
                levelTwo.player.attack(1)
            if event.key == pygame.K_w:
                levelTwo.player.attack(2)
            if event.key == pygame.K_r:
                levelTwo.player.roll()
        if event.type == pygame.QUIT:
            running = False

    levelTwo.run()
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()