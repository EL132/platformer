import pygame 
import settings 
from debug import debug
from level import Level
# from Levels/LevelOne/boss import  	

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT), flags=pygame.SCALED, vsync=1)
		pygame.display.set_caption('Level Selector')
		self.clock = pygame.time.Clock()

		self.level = Level()

	def fade(self, width, height): 
		fade = pygame.Surface((width, height))
		fade.fill((0,0,0))
		for alpha in range(0, 300):
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

			if not settings.transition: 
				self.screen.fill('black')
				self.level.run()
				pygame.display.update()
			if settings.transition: 
				pygame.image.save(self.screen,"levelSelector/Custom/screenshot.jpg")
				self.fade(settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT)
				settings.transtion = False
				self.level.kill


			self.clock.tick(settings.FPS)

if __name__ == '__main__':
	game = Game()
	game.run() 