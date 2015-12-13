import pygame
from assets.files.utilities.globals import Globals
from .base_entity import BaseEntity
from assets.files.utilities.hitbox import Hitbox


class Platform (BaseEntity):

	# images
	top_block = None
	inner_block = None

	# the images after the endblock has been hit
	update_top_block = None
	update_inner_block = None

	def __init__ (self, x, y, w, h):

		# sets coords and dimensions
		self.x = x * Globals.block_size
		self.y = y * Globals.block_size
		self.w = w * Globals.block_size
		self.h = h * Globals.block_size
		self.s = Globals.block_size

		# Adds a single hitbox that covers the whole block
		self.add_hitbox(0, 0, 16, 16)

		self.graphic_images = [
			[
				self.img_load("blocks/t_dirt_top.png"),
				self.img_load("blocks/t_dirt.png"),
			],
			[
				self.img_load("blocks/snow_top.png"),
				self.img_load("blocks/snow.png"),
			],
			[
				self.img_load("blocks/16_castle.png"),
				self.img_load("blocks/16_castle.png"),
			]
		]
		self.top_block = self.graphic_images[Globals.graphics_level][0]
		self.inner_block = self.graphic_images[Globals.graphics_level][1]

		self.is_static = True

	def update(self):

		if not Globals.is_paused:

			for hb in self.hitboxes:
				hb.update()

		if self.is_showing:
			self.render()

	def render (self):

		top_block = pygame.transform.scale(self.top_block, (self.s, self.s))
		if self.h > 1:
			inner_block = pygame.transform.scale(self.inner_block, (self.s, self.s))

		for h in range(int(self.h / Globals.block_size)):
			y = self.y + (Globals.block_size * h) + Globals.camera_offset['y']

			for w in range(int(self.w / Globals.block_size)):
				x = self.x + (Globals.block_size * w) + Globals.camera_offset['x']

				if h == 0:
					Globals.window.blit(top_block, (x, y))

				else:
					Globals.window.blit(inner_block, (x, y))
