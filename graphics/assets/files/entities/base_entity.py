import calendar
import time
import pygame

from assets.files.utilities.globals import Globals

#Defualt class for everything
class BaseEntity ():

	x = 0
	y = 0
	w = 0
	h = 0

	unix = 0

	is_animated = False

	image = None

	sprites = None
	sprite_indexes = None
	this_index = 0
	platform_under = None

	last_sprite_time = 0
	sprite_interval = 0

	facing_left = False

	last_time = 0

	def set_delta_time(self):

		if self.last_time == 0:
			self.last_time = time.time()

		self.delta_time = time.time() - self.last_time

		self.last_time = time.time()


	def render (self):

		if self.is_animated:
			self.unix = time.time() * 1000
			
			if self.last_sprite_time < self.unix - self.sprite_interval:

				self.this_index += 1
				self.last_sprite_time = time.time() * 1000

			if self.this_index >= len(self.sprite_indexes):
				self.this_index = 0

			sprite = pygame.transform.scale(self.sprites[self.sprite_indexes[self.this_index]], (self.w, self.h))

			if not self.facing_left:

				sprite = pygame.transform.flip(sprite, True, False)

			Globals.window.blit(sprite, (self.x + Globals.camera_offset['x'], self.y + Globals.camera_offset['y']))

		else:

			#draw
			print("Not animated")
