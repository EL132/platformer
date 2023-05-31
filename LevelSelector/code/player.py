import pygame
import settings

display_surface = pygame.display.set_mode((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites, entrance_sprites):
		super().__init__(groups)

		self.load_animation_sprites()

		self.screen = pygame.display.get_surface()

		self.current_sprite = 0
		self.image = self.walk_front_frames[self.current_sprite]
		self.previous_sprite_list = self.walk_front_frames

		self.current_dust = 0
		self.dust_image = self.dust_right_frames[self.current_dust]

		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-10, 0)

		self.direction = pygame.math.Vector2()
		self.speed = 3

		self.obstacle_sprites = obstacle_sprites
		self.entrance_sprites = entrance_sprites

		self.custom_font = pygame.font.Font('./Levels/LevelOne/fonts/ArcadeFont.ttf', 12)

		self.temp_x = 0
		self.temp_y = 0
		self.footstep = pygame.mixer.Sound('./SFX/footstep_two.wav')

	def input(self): 
		keys = pygame.key.get_pressed()

		if keys[pygame.K_w] or keys[pygame.K_UP]: 
			self.direction.y = -1
		elif keys[pygame.K_s] or keys[pygame.K_DOWN]: 
			self.direction.y = 1
		else: 
			self.direction.y = 0

		if keys[pygame.K_d] or keys[pygame.K_RIGHT]: 
			self.direction.x = 1
		elif keys[pygame.K_a] or keys[pygame.K_LEFT]: 
			self.direction.x = -1
		else: 
			self.direction.x = 0


	def move(self, speed): 
		if self.direction.magnitude() != 0: 
			self.direction = self.direction.normalize() * 2

		if abs(self.hitbox.x - self.temp_x) > 100:
			self.temp_x = self.hitbox.x
			self.footstep.play()
		if abs(self.hitbox.y - self.temp_y) > 100:
			self.temp_y = self.hitbox.y
			self.footstep.play()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def collision(self, direction): 
		if direction == 'horizontal': 
			for sprite in self.obstacle_sprites: 
				if sprite.hitbox.colliderect(self.hitbox): 
					if self.direction.x > 0: 
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: 
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical': 
			for sprite in self.obstacle_sprites: 
				if sprite.hitbox.colliderect(self.hitbox): 
					if self.direction.y > 0: 
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: 
						self.hitbox.top = sprite.hitbox.bottom

		collided_entrance = pygame.sprite.spritecollideany(self, self.entrance_sprites)
		if collided_entrance and not settings.transition:
			level_request = True
			# video : 
			if collided_entrance.level_number == 1 or collided_entrance.level_number == 2 or collided_entrance.level_number == 3:
				messages = ['You are about to enter level ' + str(collided_entrance.level_number) + '.', 
							'It is not that hard',
							'Are you sure you want to enter?',
							'Yes (Y) or No (N)']
			# if the user is entering a tutorial:
			elif collided_entrance.level_number % 1 == 0.5:
				messages = ['This is a tutorial house.', 
							'Are you sure you want to enter?',
							'Yes (Y) or No (N)']
			# if the user wants to return to the main menu
			elif collided_entrance.level_number == -1:
				messages = ['You are about to return to the main menu.', 
							'Are you sure you want to continue?',
							'Yes (Y) or No (N)']
			snip = self.custom_font.render('', True, (255, 255, 255))
			counter = 0
			# the bigger the speed variable, the slower it goes because of math
			speed = 4
			active_message = 0
			message = messages[active_message]
			done = False
			

			while level_request:
				pygame.draw.rect(display_surface, (0, 0, 0), pygame.Rect(225, 70, 400, 70))
				pygame.draw.rect(display_surface, (255, 255, 255), pygame.Rect(230, 75, 390, 60))

				if counter < speed * len(message):
					counter += 1
				elif counter >= speed * len(message):
					done = True
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_RETURN and done and active_message < len(messages) - 1:
							active_message += 1
							done = False
							message = messages[active_message]
							counter = 0
						elif event.key == pygame.K_y: 
							#transition and change game state
							settings.next_game_state = collided_entrance.level_number
							settings.transition = True
							pygame.image.save(self.screen,"./LevelSelector/screenshot.png")
							level_request = False			

							#change music
							pygame.mixer.music.stop()
							pygame.mixer.Sound.play(pygame.mixer.Sound('./SFX/transition_sound.wav'))
							pygame.time.delay(1000)
							if not settings.mute:
								if settings.next_game_state == -1:
									pygame.image.save(self.screen, "./LevelSelector/screenshot.png")
									pygame.mixer.music.load('./SFX/menu_music.mp3')
								if settings.next_game_state == 1:
									pygame.mixer.music.load('./SFX/level_one_bg.mp3')
								elif settings.next_game_state == 2:
									pygame.mixer.music.load('./SFX/levelTwo.mp3')
								elif settings.next_game_state == 3:
									pygame.mixer.music.load('./SFX/levelThree.mp3')
								pygame.mixer.music.play(-1)
								pygame.mixer.music.set_volume(0.1)				
						elif event.key == pygame.K_n: 
							self.hitbox.y += 20
							level_request = False
				
				snip = self.custom_font.render(message[0:counter//speed], True, (0, 0, 0))
				if active_message == 3:
					display_surface.blit(snip, (330, 100))	
				else:
					display_surface.blit(snip, (240, 100))

				pygame.display.flip()


	def update(self): 
		self.input()
		self.move(self.speed)
		self.check_animations()


	def animate(self, sprite_list, speed, idle = False):
        # loop through sprite list and change current sprite 
		if idle: 
			self.image = sprite_list[0]

		if not idle: 
			if self.current_sprite < len(sprite_list) - 0.1:
				self.current_sprite += speed
			else:
				self.current_sprite = 0

			self.image = sprite_list[int(self.current_sprite)]

		self.previous_sprite_list = sprite_list

	def animate_dust(self, pos_x, pos_y, speed): 
		if self.current_dust < len(self.dust_right_frames) - 0.1:
				self.current_dust += speed
		else:
			self.current_dust = 0

		self.dust_image = self.dust_right_frames[int(self.current_sprite)]
		self.screen.blit(self.dust_image, (settings.DISPLAY_WIDTH // 2 + pos_x, settings.DISPLAY_HEIGHT // 2 + pos_y))


	def check_animations(self):
		keys = pygame.key.get_pressed()

		if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.direction.x < 0:
			self.animate(self.walk_left_frames, 0.1)
			self.animate_dust(9, 11, 0.1)
		elif (keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.direction.x > 0):
			self.animate(self.walk_right_frames, 0.1)
			self.animate_dust(-22, 11, 0.1)
		elif (keys[pygame.K_UP] or keys[pygame.K_w]):
			self.animate(self.walk_back_frames, 0.1)
			self.animate_dust(0, 20, 0.1)
		elif (keys[pygame.K_DOWN] or keys[pygame.K_s]):
			self.animate(self.walk_front_frames, 0.1)
			self.animate_dust(0, -24, 0.1)
		else: 
			self.animate(self.previous_sprite_list, 0.1, True)



	def load_animation_sprites(self):
		self.walk_back_frames = []
		self.walk_front_frames = []
		self.walk_right_frames = []
		self.walk_left_frames = []

		self.dust_right_frames = []
		self.dust_left_frames = []

		for i in range(1, 4):
			self.walk_back_frames.append(pygame.image.load(f'./LevelSelector/SpritesAndArt/sprite animations/back/back({i}).png').convert_alpha())
			self.walk_front_frames.append(pygame.image.load(f'./LevelSelector/SpritesAndArt/sprite animations/front/front({i}).png').convert_alpha())
			self.walk_right_frames.append(pygame.image.load(f'./LevelSelector/SpritesAndArt/sprite animations/right/right({i}).png').convert_alpha())

		self.walk_back_frames.insert(2, pygame.image.load('./LevelSelector/SpritesAndArt/sprite animations/back/back(1).png').convert_alpha())
		self.walk_front_frames.insert(2, pygame.image.load('./LevelSelector/SpritesAndArt/sprite animations/front/front(1).png').convert_alpha())
		self.walk_right_frames.insert(2, pygame.image.load('./LevelSelector/SpritesAndArt/sprite animations/right/right(1).png').convert_alpha())

		for frame in self.walk_right_frames:
			self.walk_left_frames.append(pygame.transform.flip(frame, True, False))

		for i in range (1, 8):
			self.dust_right_frames.append(pygame.image.load(f"./LevelSelector/SpritesAndArt/running dust/Split/dust({i}).png"))

		for frame in self.dust_right_frames:
			self.dust_left_frames.append(pygame.transform.flip(frame, True, False))

