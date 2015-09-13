import calendar
import time
import pygame

from assets.files.globals import Globals

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

	last_sprite_time = 0
	sprite_interval = 0

	facingLeft = False

	def render (self):

		if self.is_animated:
			self.unix = time.time() * 1000
			
			if self.last_sprite_time < self.unix - self.sprite_interval:

				self.this_index += 1
				self.last_sprite_time = time.time() * 1000

			if self.this_index >= len(self.sprite_indexes):
				self.this_index = 0

			sprite = pygame.transform.scale(self.sprites[self.sprite_indexes[self.this_index]], (self.w, self.h))

			if not self.facingLeft:

				sprite = pygame.transform.flip(sprite, True, False)

			Globals.window.blit(sprite, (self.x, self.y))

		else:

			#draw
			print("Not animated")

class JumpingEntity (BaseEntity):

	jump_strength = None
	momY = None
	is_grounded = None
	gravity_strength = None

	def start_jump (self):

		self.momY = self.jump_strength

		self.is_grounded = False
		self.last_time = time.time()

	def jump_update (self):

		delta_time = time.time() - self.last_time

		starting_y = self.y

		if self.is_grounded == False:

			self.momY -= self.gravity_strength * delta_time

			self.y -= self.momY * delta_time

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
					break
				else:
					self.is_grounded = False

		self.last_time = time.time()