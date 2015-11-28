from assets.files.entities.base_entity import BaseEntity

from assets.files.utilities.globals import Globals

import pygame

class Trigger (BaseEntity):

	x = 0
	y = 0 
	w = 0
	h = 0

	on_enter = None

	used = False

	def __init__ (self, x, y, w, h, on_enter, parameters):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size
		self.h = h * Globals.block_size
		self.w = w * Globals.block_size

		self.para = parameters

		self.on_enter = on_enter

	def check_for_collision(self, target):

		if target.x + target.w > self.x:
			if target.x < self.x + self.w:
				if target.y + target.h > self.y:
					if target.y < self.y + self.h:
						return True

		return False

	def update (self):

		p = Globals.player

		if self.check_for_collision(p) and not self.used:

			self.on_enter(*self.para)
			self.used = True

		if Globals.debug:

			pink = (255, 0, 255)

			pygame.draw.rect(Globals.window, pink, [self.x + Globals.camera_offset['x'], self.y, self.w, self.h])