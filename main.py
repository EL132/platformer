import pygame, sys
import settings 
from LevelSelector.Code.levelSelector import LevelSelector
from Levels.LevelOne.levelOne import LevelOne
from Levels.LevelTwo.levelTwo import LevelTwo
from Levels.LevelThree.levelThree import LevelThree
from GameSave.SaveLoadManager import SaveLoadSystem
from Menu.menu import Menu

sys.dont_write_bytecode = True

save_load_manager = SaveLoadSystem(".save", "save_data")
settings.save_level = save_load_manager.load_game_data(["save_level"], [0])
# settings.FPS = save_load_manager.load_game_data(["FPS"], [60])
settings.FPS = 60
settings.difficulty = save_load_manager.load_game_data(["difficulty"], [2])

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT), flags=pygame.SCALED, vsync=1)
		# self.screen = pygame.display.set_mode((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))
		pygame.display.set_caption('Level Selector')
		self.clock = pygame.time.Clock()

		self.curtain_counter = 0
		self.curtain_closed = False

		self.levelSelector = LevelSelector()
		self.levelOne = LevelOne()
		self.levelTwo = LevelTwo() 
		self.levelThree = LevelThree()
		self.menu = Menu()

	def fadeOut(self): 
		pygame.image.save(self.screen, "./LevelSelector/screenshot.png")
		image = pygame.image.load("./LevelSelector/screenshot.png")
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
			image = pygame.image.load("LevelSelector/levelSelectorStart.png")
		elif settings.game_state == 1:
			image = pygame.image.load("LevelSelector/levelOneStart.png")
			
		fade = pygame.Surface((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))
		fade.fill((0, 0, 0))
		for alpha in range(275, 0, -1):
			fade.set_alpha(alpha)
			self.redrawScreen(image)
			self.screen.blit(fade, (0,0))
			pygame.display.update()
			pygame.time.delay(3)

	def redrawScreen(self, fade_image): 
		self.screen.fill((255, 255, 255))
		self.fade_image = fade_image
		self.fade_rect = self.fade_image.get_rect(topleft = (0, 0))
		self.screen.blit(self.fade_image, self.fade_rect)

	def curtainIn(self):
		image = pygame.image.load("./LevelSelector/screenshot.png")
		image_rect = image.get_rect(topleft = (0, 0))
		self.screen.blit(image, image_rect)
		if self.curtain_counter < settings.DISPLAY_WIDTH // 2 and not self.curtain_closed: 
			self.curtain_counter += 4
			pygame.draw.rect(self.screen, settings.BLACK, (0, 0, self.curtain_counter, settings.DISPLAY_HEIGHT))
			pygame.draw.rect(self.screen, settings.BLACK, (settings.DISPLAY_WIDTH - self.curtain_counter, 0, settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))
		else:
			self.curtain_closed = True
			self.curtainOut()
			

	
	def curtainOut(self):
		if settings.next_game_state == 0:
			image = pygame.image.load("LevelSelector/levelSelectorStart.png")
		elif settings.next_game_state == 1: 
			image = pygame.image.load("LevelSelector/levelOneStart.png")
		elif settings.next_game_state == 2: 
			image = pygame.image.load("LevelSelector/levelTwoStart.png")
		elif settings.next_game_state == 3: 
			image = pygame.image.load("LevelSelector/levelThreeStart.png")

		image_rect = image.get_rect(topleft = (0, 0))
		self.screen.blit(image, image_rect)

		if self.curtain_counter > 0: 
			self.curtain_counter -= 4
			pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.curtain_counter, settings.DISPLAY_HEIGHT))
			pygame.draw.rect(self.screen, (0, 0, 0), (settings.DISPLAY_WIDTH - self.curtain_counter, 0, settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))
		else: 
			settings.game_state = settings.next_game_state
			settings.transition = False
			self.curtain_closed = False	

	def run(self):
		while True:	
			print(settings.game_state)
			if settings.mute:
				pygame.mixer.music.set_volume(0)
			else:
				pygame.mixer.music.set_volume(0.5)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					save_load_manager.save_game_data([settings.save_level], ["save_level"])
					pygame.quit()
				if event.type == pygame.KEYDOWN:
					if settings.game_state == 1:
						if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and self.levelOne.player.is_attacking == False:
							self.levelOne.player.jump()
						if event.key == pygame.K_ESCAPE:
							self.levelOne.pause_game("Paused", "Press     escape     to     quit", "Press    enter     to     continue")
						if event.key == pygame.K_q:
							self.levelOne.player.attack(1)
						if event.key == pygame.K_w:
							self.levelOne.player.attack(2)

					elif settings.game_state == 2: 
						if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and self.levelOne.player.is_attacking == False:
							self.levelOne.player.jump()
						if event.key == pygame.K_ESCAPE:
							self.levelOne.pause_game("Paused", "Press     escape     to     quit", "Press    enter     to     continue")
						if event.key == pygame.K_q:
							self.levelOne.player.attack(1)
						if event.key == pygame.K_w:
							self.levelOne.player.attack(2)
						if event.key == pygame.K_k:
							# pygame.image.save(self.screen, "./LevelSelector/levelTwoStart.png")
							pass
					
					if settings.game_state == 2:
						if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and self.levelTwo.player.is_attacking == False:
							self.levelTwo.player.jump()
						if event.key == pygame.K_ESCAPE:
							self.levelTwo.pause_game("Paused", "Press     escape     to     quit", "Press    enter     to     continue")
						if event.key == pygame.K_q:
							self.levelTwo.player.attack(1)
						if event.key == pygame.K_w:
							self.levelTwo.player.attack(2)
						if event.key == pygame.K_r:
							self.levelTwo.player.roll()
						if event.key == pygame.K_t:
							self.levelTwo.player.is_angry_emoting = True
						if event.key == pygame.K_y:
							self.levelTwo.player.is_normal_emoting = True

					if settings.game_state == 3: 
						if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and self.levelThree.player.is_attacking == False:
							self.levelThree.player.jump()
						if event.key == pygame.K_ESCAPE:
							self.levelThree.pause_game("Paused", "Press     escape     to     quit", "Press    enter     to     continue")
						if event.key == pygame.K_q:
							self.levelThree.player.attack(1)
						if event.key == pygame.K_w:
							self.levelThree.player.attack(2)
						if event.key == pygame.K_r:
							self.levelThree.player.roll()
						if event.key == pygame.K_t:
							self.levelThree.player.is_angry_emoting = True
						if event.key == pygame.K_y:
							self.levelThree.player.is_normal_emoting = True
						if event.key == pygame.K_k:
							# pygame.image.save(self.screen, "./LevelSelector/levelThreeStart.png")
							pass

					if settings.game_state == 0:
						if event.key == pygame.K_k:
							# pygame.image.save(self.screen, "./LevelSelector/levelSelectorStart.png")
							pass

			self.screen.fill('black')

			#Main Menu
			if settings.game_state == -1:
				self.menu.run()

				if settings.transition:
					self.fadeOut()
					settings.transition = False
					pygame.mixer.music.load('./SFX/level_selector_background.mp3')
					pygame.mixer.music.play(-1)

			#Level Selector 
			elif settings.game_state == 0: 
				if not settings.transition: 
					self.levelSelector.run()
				else:
					self.levelOne.loaded_up = True
					self.levelOne.reset()
					self.curtainIn()

			#Level 1
			elif settings.game_state == 1: 
				if not settings.transition: 
					self.levelOne.run()
				else: 
					del self.levelSelector
					self.levelSelector = LevelSelector()

					self.curtainIn()

			elif settings.game_state == 2: 
				if not settings.transition: 
					self.levelTwo.run()
				else: 
					del self.levelSelector
					self.levelSelector = LevelSelector()

					self.curtainIn()

			elif settings.game_state == 3:
				if not settings.transition:
					self.levelThree.run()
				else:
					del self.levelSelector
					self.levelSelector = LevelSelector()

					self.curtainIn()

			pygame.display.update()

			self.clock.tick(settings.FPS)

if __name__ == '__main__':
	game = Game()
	game.run() 