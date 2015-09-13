from .jumping_entity import JumpingEntity
from ..utilities.globals import Globals

import time
import pygame

class Player (JumpingEntity):

	x_translate = 0
	speed = 8

	jump_strength = 13
	momY = 0
	is_grounded = True

	last_time = 0
	delta_time = 0

	def __init__(self, x, y):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size
		self.w = int(10 * (Globals.block_size / 16))
		self.h = int(19 * (Globals.block_size / 16))

		self.jump_strength *= Globals.block_size

		self.sprites = [
			pygame.image.load("assets/images/player/run_1.png").convert_alpha(),
			pygame.image.load("assets/images/player/run_2.png").convert_alpha(),
			pygame.image.load("assets/images/player/run_3.png").convert_alpha(),
			pygame.image.load("assets/images/player/run_2.png").convert_alpha(),
		]

		self.sprite_indexes = [
			1
		]

		self.jump_last_time = time.time()

		self.is_animated = True
		self.sprite_interval = 100

		self.gravity_strength = 15 * Globals.block_size

	def while_keys_down (self, keys):

		if pygame.K_LEFT in keys:

			self.x_translate = -1
			self.sprite_indexes = range(4)
			self.facing_left = True

		if pygame.K_RIGHT in keys:

			self.x_translate = 1
			self.sprite_indexes = range(4)
			self.facing_left = False

		if pygame.K_RIGHT not in keys and pygame.K_LEFT not in keys:

			self.x_translate = 0
			self.sprite_indexes = [1]

		if pygame.K_UP in keys and self.is_grounded:

			self.start_jump()


	def update (self):

		self.x += self.x_translate * self.speed

		self.jump_update()

		self.render()