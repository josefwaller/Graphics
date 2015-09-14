from assets.files.utilities.globals import Globals
from assets.files.entities.jumping_entity import JumpingEntity

import time
import pygame

class Walker (JumpingEntity):

	facing_left = False
	speed = 8

	def __init__(self, x, y, facing_left=False):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size
		self.w = Globals.block_size
		self.h = 2 * Globals.block_size
		self.facing_left = facing_left

		self.is_animated = True

		self.sprite_interval = 150

		self.last_time = time.time()

		self.sprites = [
			pygame.image.load("assets/images/enemies/walker/run_1.png"),
			pygame.image.load("assets/images/enemies/walker/run_2.png"),
			pygame.image.load("assets/images/enemies/walker/run_3.png"),
			pygame.image.load("assets/images/enemies/walker/run_2.png")
		]

		self.gravity_strength = 10

		self.sprite_indexes = [
			0,
			1,
			2,
			1
		]

		self.jump_last_time = time.time()

	def move (self):

		if self.facing_left == True:
			self.x += self.speed * self.delta_time

		else:
			self.x -= self.speed * self.delta_time

	def update (self):

		self.set_delta_time()

		self.move()

		self.jump_update()
		self.render()
