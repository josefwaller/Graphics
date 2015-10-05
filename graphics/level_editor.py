from assets.files.utilities.key_handler import KeyHandler
from assets.files.utilities.globals import Globals

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

				spawn_entity = False
				new_entity = {
					"type": None,
					"x": self.block_chosen[0],
					"y": self.block_chosen[1]
				}

				if pygame.K_RETURN in keys:

					new_entity['type'] = 'platform'
					spawn_entity = True

				elif pygame.K_p in keys:

					new_entity['type'] = 'player'
					spawn_entity = True

				elif pygame.K_b in keys:

					new_entity['type'] = 'walker'
					spawn_entity = True

				elif pygame.K_a in keys:

					new_entity['type'] = 'archer'
					spawn_entity = True

				elif pygame.K_w in keys:

					new_entity['type'] = 'wizard'
					spawn_entity = True

				elif pygame.K_j in keys:

					new_entity['type'] = 'jumper'
					spawn_entity = True

				if spawn_entity:
					self.entities.append(new_entity)

			for x in self.entities:

				if x['type'] == 'platform':
					image = pygame.image.load("assets/images/blocks/snow.png").convert_alpha()

				elif x['type'] == 'player':
					image = pygame.image.load("assets/images/player/run_1.png").convert_alpha()

				elif x['type'] == 'wizard':
					image = pygame.image.load("assets/images/enemies/wizard/front1.png").convert_alpha()

				elif x['type'] == 'archer':
					image = pygame.image.load("assets/images/enemies/archer/archer_1.png").convert_alpha()

				elif x['type'] == 'walker':
					image = pygame.image.load("assets/images/enemies/walker/run_1.png").convert_alpha()

				elif x['type'] == 'jumper':
					image = pygame.image.load("assets/images/enemies/jumper/jumper_stand_1.png").convert_alpha()


				image = pygame.transform.scale(image, (self.block_size, self.block_size))

				self.window.blit(image, (x['x'] * self.block_size, x['y'] * self.block_size))
			pygame.draw.rect(self.window, red, [self.block_chosen[0] * self.block_size, self.block_chosen[1] * self.block_size, self.block_size, self.block_size])

			pygame.display.flip()
