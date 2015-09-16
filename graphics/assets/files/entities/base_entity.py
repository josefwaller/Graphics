import calendar
import time
import pygame

from assets.files.utilities.globals import Globals

#Defualt class for everything
class BaseEntity ():
	momY = None
	is_grounded = None
	gravity_strength = None

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

	def make_pixelated(self, num):

		return int(num * (Globals.block_size / 16))

	def check_for_collision(self, target):
		if target.x + target.w > self.x:
			if target.x < self.x + self.w:
				if target.y + target.h > self.y:
					if target.y < self.y + self.h:
						return True

		return False

	def render (self):

		sprite = 0

		if self.is_animated:
			self.unix = time.time() * 1000
			
			if self.last_sprite_time < self.unix - self.sprite_interval:

				self.this_index += 1
				self.last_sprite_time = time.time() * 1000

			if self.this_index >= len(self.sprite_indexes):
				self.this_index = 0

			sprite = self.sprites[self.sprite_indexes[self.this_index]]

		else:

			sprite = self.image

		sprite = pygame.transform.scale(sprite, (self.w, self.h))

		if not self.facing_left:

			sprite = pygame.transform.flip(sprite, True, False)

		Globals.window.blit(sprite, (self.x + Globals.camera_offset['x'], self.y + Globals.camera_offset['y']))

	def gravity_update (self):

		starting_y = self.y

		if self.is_grounded == False:

			self.momY -= self.gravity_strength * self.delta_time

			self.y -= self.momY * self.delta_time

			for platform in Globals.platforms:

				collide_x = False
				collide_y = False

				if self.x <= platform.x + platform.w * Globals.block_size:
					if self.x + self.w >= platform.x:

						collide_x = True

				if self.y + self.h >= platform.y :
					if starting_y + self.h < platform.y:

						collide_y = True

				if collide_x and collide_y:

					self.is_grounded = True
					self.y = (platform.y - self.h)
					self.platform_under = platform
					break
				else:
					self.is_grounded = False

		else:

			platform = self.platform_under

			if platform == None or self.x > platform.x + platform.w * Globals.block_size or self.x + self.w < platform.x:

				self.is_grounded = False
				self.momY = 0
				self.platform_under = None
