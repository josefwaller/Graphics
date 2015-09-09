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

		width = Globals.block_size * self.w
		height = Globals.block_size * self.h
		x = Globals.pixel_size * self.x
		y = Globals.pixel_size * self.y

		if self.is_animated:
			self.unix = time.time() * 1000
			
			if self.last_sprite_time < self.unix - self.sprite_interval:

				self.this_index += 1
				self.last_sprite_time = time.time() * 1000

			if self.this_index >= len(self.sprite_indexes):
				self.this_index = 0

			sprite = pygame.transform.scale(self.sprites[self.sprite_indexes[self.this_index]], (width, height))

			if self.facingLeft:

				sprite = pygame.transform.flip(sprite, True, False)

			Globals.window.blit(sprite, (x, y))

		else:

			#draw
			print("Not animated")

class JumpingEntity (BaseEntity):

	jump_strength = None
	momY = None
	is_grounded = None

	def start_jump (self):

		self.momY = self.jump_strength

		self.is_grounded = False
		self.last_time = time.time()

	def jump_update (self):

		self.delta_time = time.time() - self.last_time

		starting_y = self.y

		if self.is_grounded == False:

			self.momY -= 9.8 * Globals.block_size * self.delta_time

			self.y -= self.momY * self.delta_time

			for platform in Globals.platforms:

				collide_x = False
				collide_y = False

				block_con = Globals.pixel_size / Globals.block_size
		
				if self.x * block_con <= platform.x + platform.w:
					if self.x * block_con + self.w >= platform.x:

						collide_x = True
				print("%s compared to %s" % (self.y * block_con + self.h, platform.y ))
				print("%sasdf compared to %s" % (starting_y *block_con, platform.y ))

				if self.y * block_con + self.h >= platform.y :
					if starting_y * block_con + self.h < platform.y:

						collide_y = True

				if collide_x and collide_y:

					self.is_grounded = True
					self.y = platform.y - self.h
				else:
					self.is_grounded = False

		self.last_time = time.time()