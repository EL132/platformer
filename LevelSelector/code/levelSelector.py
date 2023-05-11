#this is on the new branch 
import pygame
import settings
from LevelSelector.code.tile import Tile
from LevelSelector.code.player import Player
from LevelSelector.code.debug import debug
from LevelSelector.code.levelEntrance import LevelEntrance
from LevelSelector.code.support import *

class LevelSelector:
	def __init__(self):

		self.screen = pygame.display.get_surface()

		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.level_entrance_sprites = pygame.sprite.Group()

		self.entrance_count = 0

		self.create_map()

	def create_map(self):
		#add each csv into layout array
		layout = {
			'trail_border': import_csv_layout('./levelSelectorTileMap/csv/map_Border.csv'),
			'level_entrance': import_csv_layout('./levelSelectorTileMap/csv/map_Level Entrance.csv'),
		}

		for style, layout in layout.items(): 
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':				#there should be a functional / visual tile 
						x = col_index * settings.TILESIZE
						y = row_index * settings.TILESIZE
						if style == 'trail_border': 	
							Tile((x, y), [self.obstacle_sprites], 'invisible')
						if style == 'level_entrance': 
							if self.level_entrance_sprites.__len__() == 0: 
								LevelEntrance((x, y), [self.obstacle_sprites, self.level_entrance_sprites], 'invisible', 1)
							elif self.level_entrance_sprites.__len__() == 1: 
								LevelEntrance((x, y), [self.obstacle_sprites, self.level_entrance_sprites], 'invisible', 3)
							elif self.level_entrance_sprites.__len__() == 2:
								LevelEntrance((x, y), [self.obstacle_sprites, self.level_entrance_sprites], 'invisible', 2)

		# for entrance in self.level_entrance_sprites: 
		# 	print(entrance.level_number)
		
		self.player = Player((578, 382), [self.visible_sprites], self.obstacle_sprites, self.level_entrance_sprites)

	def entrance_confirmation(self): 
		pass

	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		debug(self.player.rect)

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self): 
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.half_width = self.screen.get_size()[0] // 2
		self.half_height = self.screen.get_size()[1] // 2 
		self.offset = pygame.math.Vector2(100, 200)

		self.map_image = pygame.image.load("./levelSelectorTileMap/map.png")
		self.map_rect = self.map_image.get_rect(topleft = (0, 0))

		if settings.level_one_score == 0:
			self.level_one_stars = pygame.image.load("./levelSelectorTileMap/setOne/3 UI/starsZero.png")
		elif settings.level_one_score < 1500:
			self.level_one_stars = pygame.image.load("./levelSelectorTileMap/setOne/3 UI/starsOne.png")
		elif settings.level_one_score < 2500: 
			self.level_one_stars = pygame.image.load("./levelSelectorTileMap/setOne/3 UI/starsTwo.png")
		elif settings.level_one_score > 2500: 
			self.level_one_stars = pygame.image.load("./levelSelectorTileMap/setOne/3 UI/Stars.png")

		self.stars_rect_one = self.level_one_stars.get_rect(topleft = (685, 311))

	def custom_draw(self, player): 
		#calculate offset based on player movement 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		map_offset = self.map_rect.topleft - self.offset
		self.screen.blit(self.map_image, map_offset)

		stars_offset = self.stars_rect_one.topleft - self.offset
		self.screen.blit(self.level_one_stars, stars_offset)

		#loop through each sprite and blit according to offset position 
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.screen.blit(sprite.image, offset_pos)