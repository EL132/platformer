import pygame, sys
import settings 
from levelSelector.Custom.code.debug import debug
from levelSelector.Custom.code.levelSelector import Level
from Levels.LevelOne.levelOne import LevelOne

sys.dont_write_bytecode = True

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT), flags=pygame.SCALED, vsync=1)
		pygame.display.set_caption('Level Selector')
		self.clock = pygame.time.Clock()

		self.level = Level()
		self.levelOne = LevelOne()

	def fade(self, width, height): 
		fade = pygame.Surface((width, height))
		fade.fill((0,0,0))
		for alpha in range(0, 150):
			print("looping through" + str(alpha))
			fade.set_alpha(alpha)
			self.redrawScreen()
			self.screen.blit(fade, (0,0))
			pygame.display.update()
			pygame.time.delay(3)


	def redrawScreen(self): 
		self.screen.fill((255, 255, 255))
		self.fade_image = pygame.image.load("levelSelector/Custom/screenshot.jpg")
		self.fade_rect = self.fade_image.get_rect(topleft = (0, 0))
		self.screen.blit(self.fade_image, self.fade_rect)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
						self.levelOne.player.is_jumping = True
						self.levelOne.player.jump()
					if event.key == pygame.K_ESCAPE:
						self.levelOne.pause_game("Paused", "Press    enter     to     play")
					if event.key == pygame.K_1:
						self.levelOne.player.attack(1)
					if event.key == pygame.K_2:
						self.levelOne.player.attack(2)

			self.screen.fill('black')


			if settings.game_state == 0: 
				if not settings.transition: 
					self.level.run()
				if settings.transition: 
					pygame.image.save(self.screen,"levelSelector/Custom/screenshot.jpg")
					self.fade(settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT)
					settings.transtion = False

			elif settings.game_state == 1: 
				self.levelOne.run()

			pygame.display.update()

			self.clock.tick(settings.FPS)

if __name__ == '__main__':
	game = Game()
	game.run() 