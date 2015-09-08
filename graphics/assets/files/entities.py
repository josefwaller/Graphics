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
	is_jumping = None
	momY = None
	is_grounded = None

	def start_jump (self):

		self.momY = self.jump_strength

		self.is_jumping = True
		self.last_time = time.time()

	def jump_update (self):

		self.delta_time = time.time() - self.last_time

		if self.is_jumping == True:

			self.momY -= 9.8 * 5 * self.delta_time

			self.y -= self.momY * self.delta_time

		self.last_time = time.time()