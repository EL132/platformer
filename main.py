import pygame, sys
import settings 
from LevelSelector.code.debug import debug
from LevelSelector.code.levelSelector import Level
from Levels.LevelOne.levelOne import LevelOne
from GameSave.SaveLoadManager import SaveLoadSystem
from menu import Menu

sys.dont_write_bytecode = True

save_load_manager = SaveLoadSystem(".save", "save_data")
settings.save_level = save_load_manager.load_game_data(["save_level"], [0])
settings.FPS = save_load_manager.load_game_data(["FPS"], [60])
settings.difficulty = save_load_manager.load_game_data(["difficulty"], [2])

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT), flags=pygame.SCALED, vsync=1)
		pygame.display.set_caption('Level Selector')
		self.clock = pygame.time.Clock()
		self.fade_counter = 0

		self.level = Level()
		self.levelOne = LevelOne()
		self.menu = Menu()

	def fadeOut(self): 
		pygame.image.save(self.screen,"LevelSelector/screenshot.jpg")
		image = pygame.image.load("LevelSelector/screenshot.jpg")
		fade = pygame.Surface((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))
		fade.fill((0,0,0))
		for alpha in range(0, 275):
			fade.set_alpha(alpha)
			self.redrawScreen(image)
			self.screen.blit(fade, (0,0))
			pygame.display.update()
			pygame.time.delay(1)
		self.fadeIn()

	def fadeIn(self):
		if settings.game_state == 0: 
			image = pygame.image.load("LevelSelector/levelSelectorStart.jpg")
		elif settings.game_state == 1:
			image = pygame.image.load("LevelSelector/levelOneStart.jpg")
			
		fade = pygame.Surface((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))
		fade.fill((0, 0, 0))
		for alpha in range(275, 0, -1):
			fade.set_alpha(alpha)
			self.redrawScreen(image)
			self.screen.blit(fade, (0,0))
			pygame.display.update()
			pygame.time.delay(1)

	def redrawScreen(self, fade_image): 
		self.screen.fill((255, 255, 255))
		self.fade_image = fade_image
		self.fade_rect = self.fade_image.get_rect(topleft = (0, 0))
		self.screen.blit(self.fade_image, self.fade_rect)

	def curtain(self):
		image = pygame.image.load("LevelSelector/screenshot.jpg")
		image_rect = image.get_rect()
		image_rect = (0, 0)
		self.screen.blit(image, image_rect)
		if self.fade_counter < settings.DISPLAY_WIDTH // 2: 
			self.fade_counter += 4
			pygame.draw.rect(self.screen, settings.BLACK, (0, 0, self.fade_counter, settings.DISPLAY_HEIGHT))
			pygame.draw.rect(self.screen, settings.BLACK, (settings.DISPLAY_WIDTH - self.fade_counter, 0, settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))
		else:
			settings.game_state = settings.next_game_state


	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					save_load_manager.save_game_data([settings.save_level], ["save_level"])
					pygame.quit()
				if event.type == pygame.KEYDOWN:
					if settings.game_state == 1:
						if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
							self.levelOne.player.is_jumping = True
							self.levelOne.player.jump()
						if event.key == pygame.K_ESCAPE:
							self.levelOne.pause_game("Paused", "Press    enter     to     play")
						if event.key == pygame.K_1:
							self.levelOne.player.attack(1)
						if event.key == pygame.K_2:
							self.levelOne.player.attack(2)
						if event.key == pygame.K_k:
							pygame.image.save(self.screen,"LevelSelector/levelOneStart.jpg")

					if settings.game_state == 0:
						pass

			self.screen.fill('black')

			#Main Menu
			if settings.game_state == -1:
				self.menu.run()

				if self.menu.started_game:
					self.fadeOut()
					settings.transtion = False
					self.menu.started_game = False
					pygame.mixer.music.load('./SFX/level_selector_background.mp3')
					pygame.mixer.music.play(-1)

			#Level Selector 
			if settings.game_state == 0: 
				if not settings.transition: 
					self.level.run()
				if settings.transition: 
					# self.levelOne.loaded_up = True
					self.curtain()
					
					# image = pygame.image.load("LevelSelector/levelOneStart.jpg")
					# self.image_rect = self.fade_image.get_rect(topleft = (0, 0))
					# self.screen.blit(self.image_rect, self.image_rect)
					
					# self.fadeOut()
					settings.transtion = False				


			#Level 1
			elif settings.game_state == 1: 
				self.levelOne.run()

			pygame.display.update()

			self.clock.tick(settings.FPS)

if __name__ == '__main__':
	game = Game()
	game.run() 