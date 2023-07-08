import pygame, sys
import settings 
from LevelSelector.Code.levelSelector import LevelSelector
from Levels.LevelOne.levelOne import LevelOne
from Levels.LevelTwo.levelTwo import LevelTwo
from Levels.LevelThree.levelThree import LevelThree
from Tutorial.tutorial import Tutorial
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

		self.levelSelector = LevelSelector((578, 382))
		self.levelOne = LevelOne()
		self.levelTwo = LevelTwo() 
		self.levelThree = LevelThree()
		self.levelOneTut = Tutorial(1)
		self.levelTwoTut = Tutorial(2)
		self.levelThreeTut = Tutorial(3)
		self.menu = Menu()

	def fadeOut(self): 
		if settings.game_state == -1:
			pygame.image.save(self.screen, "./LevelSelector/TransitionImages/screenshot.png")
		image = pygame.image.load("./LevelSelector/TransitionImages/screenshot.png")
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
		if settings.next_game_state == -1:
			image = pygame.image.load("LevelSelector/TransitionImages/menu.png")
		elif settings.next_game_state == 0: 
			image = pygame.image.load("LevelSelector/TransitionImages/levelSelectorStart.png")
			
		fade = pygame.Surface((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))
		fade.fill((0, 0, 0))
		for alpha in range(275, 0, -1):
			fade.set_alpha(alpha)
			self.redrawScreen(image)
			self.screen.blit(fade, (0,0))
			pygame.display.update()
			pygame.time.delay(3)
		
		settings.game_state = settings.next_game_state


	def redrawScreen(self, fade_image): 
		self.screen.fill((255, 255, 255))
		self.fade_image = fade_image
		self.fade_rect = self.fade_image.get_rect(topleft = (0, 0))
		self.screen.blit(self.fade_image, self.fade_rect)


	def curtainIn(self):
		image = pygame.image.load("./LevelSelector/TransitionImages/screenshot.png")
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
		if settings.next_game_state == 0 and (settings.game_state == 0.5 or settings.game_state == 1): 
			image = pygame.image.load("LevelSelector/TransitionImages/levelOneRespawn.png")
		elif settings.next_game_state == 0 and (settings.game_state == 1.5 or settings.game_state == 2): 
			image = pygame.image.load("LevelSelector/TransitionImages/levelTwoRespawn.png")
		elif settings.next_game_state == 0 and (settings.game_state == 2.5 or settings.game_state == 3): 
			image = pygame.image.load("LevelSelector/TransitionImages/levelThreeRespawn.png")
		elif settings.next_game_state == 0.5 or settings.next_game_state == 1.5 or settings.next_game_state == 2.5: 
			image = pygame.image.load("LevelSelector/TransitionImages/tutorialStart.png")
		elif settings.next_game_state == 1: 
			image = pygame.image.load("LevelSelector/TransitionImages/levelOneStart.png")
			self.levelOne.reset()
		elif settings.next_game_state == 2: 
			image = pygame.image.load("LevelSelector/TransitionImages/levelTwoStart.png")
			self.levelTwo.reset()
		elif settings.next_game_state == 3: 
			image = pygame.image.load("LevelSelector/TransitionImages/levelThreeStart.png")
			self.levelThree.reset()

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
			# print(settings.next_game_state)
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
						if event.key == pygame.K_k:
							# pygame.image.save(self.screen, "./Website/vert-image.png")
							pass
					
					elif settings.game_state == 2:
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

					elif settings.game_state == 3: 
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
							# pygame.image.save(self.screen, "./LevelSelector/TransitionImages/levelThreeStart.png")
							pass

					# level one animations
					elif settings.game_state == 0.5:
						if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and self.levelOneTut.player.is_attacking == False:
							self.levelOneTut.player.jump()
						if event.key == pygame.K_ESCAPE:
							self.levelOneTut.pause_game("Paused", "Press     escape     to     quit", "Press    enter     to     continue")
						if event.key == pygame.K_q:
							self.levelOneTut.player.attack(1)
						if event.key == pygame.K_w:
							self.levelOneTut.player.attack(2)

					elif settings.game_state == 1.5:
						if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and self.levelTwoTut.player.is_attacking == False:
							self.levelTwoTut.player.jump()
						if event.key == pygame.K_ESCAPE:
							self.levelTwoTut.pause_game("Paused", "Press     escape     to     quit", "Press    enter     to     continue")
						if event.key == pygame.K_q:
							self.levelTwoTut.player.attack(1)
						if event.key == pygame.K_w:
							self.levelTwoTut.player.attack(2)
						# level two animations
						if event.key == pygame.K_r:
							self.levelTwoTut.player.roll()
						if event.key == pygame.K_t:
							self.levelTwoTut.player.current_sprite = 0
							self.levelTwoTut.player.is_angry_emoting = True
						if event.key == pygame.K_y:
							self.levelTwoTut.player.is_normal_emoting = True

					elif settings.game_state == 2.5:
						if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and self.levelThreeTut.player.is_attacking == False:
							self.levelThreeTut.player.jump()
						if event.key == pygame.K_ESCAPE:
							self.levelThreeTut.pause_game("Paused", "Press     escape     to     quit", "Press    enter     to     continue")
						if event.key == pygame.K_q:
							self.levelThreeTut.player.attack(1)
						if event.key == pygame.K_w:
							self.levelThreeTut.player.attack(2)
						# level three animations
						if event.key == pygame.K_r:
							self.levelThreeTut.player.roll()
						if event.key == pygame.K_t:
							self.levelThreeTut.player.current_sprite = 0
							self.levelThreeTut.player.is_angry_emoting = True
						if event.key == pygame.K_y:
							self.levelThreeTut.player.is_normal_emoting = True

					elif settings.game_state == 0:
						if event.key == pygame.K_k: 
							pygame.image.save(self.screen, "./LevelSelector/TransitionImages/LevelSelectorStart.png")
							pass			

			self.screen.fill('black')

			#previous: Main Menu - lalalala
			#Main Menu - lalalala
			#Main Menu - lalalala
			if settings.game_state == -1:
				self.menu.run()

				if settings.transition:
					del self.levelSelector
					self.levelSelector = LevelSelector((440, 380))

					self.fadeOut()
					settings.transition = False
					pygame.mixer.music.load('./SFX/level_selector_background.mp3')
					pygame.mixer.music.play(-1)

			#Level Selector 
			elif settings.game_state == 0: 
				if not settings.transition: 
					self.levelSelector.run()
				else:
					if settings.next_game_state == -1: 
						self.fadeOut()
					else:
						self.curtainIn()

			elif settings.game_state == 0.5:
				if not settings.transition:
					self.levelOneTut.run()
				else:
					del self.levelSelector
					self.levelSelector = LevelSelector((898, 382))

					self.curtainIn()

			#Level 1
			elif settings.game_state == 1: 
				if not settings.transition: 
					self.levelOne.run()
				else: 
					del self.levelSelector
					self.levelSelector = LevelSelector((898, 382))

					self.curtainIn()
			
			elif settings.game_state == 1.5:
				if not settings.transition: 
					self.levelTwoTut.run()
				else: 
					del self.levelSelector
					self.levelSelector = LevelSelector((990, 895))

					self.curtainIn()

			#Level 2
			elif settings.game_state == 2: 
				if not settings.transition: 
					self.levelTwo.run()
				else: 
					del self.levelSelector
					self.levelSelector = LevelSelector((990, 895))

					self.curtainIn()

			elif settings.game_state == 2.5:
				if not settings.transition: 
					self.levelThreeTut.run()
				else: 
					del self.levelSelector
					self.levelSelector = LevelSelector((1630, 605))

					self.curtainIn()
					
			#Level 3
			elif settings.game_state == 3:
				if not settings.transition:
					self.levelThree.run()
				else:
					del self.levelSelector
					self.levelSelector = LevelSelector((1630, 605))

					self.curtainIn()

			pygame.display.update()

			self.clock.tick(settings.FPS)

if __name__ == '__main__':
	game = Game()
	game.run() 