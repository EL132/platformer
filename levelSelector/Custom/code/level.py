import pygame
from settings import *
from tile import Tile
from Levels.LevelOne.player import Player
from debug import debug
from support import *

class Level:
	def __init__(self):

		self.screen = pygame.display.get_surface()

		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.level_entrance_sprites = pygame.sprite.Group()

		self.create_map()

	def create_map(self):
		#add each csv into layout array
		layout = {
			'trail_border': import_csv_layout('./levelSelector/Custom/Tilemaps/csv/LevelSelector._Trail Border.csv'),
			'level_entrance': import_csv_layout('./levelSelector/Custom/Tilemaps/csv/LevelSelector._Level Entrance.csv')
		}

		for style, layout in layout.items(): 
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':				#there should be a functional / visual tile 
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'trail_border': 	
							Tile((x, y), [self.obstacle_sprites], 'invisible')
						if style == 'level_entrance': 
							Tile((x, y), [self.obstacle_sprites, self.level_entrance_sprites], 'invisible')

		self.player = Player((15, 45), [self.visible_sprites], self.obstacle_sprites, self.level_entrance_sprites)

	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		debug(self.player.rect.topleft)

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self): 
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.half_width = self.screen.get_size()[0] // 2
		self.half_height = self.screen.get_size()[1] // 2 
		self.offset = pygame.math.Vector2(100, 200)

		self.map_image = pygame.image.load("./levelSelector/Custom/Tilemaps/levelSelector.png")
		self.map_rect = self.map_image.get_rect(topleft = (0, 0))

	def custom_draw(self, player): 
		#calculate offset based on player movement 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		map_offset = self.map_rect.topleft - self.offset
		self.screen.blit(self.map_image, map_offset)

		#loop through each sprite and blit according to offset position 
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.screen.blit(sprite.image, offset_pos)