import pygame
import settings

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites, entrance_sprites):
		super().__init__(groups)
		self.image = pygame.transform.scale(pygame.image.load('./LevelSelector/graphics/test/player.png').convert_alpha(), (settings.TILESIZE, settings.TILESIZE))
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-10, 0)

		self.direction = pygame.math.Vector2()
		self.speed = 1.5

		self.obstacle_sprites = obstacle_sprites
		self.entrance_sprites = entrance_sprites

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
		print(str(collided_entrance))
		if collided_entrance:
			print("entrance collided")
			print("Would you like to enter level " + str(collided_entrance.level_number) + "? (y/n)")
			level_request = True
			while level_request:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						print("keydown")
						if event.key == pygame.K_y: 
							print("yes selected")
							settings.game_state = collided_entrance.level_number
							print("level request first" + str(level_request))
							level_request = False
							collided_entrance = False
							print("level request second" + str(level_request))
							settings.transition = True
						elif event.key == pygame.K_n: 
							self.hitbox.y += 20
							level_request = False


	def update(self): 
		self.input()
		self.move(self.speed)