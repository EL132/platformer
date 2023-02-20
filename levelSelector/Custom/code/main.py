import pygame, sys
from settings import *
from debug import debug
from level import Level

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 448


class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), flags=pygame.SCALED, vsync=1)
		pygame.display.set_caption('Level Selector')
		self.clock = pygame.time.Clock()

		self.level = Level()
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run() 