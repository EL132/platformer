import pygame 
from settings import *

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

		self.direction = pygame.math.Vector2()
		self.speed = 5

	def input(self): 
		keys = pygame.key.get_pressed()

		if keys[pygame.K_w]: 
			self.direction.y = -1
		elif keys[pygame.K_s]: 
			self.direction.y = 1
		else: 
			self.direction.y = 0

		if keys[pygame.K_d]: 
			self.direction.x = 1
		elif keys[pygame.K_a]: 
			self.direction.x = -1
		else: 
			self.direction.x = 0

	def move(self, speed): 
		self.rect.center += self.direction * speed

	def update(self): 
		self.input()
		self.move(self.speed)