from assets.files.utilities.globals import Globals

import pygame

class Hitbox ():

	x = None
	y = None
	w = None
	h = None
	offset_x = None
	offset_y = None
	parent = None

	def __init__(self, x, y, w, h, parent):

		self.offset_x = x
		self.offset_y = y
		self.w = w
		self.h = h
		self.parent = parent

		self.last = {
			"x": x,
			"y": y
		}

		self.update()

	def update (self):

		if not self.x == None:

			self.last['x'] = self.x
			self.last['y'] = self.y

		if self.parent.facing_left:
			self.x = self.parent.x + self.offset_x

		else:
			self.x = self.parent.x  + self.offset_x

		self.y = self.parent.y + self.offset_y


		if Globals.debug:
			self.debug_draw()

	def debug_draw(self):

		pink = (255, 0, 255)

		pygame.draw.rect(Globals.window, pink, [self.x + Globals.camera_offset['x'], self.y, self.w, self.h], 2) 