import pygame, time
from pytmx.util_pygame import load_pygame

from Tutorial.playerOne import Player as playerOne
from Tutorial.playerTwo import Player as playerTwo
# from Levels.LevelThree.player import Player as playerThree
from Tutorial.tile import Tile
import settings


screen = pygame.display.get_surface()

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
        self.small_font = pygame.font.Font('./Levels/LevelOne/fonts/ARCADECLASSIC.ttf', 24)

        self.player_group = pygame.sprite.Group()

        if self.level == 1:
            self.player = playerOne(100, 384, land_sprite_group)
        elif self.level == 2:
            self.player = playerTwo(100, 384, land_sprite_group)
        else:
            self.player = playerTwo(100, 384, land_sprite_group)

        self.player_group.add(self.player)
        self.started = False
        
        self.starting_time = time.time()
        self.time_passed = 0

        self.beginning_text = False

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
        main_rect.center = (settings.DISPLAY_WIDTH//2, settings.DISPLAY_HEIGHT//2 - 100)

        #Create sub pause text
        sub_text1 = self.custom_font.render(sub_text1, True, WHITE)
        sub_rect1 = sub_text1.get_rect()
        sub_rect1.center = (settings.DISPLAY_WIDTH//2, settings.DISPLAY_HEIGHT//2 - 50)
        
        #Create sub pause text
        sub_text2 = self.custom_font.render(sub_text2, True, WHITE)
        sub_rect2 = sub_text2.get_rect()
        sub_rect2.center = (settings.DISPLAY_WIDTH//2, settings.DISPLAY_HEIGHT//2)

        # blurred_background = pygame.transform.box_blur(screen, 5)
        blurred_background = self.blurSurf(screen, 5)
        pygame.image.save(blurred_background, "./Levels/LevelOne/blurred.jpg")
        blurred_rect = blurred_background.get_rect(topleft = (0, 0))
        screen.blit(blurred_background, blurred_rect)

        #Display the pause text
        # screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, pygame.Rect(150, 80, 475, 180), 3)
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
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    pygame.quit()

    def blurSurf(self, surface, amt):
        if amt < 1.0:
            raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
        scale = 1.0/float(amt)
        surf_size = surface.get_size()
        scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
        surf = pygame.transform.smoothscale(surface, scale_size)
        surf = pygame.transform.smoothscale(surf, surf_size)
        return surf

    def starting_text(self):
        if self.started:
            self.beginning_text = True
            # video : 
            messages = ['Welcome    to    the    tutorial!', 
                'You    get    different    abilities    as    you    play',
                'Come    back    later    to    test    them    out!']
            snip = self.custom_font.render('', True, (255, 255, 255))
            counter = 0
            # the bigger the speed variable, the slower it goes because of math
            speed = 4
            active_message = 0
            message = messages[active_message]
            done = False
            

            while self.beginning_text:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and done and active_message < len(messages):
                            if active_message == 2:
                                self.beginning_text = False
                                break
                            active_message += 1
                            done = False
                            message = messages[active_message]
                            counter = 0
                            self.update()
                if counter < speed * len(message):
                    counter += 1
                elif counter >= speed * len(message):
                    done = True
                


                
                snip = self.custom_font.render(message[0:counter//speed], True, (255, 255, 255))
                screen.blit(snip, (50, 100))

                pygame.display.flip()

    def key(self):
        key_binds = ['LEFT', 'RIGHT', 'UP', 'SPACE', 'SHIFT', 'ESCAPE', 'Q', 'W', 'R', 'T', 'Y', 'SPACE']
        directions = ['move   left', 'move   right', 'jump', 'jump', 'sprint', 'pause', 'attack 1', 'attack 2', 'roll', 'taunt', 'emote', 'double jump']

        # i want to draw a rectangle for each key bind
        for i in range(0, 8):
            if not 15 + 50 * i > 200:
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(25, 15 + 50 * i, 125, 50), 3)
                snip = self.custom_font.render(key_binds[i], True, (255, 255, 255))
                screen.blit(snip, (35, 25 + 50 * i))
                direction = self.small_font.render(directions[i], True, (255, 255, 255))
                screen.blit(direction, (160, 25 + 50 * i))
            else:
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(290, 15 + 50 * (i - 4), 125, 50), 3)
                snip = self.custom_font.render(key_binds[i], True, (255, 255, 255))
                screen.blit(snip, (300, 25 + 50 * (i - 4)))
                direction = self.small_font.render(directions[i], True, (255, 255, 255))
                screen.blit(direction, (425, 25 + 50 * (i - 4)))
        
        if self.level >= 2:
            for i in range(0, 3):
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(530, 15 + 50 * i, 125, 50), 3)
                snip = self.custom_font.render(key_binds[i + 8], True, (255, 255, 255))
                screen.blit(snip, (540, 25 + 50 * i))
                direction = self.small_font.render(directions[i + 8], True, (255, 255, 255))
                screen.blit(direction, (665, 25 + 50 * i))
        
        if self.level >= 3:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(530, 15 + 150, 125, 50), 3)
            snip = self.custom_font.render(key_binds[11], True, (255, 255, 255))
            screen.blit(snip, (540, 25 + 150))
            direction = self.small_font.render(directions[11], True, (255, 255, 255))
            screen.blit(direction, (665, 25 + 150))


    def update(self):
        self.time_passed = time.time() - self.starting_time

        if self.time_passed > 1 and not self.started:
            self.started = True
            self.starting_text()

        if not self.beginning_text and self.started:
            self.key()

    def run(self): 
        sprite_group.update()
        sprite_group.draw(screen)

        self.player_group.update()
        self.player_group.draw(screen)

        self.update()