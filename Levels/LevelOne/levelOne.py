from colorsys import rgb_to_hls
import pygame, time, random, math
from pytmx.util_pygame import load_pygame
import settings


from GameSave.SaveLoadManager import SaveLoadSystem
from Levels.LevelOne.tile import Tile
from Levels.LevelOne.player import Player
from Levels.LevelOne.boss import Boss
from Levels.LevelOne.creeper import MiniChomper
from Levels.LevelOne.constants import *


display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

sprite_group = pygame.sprite.Group()

# video tmx code
tmx_data = load_pygame('./Levels/levelOne/maps/levelOne.tmx')

save_load_manager = SaveLoadSystem(".save", "save_data")

settings.level_one_score = save_load_manager.load_game_data(["level_one_score"], [0])


land_sprite_group = pygame.sprite.Group()

# cycle through all layers
for layer in tmx_data.visible_layers:
    if hasattr(layer,'data'):
        for x, y, surf in layer.tiles():
            # for tile in layer.tiles():
                # NOTE: here i need to check if the tile is an edge tile , use the ID of the edge tile to check this, just am not sure 
                # how to do that because the documentation is so shit and basic 
            pos = (x * 32, y * 32)
            temp = Tile(pos = pos, surf = surf, groups = sprite_group)
            if layer.name in ('Collisions'):
                land_sprite_group.add(temp)

