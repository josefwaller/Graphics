import pygame
from .globals import Globals
from .entities import BaseEntity

class Platform ():

	top_block = None
	inner_block = None

	def __init__ (self, x, y, w, h, top_block, inner_block):

		self.x = x
		self.y = y
		self.w = w
		self.h = h

		self.top_block = top_block
		self.inner_block = inner_block

	def render (self):

		width = Globals.block_size
		height = Globals.block_size
		x = Globals.block_size * self.x
		y = Globals.block_size * self.y

		top_block = pygame.transform.scale(self.top_block, (width, height))
		if self.inner_block != None:
			inner_block = pygame.transform.scale(self.inner_block, (width, height))

		for h in range(self.h):
			for w in range(self.w):
				if h == 0:

					Globals.window.blit(top_block, (x + w * width, y + h * height))

				else:

					Globals.window.blit(inner_block, (x + w * width, y + h * height))




