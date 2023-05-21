#this is on the new branch 
import pygame
import settings
from LevelSelector.Code.tile import Tile
from LevelSelector.Code.player import Player
from debug import debug
from LevelSelector.Code.levelEntrance import LevelEntrance
from LevelSelector.Code.support import *

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
			'trail_border': import_csv_layout('./LevelSelector/TilemapAssets/csv/map_Border.csv'),
			'level_entrance': import_csv_layout('./LevelSelector/TilemapAssets/csv/map_Level Entrance.csv'),
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
								LevelEntrance((x, y), [self.obstacle_sprites, self.level_entrance_sprites], 'invisible', 0.5)
							elif self.level_entrance_sprites.__len__() == 2:
								LevelEntrance((x, y), [self.obstacle_sprites, self.level_entrance_sprites], 'invisible', 3)
							elif self.level_entrance_sprites.__len__() == 3:
								LevelEntrance((x, y), [self.obstacle_sprites, self.level_entrance_sprites], 'invisible', -1)
							elif self.level_entrance_sprites.__len__() == 4:
								LevelEntrance((x, y), [self.obstacle_sprites, self.level_entrance_sprites], 'invisible', 2.5)
							elif self.level_entrance_sprites.__len__() == 5:
								LevelEntrance((x, y), [self.obstacle_sprites, self.level_entrance_sprites], 'invisible', 1.5)
							else:
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

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self): 
		super().__init__()
		self.screen = pygame.display.get_surface()
		self.half_width = self.screen.get_size()[0] // 2
		self.half_height = self.screen.get_size()[1] // 2 
		self.offset = pygame.math.Vector2(100, 200)

		self.map_image = pygame.image.load("./LevelSelector/TilemapAssets/map.png")
		self.map_rect = self.map_image.get_rect(topleft = (0, 0))

		#calculate stars for levelOne
		if settings.level_one_score == 0:
			self.level_one_stars = pygame.image.load("./LevelSelector/TilemapAssets/setOne/3 UI/starsZero.png")
		elif settings.level_one_score < 1500:
			self.level_one_stars = pygame.image.load("./LevelSelector/TilemapAssets/setOne/3 UI/starsOne.png")
		elif settings.level_one_score < 2500: 
			self.level_one_stars = pygame.image.load("./LevelSelector/TilemapAssets/setOne/3 UI/starsTwo.png")
		else:
			self.level_one_stars = pygame.image.load("./LevelSelector/TilemapAssets/setOne/3 UI/Stars.png")

		#calculate stars for levelTwo
		if settings.level_two_score == 0:
			self.level_two_stars = pygame.image.load("./LevelSelector/TilemapAssets/setOne/3 UI/starsZero.png")
		elif settings.level_two_score < 1500:
			self.level_two_stars = pygame.image.load("./LevelSelector/TilemapAssets/setOne/3 UI/starsOne.png")
		elif settings.level_two_score < 2500: 
			self.level_two_stars = pygame.image.load("./LevelSelector/TilemapAssets/setOne/3 UI/starsTwo.png")
		else:
			self.level_two_stars = pygame.image.load("./LevelSelector/TilemapAssets/setOne/3 UI/Stars.png")

		#calculate stars for levelThree
		if settings.level_three_score == 0:
			self.level_three_stars = pygame.image.load("./LevelSelector/TilemapAssets/setOne/3 UI/starsZero.png")
		elif settings.level_three_score < 1500:
			self.level_three_stars = pygame.image.load("./LevelSelector/TilemapAssets/setOne/3 UI/starsOne.png")
		elif settings.level_three_score < 2500: 
			self.level_three_stars = pygame.image.load("./LevelSelector/TilemapAssets/setOne/3 UI/starsTwo.png")
		else:
			self.level_three_stars = pygame.image.load("./LevelSelector/TilemapAssets/setOne/3 UI/Stars.png")

		self.level_one_stars_rect = self.level_one_stars.get_rect(topleft = (685, 311))
		self.level_two_stars_rect = self.level_two_stars.get_rect(topleft = (654, 1317))
		self.level_three_stars_rect = self.level_three_stars.get_rect(topleft = (1293, 375))


	def custom_draw(self, player): 
		#calculate offset based on player movement 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		map_offset = self.map_rect.topleft - self.offset
		self.screen.blit(self.map_image, map_offset)

		stars_one_offset = self.level_one_stars_rect.topleft - self.offset
		self.screen.blit(self.level_one_stars, stars_one_offset)

		stars_two_offset = self.level_two_stars_rect.topleft - self.offset
		self.screen.blit(self.level_two_stars, stars_two_offset)

		stars_three_offset = self.level_three_stars_rect.topleft - self.offset
		self.screen.blit(self.level_three_stars, stars_three_offset)

		#loop through each sprite and blit according to offset position 
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.screen.blit(sprite.image, offset_pos)