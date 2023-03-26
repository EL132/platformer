import pygame
from settings import *

class LevelEntrance(pygame.sprite.Sprite):
	def __init__(self, pos, groups, sprite_type, level_number):
		super().__init__(groups)
		self.sprite_type = sprite_type
		self.level_number = level_number
		self.rect = pygame.Rect(pos[0], pos[1], TILESIZE, TILESIZE)
		self.hitbox = self.rect.inflate(0, -10)