from assets.files.entities.base_entity import BaseEntity

from assets.files.utilities.globals import Globals

import pygame


class Prop (BaseEntity):

	sprite_interval = 100

	def __init__(self, x, y, images):

		# Loads images
		self.sprites = []
		self.sprite_indexes = range(len(images))
		for img in images:
			self.sprites.append(self.img_load(img))

		self.is_animated = True

		# Initializes

		self.w = int((Globals.block_size / Globals.pixels_per_block) * self.sprites[0].get_size()[0])
		self.h = int((Globals.block_size / Globals.pixels_per_block) * self.sprites[1].get_size()[1])

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size + Globals.block_size - self.h

		for s in range(len(self.sprites)):
			self.sprites[s] = pygame.transform.scale(self.sprites[s], (self.w, self.h))

	def update(self):
		self.render()
