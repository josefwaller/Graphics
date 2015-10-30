import pygame
from assets.files.utilities.globals import Globals
from .base_entity import BaseEntity
from assets.files.utilities.hitbox import Hitbox

class Platform (BaseEntity):

	top_block = None
	inner_block = None

	update_top_block = None
	update_inner_block = None

	def __init__ (self, x, y, w, h, top_block, inner_block, update_top_block=None, update_inner_block=None):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size
		self.w = w * Globals.block_size
		self.h = h * Globals.block_size
		self.s = Globals.block_size

		self.update_inner_block = update_inner_block
		self.update_top_block = update_top_block

		self.hitboxes = [
			Hitbox(x=0, y=0, w=self.w, h=self.h, parent=self)
		]

		self.top_block = self.img_load(top_block)

		self.is_static = True

		if not inner_block == None:
			self.inner_block = self.img_load(inner_block)

	def update (self):

		if not self.last_graphics == Globals.graphics_level:

			self.update_graphics()

		if self.is_showing:
			self.render()

		for hb in self.hitboxes:

			hb.update()

	def update_graphics (self):

		if not self.update_top_block == None and not self.update_inner_block == None:

			self.inner_block = self.img_load(self.update_inner_block)
			self.top_block = self.img_load(self.update_top_block)

	def render (self):

		top_block = pygame.transform.scale(self.top_block, (self.s, self.s))
		if self.h > 1:
			inner_block = pygame.transform.scale(self.inner_block, (self.s, self.s))

		for h in range(int(self.h / Globals.block_size)):
			y = self.y + (Globals.block_size * h)

			for w in range(int(self.w / Globals.block_size)):
				x = self.x + (Globals.block_size * w) + Globals.camera_offset['x']

				try:

					if h == 0:
						Globals.window.blit(top_block, (x, y))

					else:
						Globals.window.blit(inner_block, (x, y))

				except:
					pass




