from assets.files.utilities.key_handler import KeyHandler
from assets.files.utilities.globals import Globals

from assets.files.entities.platform import Platform

import pygame

class LevelEditor():

	item_chosen = [0, 0]
	menu_width = None
	items = []

	block_chosen = [0, 0]

	entities = []

	def __init__(self):

		self.level_width = 20
		self.menu_width = 300
		windowSize = width, height = 100 + (self.level_width * 30), 480
		self.window = pygame.display.set_mode(windowSize)

		self.block_size = int(self.window.get_size()[1] / 16)

		Globals.block_size = int(self.window.get_size()[1] / 16)

		self.run_editor()

	def run_editor (self):

		k = KeyHandler()

		red = 255, 0, 0

		while True:

			pygame.draw.rect(self.window, (255, 255, 255), [0, 0, self.window.get_size()[0], self.window.get_size()[1]], self.window.get_size()[0])

			for event in pygame.event.get():

				keys = k.new_event(event)

				if pygame.K_LEFT in keys:

					self.block_chosen[0] -= 1

				elif pygame.K_RIGHT in keys:

					self.block_chosen[0] += 1

				if pygame.K_UP in keys:

					self.block_chosen[1] -= 1

				elif pygame.K_DOWN in keys:

					self.block_chosen[1] += 1

				#Spawns different entities

				if pygame.K_RETURN in keys:

					x = self.block_chosen[0]
					y = self.block_chosen[1]

					self.entities.append(Platform(x=x, y=y, w=1, h=1, top_block="blocks/temp_block.png", inner_block=None))

			for x in self.entities:

				print(x)

				x.render()

			pygame.draw.rect(self.window, red, [self.block_chosen[0] * self.block_size + self.menu_width, self.block_chosen[1] * self.block_size, self.block_size, self.block_size])

			pygame.display.flip()
