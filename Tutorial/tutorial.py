import pygame, time
from pytmx.util_pygame import load_pygame

from playerOne import Player as playerOne
from playerTwo import Player as playerTwo
# from Levels.LevelThree.player import Player as playerThree
from tile import Tile

pygame.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 448

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), flags=pygame.SCALED, vsync=1)

tmx_data = load_pygame('./Tutorial/maps/main.tmx')

sprite_group = pygame.sprite.Group()
land_sprite_group = pygame.sprite.Group()

# cycle through all layers
for layer in tmx_data.visible_layers:
    if hasattr(layer,'data'):
        for x, y, surf in layer.tiles():
            pos = (x * 32, y * 32)
            temp = Tile(pos = pos, surf = surf, groups = sprite_group)
            if layer.name in ('Main'):
                land_sprite_group.add(temp)




class Tutorial():
    def __init__(self, level):
        self.level = level
        self.custom_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 32)

        self.player_group = pygame.sprite.Group()

        if self.level == 1:
            self.player = playerOne(100, 100, land_sprite_group)
        elif self.level == 2:
            self.player = playerTwo(100, 100, land_sprite_group)
        else:
            self.player = 0

        self.player_group.add(self.player)
        self.started = False
        
        self.starting_time = time.time()
        self.time_passed = 0

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

    def starting_text(self):
        if self.started:
            beginning_text = True
            # video : 
            messages = ['Welcome to the tutorial!', 
                        'You will be learning how to play the game.',
                        'You will get access to different abilities as you complete more levels.',
                        'Come back later to learn how to use them as you play.']
            snip = self.custom_font.render('', True, (255, 255, 255))
            counter = 0
            # the bigger the speed variable, the slower it goes because of math
            speed = 4
            active_message = 0
            message = messages[active_message]
            done = False
            

            while beginning_text:
                if counter < speed * len(message):
                    counter += 1
                elif counter >= speed * len(message):
                    done = True
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and done and active_message < len(messages) - 1:
                            if active_message == 3:
                                beginning_text = False
                            active_message += 1
                            done = False
                            message = messages[active_message]
                            counter = 0
                            self.update()


                
                snip = self.custom_font.render(message[0:counter//speed], True, (255, 255, 255))
                screen.blit(snip, (50, 100))

                pygame.display.flip()

    def update(self):
        sprite_group.update()
        sprite_group.draw(screen)

        self.player_group.update()
        self.player_group.draw(screen)

        self.time_passed = time.time() - self.starting_time

        if self.time_passed > 3 and not self.started:
            self.started = True
            self.starting_text()



tutorial = Tutorial(1)

clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # level one animations
            if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and tutorial.player.is_attacking == False:
                tutorial.player.jump()
            if event.key == pygame.K_ESCAPE:
                tutorial.pause_game("Paused", "Press     escape     to     quit", "Press    enter     to     continue")
            if event.key == pygame.K_q:
                tutorial.player.attack(1)
            if event.key == pygame.K_w:
                tutorial.player.attack(2)

            # level two aniamtions
            if tutorial.level == 2:
                if event.key == pygame.K_r:
                    tutorial.player.roll()
        if event.type == pygame.QUIT:
            running = False

    tutorial.update()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()