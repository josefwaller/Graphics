import pygame
from assets.files.utilities.globals import Globals
from .base_entity import BaseEntity

class Platform (BaseEntity):

	top_block = None
	inner_block = None

	def __init__ (self, x, y, w, h, top_block, inner_block):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size
		self.w = w
		self.h = h
		self.s = Globals.block_size

		self.top_block = self.img_load(top_block)

		if not inner_block == None:
			self.inner_block = self.img_load(inner_block)

	def render (self):

		top_block = pygame.transform.scale(self.top_block, (self.s, self.s))
		if self.h > 1:
			inner_block = pygame.transform.scale(self.inner_block, (self.s, self.s))

		for h in range(self.h):
			y = self.y + (Globals.block_size * h)

			for w in range(self.w):
				x = self.x + (Globals.block_size * w) + Globals.camera_offset['x']

				if h == 0:
					Globals.window.blit(top_block, (x, y))

				else:
					Globals.window.blit(inner_block, (x, y))




