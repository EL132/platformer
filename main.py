import pygame, sys
import settings 
from LevelSelector.code.debug import debug
from LevelSelector.code.levelSelector import Level
from Levels.LevelOne.levelOne import LevelOne
from menu import Menu

sys.dont_write_bytecode = True

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT), flags=pygame.SCALED, vsync=1)
		pygame.display.set_caption('Level Selector')
		self.clock = pygame.time.Clock()

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
			pygame.time.delay(3)
		self.fadeIn()

	def fadeIn(self):
		image = pygame.image.load("LevelSelector/levelSelectorStart.jpg")
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

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
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

			#Level Selector 
			if settings.game_state == 0: 
				if not settings.transition: 
					self.level.run()
				if settings.transition: 
					self.fadeOut()
					settings.transtion = False

			#Level 1
			elif settings.game_state == 1: 
				self.levelOne.run()

			pygame.display.update()

			self.clock.tick(settings.FPS)

if __name__ == '__main__':
	game = Game()
	game.run() 