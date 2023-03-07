from colorsys import rgb_to_hls
import pygame, time, random, math
from pytmx.util_pygame import load_pygame


from tile import Tile
from player import Player
from boss import Boss
from constants import *


display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

sprite_group = pygame.sprite.Group()

clock = pygame.time.Clock()

#Initiailize pygame
pygame.init()

# video tmx code
tmx_data = load_pygame('./Levels/levelOne/maps/levelOne.tmx')


land_sprite_group = pygame.sprite.Group()

# cycle through all layers
for layer in tmx_data.visible_layers:
    if hasattr(layer,'data'):
        for x, y, surf in layer.tiles():
            # for tile in layer.tiles():
                # NOTE: here i need to check if the tile is an edge tile , use the ID of the edge tile to check this, just am not sure 
                # how to do that because the documentation is so shit and basic 
            pos = (x * 31, y * 32)
            temp = Tile(pos = pos, surf = surf, groups = sprite_group)
            if layer.name in ('Collisions'):
                land_sprite_group.add(temp)





my_player_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

my_player = Player(164, 164, land_sprite_group)
my_player_group.add(my_player)

boss_chomper = Boss(600, 385)
boss_group.add(boss_chomper)





class Game():
    def __init__(self):
        self.player_lives = 3

        self.custom_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 32)

        self.player_lives_text = self.custom_font.render("Lives", True, BEIGE)
        self.player_lives_text_rect = self.player_lives_text.get_rect()
        self.player_lives_text_rect.center = (65, 35)
        display_surface.blit(self.player_lives_text, self.player_lives_text_rect)

        self.heart = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/heart.png").convert_alpha(), (48, 48))


    def update(self):
        self.check_collisions(my_player, boss_chomper)
        self.check_game_over()
        self.draw_hearts()


    def draw_hearts(self):
        # can't do a "if change needed" because the hearts need to be drawn every frame since the back
        
        for i in range(math.ceil(self.player_lives)):
            if self.player_lives % 1 is not 0 and i is math.floor(self.player_lives):
                self.heart = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/half-heart.png").convert_alpha(), (48, 48))
            else:
                self.heart = pygame.transform.scale(pygame.image.load("./Levels/LevelOne/images/heart.png").convert_alpha(), (48, 48))
            self.heart_rect = self.heart.get_rect() # sets a rectangle that surrounds the surface, use this to position
            self.heart_rect.topleft = (130 + (i * 52), 10) # can position multiple ways
            display_surface.blit(self.heart, self.heart_rect)
        
        display_surface.blit(self.player_lives_text, self.player_lives_text_rect)

    def check_collisions(self, player, boss):
        # Check for collisions between player and boss
        collision_list = pygame.sprite.spritecollide(player, [boss], False, pygame.sprite.collide_mask)
        for collided in collision_list:
            if not collided.collision_occurred and player.is_attacking and not boss.attacking:
                boss.is_hurting = True
                collided.collision_occurred = True
            elif not collided.collision_occurred and not player.is_attacking and boss.attacking:
                player.is_hurting = True
                self.player_lives_update(0.5)
                collided.collision_occurred = True
            elif player.is_attacking and boss.attacking and not collided.collision_occurred:
                self.player_lives_update(0.5)
                boss.is_hurting = True
                player.is_hurting = True
        if len(collision_list) == 0:
            boss.collision_occurred = False

    def check_game_over(self):
        if self.player_lives <= 0:
            game_over = True
            #Set colors
            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)
            GREEN = (25, 200, 25)            

            #Create main pause text
            main_text = self.custom_font.render("GAME OVER", True, WHITE)
            main_rect = main_text.get_rect()
            main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

            #Display the pause text
            display_surface.fill(BLACK)
            # pygame.draw.rect(display_surface, BLACK, pygame.Rect(30, 30, 60, 60))
            display_surface.blit(main_text, main_rect)
            pygame.display.update()
            while game_over:
                for event in pygame.event.get():    
                    #User wants to quit
                    if event.type == pygame.QUIT:
                        game_over = False
                        self.player_lives = 3
                        pygame.mixer.music.stop()
    
    def player_lives_update(self, lives):
        self.player_lives -= lives
        self.update_needed = True

    def pause_game(self, main_text, sub_text):
        """Pause the game"""
        global running

        pygame.mixer.music.pause()

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
                        pygame.mixer.music.unpause()
                #User wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                    pygame.mixer.music.stop()


my_game = Game()



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                my_player.is_jumping = True
                my_player.jump()
            if event.key == pygame.K_ESCAPE:
                my_game.pause_game("Paused", "Press    enter     to     play")
            if event.key == pygame.K_1:
                my_player.attack(1)
            if event.key == pygame.K_2:
                my_player.attack(2)


    # high level loop progression: screen goes black, tiles get loaded, player and boss update position and get redrawn, 
    # game updates, screen updates, repeat 

    display_surface.fill('black')
    sprite_group.draw(display_surface)


    my_player_group.update()
    my_player_group.draw(display_surface)
    # pygame.draw.rect(display_surface, (255, 255, 255), my_player.rect)

    boss_group.update()
    boss_group.draw(display_surface)
    # pygame.draw.rect(display_surface, (255, 255, 255), boss_chomper.rect)

    my_game.update()
    # display_surface.blit(heart, heart_rect)

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()