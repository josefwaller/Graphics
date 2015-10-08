from assets.files.utilities.key_handler import KeyHandler
from assets.files.utilities.globals import Globals

import pygame
import json
import sys

class LevelEditor():

	item_chosen = [0, 0]
	menu_width = None
	items = []

	block_chosen = [0, 0]

	entities = [[]]

	write_entities = []
	def __init__(self):

		self.level_width = 20
		self.menu_width = 300
		windowSize = width, height = 100 + (self.level_width * 30), 480
		self.window = pygame.display.set_mode(windowSize)

		self.block_size = int(self.window.get_size()[1] / 16)

		Globals.block_size = int(self.window.get_size()[1] / 16)

		self.run_editor()


	def print_to_file(self, file_name):

		print_entities = []

		for x in range(len(self.entities)):
			for y in range(len(self.entities[x])):

				if not self.entities[x][y] == None:

					new_entity = {
						"x": x,
						"y": y,
						"type": self.entities[x][y]
					}

					print_entities.append(new_entity)

		f = open(file_name, 'w')
		f.write(json.dumps(print_entities))
		sys.exit()

	def run_editor (self):

		for x in range(self.level_width):
				
			while len(self.entities) <= x:
				self.entities.append([])

			for y in range(16):

				while len(self.entities[x]) <= y:
					self.entities[x].append([])

				self.entities[x][y] = None

		k = KeyHandler()

		red = 255, 0, 0

		sky = pygame.image.load("assets/images/props/sky.png").convert_alpha()

		converter = sky.get_size()[0] / sky.get_size()[1]

		sky = pygame.transform.scale(sky, (int(self.window.get_size()[0] * converter), self.window.get_size()[1]))

		while True:

			self.window.blit(sky, (0, 0))

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

				x = self.block_chosen[0]
				y = self.block_chosen[1]

				if pygame.K_RETURN in keys:

					self.entities[x][y] = 'platform'

				elif pygame.K_p in keys:

					self.entities[x][y] = 'player'

				elif pygame.K_z in keys:

					self.entities[x][y] = 'walker'


				elif pygame.K_a in keys:

					self.entities[x][y] = 'archer'
					
				elif pygame.K_w in keys:

					self.entities[x][y] = 'wizard'

				elif pygame.K_j in keys:

					self.entities[x][y] = 'jumper'

				elif pygame.K_c in keys:

					self.entities[x][y] = 'checkpoint'

				elif pygame.K_b in keys:

					self.entities[x][y] = 'bar'

				if pygame.K_n in keys:
					self.print_to_file("assets/levels/l1.json")

			for x in range(len(self.entities)):
				for y in range(len(self.entities[x])):

					if self.entities[x][y] == 'platform':
						image = pygame.image.load("assets/images/blocks/snow.png").convert_alpha()

					elif self.entities[x][y] == 'player':
						image = pygame.image.load("assets/images/player/run_1.png").convert_alpha()

					elif self.entities[x][y] == 'wizard':
						image = pygame.image.load("assets/images/enemies/wizard/front1.png").convert_alpha()

					elif self.entities[x][y] == 'archer':
						image = pygame.image.load("assets/images/enemies/archer/archer_1.png").convert_alpha()

					elif self.entities[x][y] == 'walker':
						image = pygame.image.load("assets/images/enemies/walker/run_1.png").convert_alpha()

					elif self.entities[x][y] == 'jumper':
						image = pygame.image.load("assets/images/enemies/jumper/jumper_stand_1.png").convert_alpha()

					if not self.entities[x][y] == None:

						image = pygame.transform.scale(image, (self.block_size, self.block_size))

						self.window.blit(image, (x * self.block_size, y * self.block_size))
			pygame.draw.rect(self.window, red, [self.block_chosen[0] * self.block_size, self.block_chosen[1] * self.block_size, self.block_size, self.block_size])

			pygame.display.flip()

