import pygame
from .globals import Globals
from .entities import BaseEntity

class Platform ():

	top_block = None
	inner_block = None

	def __init__ (self, x, y, w, h, top_block, inner_block):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size
		self.w = w
		self.h = h
		self.s = Globals.block_size

		self.top_block = top_block
		self.inner_block = inner_block

	def render (self):

		top_block = pygame.transform.scale(self.top_block, (self.s, self.s))
		if self.h > 1:
			inner_block = pygame.transform.scale(self.inner_block, (self.s, self.s))

		for h in range(self.h):
			y = self.y + (Globals.block_size * h)

			for w in range(self.w):
				x = self.x + (Globals.block_size * w)

				if h == 0:
					Globals.window.blit(top_block, (x, y))

				else:
					Globals.window.blit(inner_block, (x, y))




