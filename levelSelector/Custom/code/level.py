import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
	def __init__(self):

		# get the display surface 
		self.screen = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

	def create_map(self):
		layout = {
			'boundary': import_csv_layout(' ')
		}
		# for row_index, row in enumerate(WORLD_MAP):
		# 	for col_index, col in enumerate(row):
		# 		x = col_index * TILESIZE
		# 		y = row_index * TILESIZE
		# 		# if col == 'x':
		# 		# 	Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
		# 		if col == 'p':
		# 			self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
		self.player = Player((400, 300), [self.visible_sprites], self.obstacle_sprites)

	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		debug(self.player.direction)

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self): 
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.half_width = self.screen.get_size()[0] // 2
		self.half_height = self.screen.get_size()[1] // 2 
		self.offset = pygame.math.Vector2(100, 200)

		self.map_image = pygame.image.load("./levelSelector/Custom/Ninja Tilemaps/levelSelector.png")
		self.map_rect = self.map_image.get_rect(topleft = (0, 0))

	def custom_draw(self, player): 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		map_offset = self.map_rect.topleft - self.offset
		self.screen.blit(self.map_image, map_offset)

		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.screen.blit(sprite.image, offset_pos)