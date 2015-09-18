from assets.files.utilities.key_handler import KeyHandler

import pygame

class LevelEditor():

	block_chosen = [0, 0]

	blocks = [[]]

	def __init__(self):

		windowSize = width, height = 500, 500
		self.window = pygame.display.set_mode(windowSize)

		self.block_size = int(self.window.get_size()[1] / 16)

		self.level_width = 20

		for i in range(self.level_width):

			if len(self.blocks) <= i:

				self.blocks.append([])

			for x in range(16):

				if len(self.blocks[i]) <= x:

					self.blocks[i].append(False)

				try:

					self.blocks[i][x]

				except IndexError:

					print("Index error")

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

				if pygame.K_RETURN in keys:

					x = self.block_chosen[0]
					y = self.block_chosen[1]

					self.blocks[x][y] = not self.blocks[x][y]

			for x in range(len(self.blocks)):

				for i in range(len(self.blocks[x])):

					if self.blocks[x][i] == True:

						pygame.draw.rect(self.window, (0, 0, 0), [x * self.block_size, i * self.block_size, self.block_size, self.block_size])

			pygame.draw.rect(self.window, red, [self.block_chosen[0] * self.block_size, self.block_chosen[1] * self.block_size, self.block_size, self.block_size])

			pygame.display.flip()