class LevelOne():
    def __init__(self):
        self.player = Player(164, 164, land_sprite_group)
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.player_lives = 3

        self.custom_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 32)
        self.medium_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 40)
        self.title_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 64)

        self.boss_chomper = Boss(600, 385)
        self.boss_group = pygame.sprite.Group()
        self.boss_group.add(self.boss_chomper)

        self.creeper_group = pygame.sprite.Group()
        self.creeper_one = MiniChomper(500, 179, 'right', 3500)
        self.creeper_two = MiniChomper(200, 338, 'right', 2500)
        self.creeper_three = MiniChomper(690, 115, 'left', 4500)
        self.creeper_group.add(self.creeper_one)
        self.creeper_group.add(self.creeper_two)
        self.creeper_group.add(self.creeper_three)

        self.heart = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/heart.png").convert_alpha(), (48, 48))
        self.boss_health = 1

        self.oof = pygame.mixer.Sound("./SFX/oof.wav")

        # i want to play the level one background music when the user enters this level
        self.loaded_up = False
        self.starting_time = time.time()

        self.display_time = 0

        self.score = 0

        self.flashing_red = False
        self.word_present = False
        self.displaying_word = False

        self.word_draw_start_time = 0

    def update(self):
        if self.loaded_up:
            self.starting_time = time.time()
            self.loaded_up = False
        self.check_game_over()
        self.draw_hearts()
        self.draw_health_bar()
        self.draw_time()
        self.draw_portrait()
        self.check_collisions(self.player, self.boss_chomper, self.creeper_one, self.creeper_two, self.creeper_three)
        if self.displaying_word:
            self.draw_word()

    def draw_portrait(self):
        portrait = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/player/Woodcutter/portrait.png").convert_alpha(), (48, 48))
        portrait_rect = portrait.get_rect()
        portrait_rect.topleft = (0, 0)
        display_surface.blit(portrait, portrait_rect)


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
        time_rect.center = (WINDOW_WIDTH - 75, 20)
        
        display_surface.blit(time_text, time_rect)


    def draw_health_bar(self):
        left_shift = 30
        right_shift = 15

        # want to have this hover over the boss, so we need to access position of boss 
        if self.boss_chomper.right:
            pygame.draw.line(display_surface, (0, 0, 0), (self.boss_chomper.rect.x - right_shift, self.boss_chomper.rect.y + 60), (self.boss_chomper.rect.x + 165, self.boss_chomper.rect.y + 60), 2)
            pygame.draw.line(display_surface, (0, 0, 0), (self.boss_chomper.rect.x - right_shift, self.boss_chomper.rect.y + 80), (self.boss_chomper.rect.x + 165, self.boss_chomper.rect.y + 80), 2)
            pygame.draw.line(display_surface, (0, 0, 0), (self.boss_chomper.rect.x - right_shift, self.boss_chomper.rect.y + 60), (self.boss_chomper.rect.x - right_shift, self.boss_chomper.rect.y + 80), 2)
            pygame.draw.line(display_surface, (0, 0, 0), (self.boss_chomper.rect.x + 165, self.boss_chomper.rect.y + 60), (self.boss_chomper.rect.x + 165, self.boss_chomper.rect.y + 80), 2)
        
            # fill for the health bar: 
            if time.time() - self.word_draw_start_time < 0.35:
                pygame.draw.rect(display_surface, (255, 0, 0), pygame.Rect(self.boss_chomper.rect.x - (12), self.boss_chomper.rect.y + 63, 176 * self.boss_health, 16.5))
                self.flashing_red = False
            else:
                pygame.draw.rect(display_surface, (100, 255, 0), pygame.Rect(self.boss_chomper.rect.x - (right_shift - 3), self.boss_chomper.rect.y + 63, 176 * self.boss_health, 16.5))
        else:
            pygame.draw.line(display_surface, (0, 0, 0), (self.boss_chomper.rect.x + left_shift, self.boss_chomper.rect.y + 60), (self.boss_chomper.rect.x + 210, self.boss_chomper.rect.y + 60), 2)
            pygame.draw.line(display_surface, (0, 0, 0), (self.boss_chomper.rect.x + left_shift, self.boss_chomper.rect.y + 80), (self.boss_chomper.rect.x + 210, self.boss_chomper.rect.y + 80), 2)
            pygame.draw.line(display_surface, (0, 0, 0), (self.boss_chomper.rect.x + left_shift, self.boss_chomper.rect.y + 60), (self.boss_chomper.rect.x + left_shift, self.boss_chomper.rect.y + 80), 2)
            pygame.draw.line(display_surface, (0, 0, 0), (self.boss_chomper.rect.x + 210, self.boss_chomper.rect.y + 60), (self.boss_chomper.rect.x + 210, self.boss_chomper.rect.y + 80), 2)
        
            # outline for the health bar: 
            if time.time() - self.word_draw_start_time < 0.35:
                pygame.draw.rect(display_surface, (255, 0, 0), pygame.Rect(self.boss_chomper.rect.x + (33), self.boss_chomper.rect.y + 63, 176 * self.boss_health, 16.5))
                self.flashing_red = False
            else:
                pygame.draw.rect(display_surface, (100, 255, 0), pygame.Rect(self.boss_chomper.rect.x + (left_shift + 3), self.boss_chomper.rect.y + 63, 176 * self.boss_health, 16.5))

    def boss_hurt(self, damage):
        self.boss_health -= damage
        self.flashing_red = True
        self.displaying_word = True
        self.word_draw_start_time = time.time()
        
        # Define the message to display
        if damage == 0.1:
            self.message = 'Critical Hit!'
        elif damage == 0.05:
            self.message = 'Oof!'
        else:
            self.message = ''

    def draw_word(self):
        if time.time() - self.word_draw_start_time < 1:
            # Render the text to the screen
            text = self.custom_font.render(self.message, True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (self.boss_chomper.rect.x + 100, self.boss_chomper.rect.y + 25)
            display_surface.blit(text, text_rect)
        else:
            self.displaying_word = False


    def draw_hearts(self):
        for i in range(1, 4):
            if math.ceil(self.player_lives) < i:
                # if player has two lives and we are on the third heart location, then load empty heart
                self.heart = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/empty-heart.png").convert_alpha(), (48, 48))            
            elif self.player_lives % 1 != 0 and i == math.ceil(self.player_lives):
                self.heart = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/half-heart.png").convert_alpha(), (48, 48))
            else:
                self.heart = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/heart.png").convert_alpha(), (48, 48))

            self.heart_rect = self.heart.get_rect(  ) # sets a rectangle that surrounds the surface, use this to position
            self.heart_rect.topleft = (10 + (i * 52), 0) # can position multiple ways
            display_surface.blit(self.heart, self.heart_rect)
        

    def check_collisions(self, player, boss, creeper_one, creeper_two, creeper_three):
        # Check for collisions between player and boss
        collision_list = pygame.sprite.spritecollide(player, [boss, creeper_one, creeper_two, creeper_three], False, pygame.sprite.collide_mask)
        # collision_list is either empty or contains just the boss sprite
        for collided in collision_list:
            # essentially looping through an array or 0 or 1 and checking the collision_occurred variable in the boss class
            if not collided.collision_occurred and player.is_attacking and not boss.attacking_basic and not boss.attacking_special:
                # now want to check if the player hit the butt or head rect to determine how much damage the boss takes
                if player.rect.colliderect(boss.butt_rect):
                    self.boss_hurt(1)
                elif player.rect.colliderect(boss.head_rect):
                    self.boss_hurt(1)
                else:
                    self.boss_hurt(1)
            
                boss.is_hurting = True
                collided.collision_occurred = True
            elif not collided.collision_occurred and not player.is_attacking and (boss.attacking_basic or boss.attacking_special):
                if boss.attacking_special:
                    self.player_lives_update(1)
                else:
                    self.player_lives_update(0.5)
                player.is_hurting = True
                player.started_hurting = True
                collided.collision_occurred = True
            elif player.is_attacking and (boss.attacking_basic or boss.attacking_special) and not collided.collision_occurred:
                if boss.attacking_special:
                    self.player_lives_update(1)
                else:
                    self.player_lives_update(0.5)

                if player.rect.colliderect(boss.butt_rect):
                    self.boss_hurt(0.05)
                elif player.rect.colliderect(boss.head_rect):
                    self.boss_hurt(0.1)
                else:
                    self.boss_hurt(0.05)
                boss.is_hurting = True
                player.is_hurting = True
            elif not collided.collision_occurred and (creeper_one.attacking or creeper_two.attacking or creeper_three.attacking):
                # this if is so that the player only gets hurt if they are being attacked by the creeper they are closest to
                # print("creeper two rect: ", creeper_two.rect.x)
                # print("player rect: ", player.rect.x)
                if (creeper_one.attacking and player.rect.x < (creeper_one.rect.x + 100) and player.rect.x > (creeper_one.rect.x - 100)) or (creeper_two.attacking and player.rect.x < (creeper_two.rect.x + 100) and player.rect.x > (creeper_two.rect.x - 100)) or (creeper_three.attacking and player.rect.x < (creeper_three.rect.x + 100) and player.rect.x > (creeper_three.rect.x - 100)):
                    # print("player is being attacked by creeper")
                    self.player_lives_update(0.25)
                    player.is_hurting = True
                    player.started_hurting = True
                    collided.collision_occurred = True
        if len(collision_list) == 0:
            boss.collision_occurred = False
            creeper_one.collision_occurred = False
            creeper_two.collision_occurred = False
            creeper_three.collision_occurred = False

    def check_game_over(self):
        if self.player_lives <= 0:
            # player lost 
            self.player.is_dying = True
            self.player.able_to_move = False
            self.player_death_animation()
            self.show_player_loss_screen()
        elif self.boss_health <= 0.09:
            self.boss_chomper.is_dying = True
            self.boss_chomper.able_to_move = False
            self.boss_death_animation()
            settings.save_level = 1
            self.show_player_win_screen()


    def player_death_animation(self):
        # here i just want the player to go through a whole cycle of animations, and 
        # then i want the game to show the death screen 
        if self.player.right:
            death_frames = self.player.death_right_frames # a list of death frames
        else:
            death_frames = self.player.death_left_frames # a list of death frames
        delay = 200 # the delay between each frame in milliseconds

        for frame in death_frames:
            # currently have it so that everything goes away except the player 
            self.player.image = frame
            # redraw the screen
            self.player_group.draw(display_surface)
            pygame.display.flip()
            pygame.time.delay(delay)
            display_surface.fill('black')
            sprite_group.draw(display_surface)

    
    def boss_death_animation(self):
        # here i just want the player to go through a whole cycle of animations, and 
        # then i want the game to show the death screen 
        if self.boss_chomper.right:
            death_frames = self.boss_chomper.death_right_frames # a list of death frames
        else:
            death_frames = self.boss_chomper.death_left_frames # a list of death frames

        delay = 400 # the delay between each frame in milliseconds

        for frame in death_frames:
            # currently have it so that everything goes away except the player 
            self.boss_chomper.image = frame
            # redraw the screen
            self.boss_group.draw(display_surface)
            self.player_group.draw(display_surface)

            pygame.display.flip()
            pygame.time.delay(delay)
            display_surface.fill('black')
            sprite_group.draw(display_surface)

        # pause the animation for a few seconds
        pygame.time.wait(2000)


    def show_player_loss_screen(self):
        game_over = True

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        main_text = self.custom_font.render("GAME OVER", True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        retry_text = self.custom_font.render("Press Y to retry", True, WHITE)
        exit_text = self.custom_font.render("Press N to exit", True, WHITE)

        retry_rect = retry_text.get_rect()
        retry_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50)

        exit_rect = exit_text.get_rect()
        exit_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100)

        #Display the pause text
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(retry_text, retry_rect)
        display_surface.blit(exit_text, exit_rect)

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
                        settings.game_state = 0
                        settings.transition = not settings.transition
                        settings.leaving_level = True
                        game_over = False

    def show_player_win_screen(self):
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        game_over = True

        #Create main pause text
        main_text = self.title_font.render("YOU WON", True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2 + 15, WINDOW_HEIGHT//2 - 150)

        new_high_score = False
        display_time = time.time() - self.starting_time
        # previous :
        if ((self.player_lives * 1000 - int(display_time) * 10) < 0):
            score = 0
        elif (self.player_lives * 1000 - int(display_time) * 10) > settings.level_one_score:
            print("new high score!!!")
            new_high_score = True
            # score is their score during this round 
            score = self.player_lives * 1000 - (display_time) * 10
        else:
            score = self.player_lives * 1000 - (display_time) * 10
        
        display_surface.fill(BLACK)

        if new_high_score and settings.level_one_score != 0:

            old_high_score_text = self.custom_font.render("OLD HIGH SCORE " + str(int(settings.level_one_score)), True, WHITE)
            old_high_score_text_rect = old_high_score_text.get_rect()
            old_high_score_text_rect.center = (WINDOW_WIDTH//2 + 20, WINDOW_HEIGHT//2 - 75)

            new_high_score = self.custom_font.render("NEW HIGH SCORE " + str(int(score)), True, WHITE)
            new_high_score_rect = new_high_score.get_rect()
            new_high_score_rect.center = (WINDOW_WIDTH//2 + 20, WINDOW_HEIGHT//2 - 25)

            # save the new high score with the "score" variable
            settings.level_one_score = score

            display_surface.blit(old_high_score_text, old_high_score_text_rect)
            display_surface.blit(new_high_score, new_high_score_rect)
        elif new_high_score and settings.level_one_score == 0:
            print("inside second if")
            # if there is no old high score, i want it to say "your score: score"
            # and then underneath it, it will say "high score: score"
            player_score_text = self.custom_font.render("YOUR SCORE " + str(int(score)), True, WHITE)
            player_score_text_rect = player_score_text.get_rect()
            player_score_text_rect.center = (WINDOW_WIDTH//2 + 20, WINDOW_HEIGHT//2 - 75)

            high_score_text = self.custom_font.render("HIGH SCORE " + str(int(score)), True, WHITE)
            high_score_text_rect = high_score_text.get_rect()
            high_score_text_rect.center = (WINDOW_WIDTH//2 + 20, WINDOW_HEIGHT//2 - 25)

            settings.level_one_score = score

            display_surface.blit(player_score_text, player_score_text_rect)
            display_surface.blit(high_score_text, high_score_text_rect)
        else:
            print("inside else")
            # if there is no new high score, i want it to say "your score: score"
            # and then underneath it, it will say "high score: score"
            player_score_text = self.custom_font.render("YOUR SCORE " + str(int(score)), True, WHITE)
            player_score_text_rect = player_score_text.get_rect()
            player_score_text_rect.center = (WINDOW_WIDTH//2 + 20, WINDOW_HEIGHT//2 - 75)

            high_score_text = self.custom_font.render("HIGH SCORE " + str(int(settings.level_one_score)), True, WHITE)
            high_score_text_rect = high_score_text.get_rect()
            high_score_text_rect.center = (WINDOW_WIDTH//2 + 20, WINDOW_HEIGHT//2 - 25)

            display_surface.blit(player_score_text, player_score_text_rect)
            display_surface.blit(high_score_text, high_score_text_rect)
        

        save_load_manager.save_game_data([settings.level_one_score], ["level_one_score"])

        continue_text = self.custom_font.render("PRESS ENTER TO CONTINUE", True, WHITE)
        continue_rect = main_text.get_rect()
        continue_rect.center = (WINDOW_WIDTH//2 - 55, WINDOW_HEIGHT//2 + 100)
        
        #Display the pause text
        display_surface.blit(main_text, main_rect)
        display_surface.blit(continue_text, continue_rect)
        

        pygame.display.update()
        while game_over:
            for event in pygame.event.get():    
                #User wants to quit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # THIS SHOULD GO TO THE LEVEL SELECTOR
                        pygame.mixer.music.stop()
                        settings.game_state = 0
                        settings.transition = not settings.transition
                        settings.leaving_level = True
                        save_load_manager.save_game_data([settings.level_one_score], ["level_one_score"])
                        game_over = False
                        self.reset()

    def reset(self):
        self.player_lives = 3
        self.boss_health = 1
        self.boss_chomper.rect.bottomleft = (600, 385)
        self.player.position = (164, 164)
        self.player.able_to_move = True
        self.player.is_hurting = False
        self.player.is_attacking = False
        self.boss_chomper.is_dying = False
        self.boss_chomper.able_to_move = True
        self.boss_chomper.is_hurting = False
        self.boss_chomper.attacking = False
        self.starting_time = time.time()

    
    def player_lives_update(self, lives):
        pygame.mixer.Sound.play(self.oof)
        self.player_lives -= lives
        self.update_needed = True

    def pause_game(self, main_text, sub_text):
        """Pause the game"""
        global running

        # pygame.mixer.music.pause()

        #Set colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0, 0)
        GREEN = (25, 200, 25)
        BLUE = (240, 248, 255)

        #Create main pause text
        main_text = self.custom_font.render(main_text, True, GREEN)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        #Create sub pause text
        sub_text = self.custom_font.render(sub_text, True, BLACK)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

        #Display the pause text
        # display_surface.fill(BLACK)
        pygame.draw.rect(display_surface, BLUE, pygame.Rect(150, 110, 475, 300))
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        #Pause the game until user hits enter or quits
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #User wants to continue
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                        # pygame.mixer.music.unpause()
                #User wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    def run(self): 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.is_jumping = True
                    self.player.jump()
                if event.key == pygame.K_ESCAPE:
                    self.pause_game("Paused", "Press    enter     to     play")
                if event.key == pygame.K_1 or event.key == pygame.K_k:
                    self.player.attack(1)
                if event.key == pygame.K_2 or event.key == pygame.K_l:
                    self.player.attack(2)

        sprite_group.draw(display_surface)

        self.player_group.update()
        self.player_group.draw(display_surface)

        self.boss_group.update()
        self.boss_group.draw(display_surface)

        self.creeper_group.update()
        self.creeper_group.draw(display_surface)

        self.update()